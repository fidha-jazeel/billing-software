# utils/invoice_generator.py
"""
Professional Invoice PDF generator (ReportLab Platypus).
Features:
 - Clean header with company name, address and optional logo
 - Structured table with separate columns (no concatenated description)
 - Handles multi-page invoices, repeats table header
 - Soft grid, alternating row shading, proper numeric alignment
 - Currency formatting and totals
Usage:
    from utils.invoice_generator import generate_invoice_pdf
    generate_invoice_pdf(invoice_data, "/path/to/out.pdf")
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from travel_billing_software.utils.path_loader import resource_path
from travel_billing_software.utils.config_manager import ConfigManager
from travel_billing_software.config.config import get_currency_symbol
import os
from datetime import datetime
import math

# ---------------------------
# FONT REGISTRATION (Unicode-safe)
# ---------------------------
# Register Unicode fonts (Regular + Bold)
try:
    # base = os.path.join(os.path.dirname(__file__), '..', 'fonts')

    reg_path = resource_path("travel_billing_software/fonts/DejaVuSans.ttf")
    bold_path = resource_path("travel_billing_software/fonts/DejaVuSans-Bold.ttf")

    if os.path.exists(reg_path):
        pdfmetrics.registerFont(TTFont('DejaVuSans', reg_path))

    if os.path.exists(bold_path):
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold_path))

    # REGISTER FAMILY (fixes bold detection)
    pdfmetrics.registerFontFamily(
        'DejaVuSans',
        normal='DejaVuSans',
        bold='DejaVuSans-Bold',
        italic='DejaVuSans',
        boldItalic='DejaVuSans-Bold'
    )

    DEFAULT_FONT = 'DejaVuSans'
    DEFAULT_FONT_BOLD = 'DejaVuSans-Bold'

except Exception as e:
    print("Font registration error:", e)
    DEFAULT_FONT = 'Helvetica'
    DEFAULT_FONT_BOLD = 'Helvetica-Bold'


# ---------------------------
# STYLES
# ---------------------------
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='H1', fontName=DEFAULT_FONT_BOLD, fontSize=18, leading=22, spaceAfter=6))
styles.add(ParagraphStyle(name='H2', fontName=DEFAULT_FONT_BOLD, fontSize=12, leading=14, spaceAfter=4))
styles.add(ParagraphStyle(name='NormalSmall', fontName=DEFAULT_FONT, fontSize=9, leading=11))
styles.add(ParagraphStyle(name='TableCell', fontName=DEFAULT_FONT, fontSize=9, leading=11))
styles.add(ParagraphStyle(name='TableCellBold', fontName=DEFAULT_FONT_BOLD, fontSize=9, leading=11, spaceAfter=2))
styles.add(ParagraphStyle(name='Footer', fontName=DEFAULT_FONT, fontSize=8, leading=10, alignment=1))

try:
    styles['Normal'].fontName = DEFAULT_FONT
    styles['NormalSmall'].fontName = DEFAULT_FONT
    styles['TableCell'].fontName = DEFAULT_FONT
except Exception:
    pass


# ---------------------------
# Get currency from ConfigManager
# ---------------------------
def _get_default_currency():
    """Get currency symbol from config settings."""
    try:
        cm = ConfigManager()
        return cm.get_invoice_config().get('currency_symbol', f'{get_currency_symbol()}')
    except:
        return f'{get_currency_symbol()}'

DEFAULT_CURRENCY = _get_default_currency()

# ---------------------------
# UTILITIES
# ---------------------------
def _format_currency(val, currency_symbol=None):
    """Format numeric value using currency symbol. Safe fallback for non-numbers."""
    try:
        v = float(val)
        cur = currency_symbol or DEFAULT_CURRENCY
        # ensure space after symbol and thousands separator
        return f"{cur} {v:,.2f}"
    except Exception:
        cur = currency_symbol or DEFAULT_CURRENCY
        return f"{cur} 0.00"

class HorizontalLine(Flowable):
    """Simple horizontal line flowable."""
    def __init__(self, width='100%', thickness=1, color=colors.HexColor('#e6e6e6')):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        w = self.canv._pagesize[0] - (2 * 15*mm)
        x1 = 0
        x2 = w
        self.canv.line(x1, 0, x2, 0)

def _on_page(canvas, doc, company, invoice_meta):
    """Header and footer for each page (called by SimpleDocTemplate)."""
    canvas.saveState()
    width, height = A4
    margin = 15 * mm
    header_y = height - margin + 8*mm

    # Left: Company name (prominent)
    canvas.setFont(DEFAULT_FONT, 14)
    canvas.setFillColor(colors.HexColor('#0b3d91'))
    canvas.drawString(margin, header_y, company.get('name', 'Company Name'))

    # Company address beneath with normal font (limited lines to avoid congestion)
    canvas.setFont(DEFAULT_FONT, 8)
    canvas.setFillColor(colors.HexColor('#333333'))
    addr_lines = str(company.get('address','')).splitlines()
    for i, ln in enumerate(addr_lines[:3]):  # limit lines
        canvas.drawString(margin, header_y - (12 + i*10), ln)

    # Right: Invoice meta block
    canvas.setFont(DEFAULT_FONT, 9)
    canvas.setFillColor(colors.black)
    canvas.drawRightString(width - margin, header_y, f"Invoice: {invoice_meta.get('number','')}")
    canvas.drawRightString(width - margin, header_y - 12, f"Date: {invoice_meta.get('date','')}")
    if invoice_meta.get('customer_id'):
        canvas.drawRightString(width - margin, header_y - 24, f"Customer ID: {invoice_meta.get('customer_id','')}")

    # Footer: page number and small note
    footer_y = 12*mm
    canvas.setFont(DEFAULT_FONT, 8)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawCentredString(width/2.0, footer_y, f"Page {doc.page} • Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    note = company.get('footer_note', '')
    if note:
        # left align small footer note (trimmed)
        canvas.drawString(margin, footer_y + 12, note[:140])

    canvas.restoreState()

# ---------------------------
# ITEMS TABLE BUILDER (now accepts currency symbol)
# ---------------------------
def _build_items_table(items, currency_symbol):
    """
    Build the items table data and compute totals.
    Expects items as list of dicts with keys:
      passenger_name, pnr, sector, supplier, type, class, qty, unit_price, tax_pct
    """
    header = [
        'S.No', 'Passenger', 'PNR', 'Sector', 'Type', 'Qty', 'Unit Price', 'Amount'
    ]
    data = [header]
    subtotal = 0.0
    total_tax = 0.0

    for i, it in enumerate(items, start=1):
        # prefer structured keys; fallback to description
        passenger = it.get('passenger_name') or it.get('passenger') or ''
        pnr = it.get('pnr','')
        sector = it.get('sector','')
        type_v = it.get('type', '')
        supplier = it.get('supplier','')
        cls = it.get('class') or it.get('travel_class') or ''
        qty = float(it.get('qty', 0) or 0)
        unit = float(it.get('unit_price', it.get('price', 0) or 0))
        tax_pct = float(it.get('tax_pct', it.get('tax', 0) or 0))

        line_sub = qty * unit
        tax_amt = line_sub * (tax_pct/100.0)
        line_total = line_sub + tax_amt

        subtotal += line_sub
        total_tax += tax_amt

        # Use Paragraph for passenger, supplier, sector so long text wraps
        passenger_para = Paragraph(str(passenger), styles['TableCell'])
        supplier_para = Paragraph(str(supplier), styles['TableCell'])
        sector_para = Paragraph(str(sector), styles['TableCell'])
        type_para = Paragraph(str(type_v), styles['TableCell'])

        row = [
            str(i),
            passenger_para,
            Paragraph(str(pnr), styles['TableCell']),
            sector_para,
            type_para,
            str(int(qty) if qty.is_integer() else f"{qty:g}"),
            Paragraph(_format_currency(unit, currency_symbol), styles['TableCell']),
            Paragraph(_format_currency(line_total, currency_symbol), styles['TableCell'])
        ]

        data.append(row)

    return data, subtotal, total_tax

# ---------------------------
# MAIN GENERATOR
# ---------------------------
def generate_invoice_pdf(invoice_data: dict, output_path: str):
    """
    invoice_data expected keys:
      company: {name, address, footer_note, logo_path (optional)}
      invoice_meta: {number, date, customer_id}
      customer: {name, address, contact}
      items: [ { passenger_name, pnr, sector, supplier, type, class, qty, unit_price, tax_pct }, ... ]
      discount: numeric (optional)
      notes: string (optional)
      terms: string (optional)
      currency: symbol (optional, e.g. '₹' or '$')
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

    # Margins chosen to be safe for most printers
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=38*mm, bottomMargin=28*mm)

    story = []
    company = invoice_data.get('company', {})
    invoice_meta = invoice_data.get('invoice_meta', {})
    customer = invoice_data.get('customer', {})
    items = invoice_data.get('items', []) or []
    notes = invoice_data.get('notes', '')
    terms = invoice_data.get('terms', '')
    discount = float(invoice_data.get('discount', 0) or 0)
    currency_symbol = invoice_data.get('currency', DEFAULT_CURRENCY)

    # Header area: optionally render logo on right, company name + address on left
    left = []
    left.append(Paragraph(company.get('name', 'Company Name'), styles['H1']))
    if company.get('tagline'):
        left.append(Paragraph(company.get('tagline'), styles['H2']))
    if company.get('address'):
        left.append(Paragraph(company.get('address').replace('\n','<br/>'), styles['NormalSmall']))
    left_block = left

    right = []
    logo_path = company.get('logo_path')
    if logo_path and os.path.exists(logo_path):
        try:
            img = Image(logo_path)
            # scale preserving aspect ratio; limit height
            max_h = 22 * mm
            aspect = img.imageWidth / float(img.imageHeight)
            img.drawHeight = max_h
            img.drawWidth = max_h * aspect
            right.append(img)
        except Exception:
            right.append(Paragraph('', styles['NormalSmall']))

    # Build a 2-column header table: left company info, right logo/meta
    header_table = Table([[left_block, right]], colWidths=[doc.width*0.72, doc.width*0.28])
    header_table.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN',(1,0),(1,0),'RIGHT'),
        ('LEFTPADDING',(0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(-1,-1),0),
    ]))
    story.append(header_table)
    story.append(Spacer(1,6))

    # Invoice Title and Bill To / From block
    title_table = Table([
        [Paragraph('<b>INVOICE</b>', styles['H1']), ''],
    ], colWidths=[doc.width*0.6, doc.width*0.4])
    title_table.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN',(0,0),(0,0),'LEFT'),
    ]))
    story.append(title_table)
    story.append(Spacer(1,8))

    # Bill To (left) / Invoice meta (right)
    bill_to = []
    bill_to.append(Paragraph('<b>Bill To</b>', styles['TableCellBold']))
    if customer.get('name'):
        bill_to.append(Paragraph(customer.get('name'), styles['TableCell']))
    if customer.get('address'):
        bill_to.append(Paragraph(customer.get('address').replace('\n','<br/>'), styles['TableCell']))
    if customer.get('contact'):
        bill_to.append(Paragraph(f"Contact: {customer.get('contact')}", styles['TableCell']))

    meta = []
    meta.append(Paragraph(f"<b>Invoice #</b> {invoice_meta.get('number','')}", styles['TableCell']))
    meta.append(Paragraph(f"<b>Date</b> {invoice_meta.get('date','')}", styles['TableCell']))
    if invoice_meta.get('customer_id'):
        meta.append(Paragraph(f"<b>Customer ID</b> {invoice_meta.get('customer_id')}", styles['TableCell']))

    info_table = Table([[bill_to, meta]], colWidths=[doc.width*0.6, doc.width*0.4])
    info_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(info_table)
    story.append(Spacer(1,10))

    # Items table (build using currency_symbol)
    table_data, subtotal, total_tax = _build_items_table(items, currency_symbol)

    # Table styling: subtle grid, repeating header, alternating rows
    col_widths = [
        10*mm,   # S.No
        45*mm,   # Passenger
        20*mm,   # PNR
        28*mm,   # Sector
        20*mm,   # Type
        12*mm,   # Qty
        22*mm,   # Unit Price
        23*mm    # Amount
    ]

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1, hAlign='LEFT')
    tbl_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f5f7fa')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#333333')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),   # S.No
        ('ALIGN', (5,1), (5,-1), 'CENTER'),   # Qty

        # Unit Price right aligned
        ('ALIGN', (6,1), (6,-1), 'RIGHT'),

        # Amount right aligned
        ('ALIGN', (7,1), (7,-1), 'RIGHT'),

        ('FONTNAME', (0,0), (-1,0), DEFAULT_FONT),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor('#e6e6e6')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#e6e6e6')),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ])
    tbl.setStyle(tbl_style)

    # Alternating row background
    for i in range(1, len(table_data)):
        if i % 2 == 0:
            tbl_style.add('BACKGROUND', (0,i), (-1,i), colors.HexColor('#fbfbfb'))
    tbl.setStyle(tbl_style)

    story.append(tbl)
    story.append(Spacer(1,8))

    # Totals block (right aligned) - use currency_symbol
    grand_total = subtotal + total_tax - discount

    totals_data = [
        ['', '', Paragraph('Subtotal', styles['TableCellBold']), Paragraph(_format_currency(subtotal, currency_symbol), styles['TableCell'])],
        ['', '', Paragraph('Tax', styles['TableCellBold']), Paragraph(_format_currency(total_tax), styles['TableCell'])],
    ]

    if discount:
        totals_data.append(['', '', Paragraph('Discount', styles['TableCellBold']),
                            Paragraph(_format_currency(discount), styles['TableCell'])])

    totals_data.append([
        '',
        '',
        Paragraph('<b>Total</b>', styles['TableCellBold']),
        Paragraph(_format_currency(grand_total, currency_symbol), styles['TableCellBold'])
    ])

    # Paid Amount and Balance
    paid_amount = float(invoice_data.get('paid_amount', 0))
    balance = float(invoice_data.get('balance', grand_total - paid_amount))
    totals_data.append([
        '',
        '',
        Paragraph('Paid Amount', styles['TableCellBold']),
        Paragraph(_format_currency(paid_amount, currency_symbol), styles['TableCell'])
    ])
    totals_data.append([
        '',
        '',
        Paragraph('Balance', styles['TableCellBold']),
        Paragraph(_format_currency(balance, currency_symbol), styles['TableCell'])
    ])

    totals_tbl = Table(totals_data, colWidths=[doc.width*0.5, doc.width*0.1, doc.width*0.2, doc.width*0.2], hAlign='RIGHT')
    totals_tbl.setStyle(TableStyle([
        ('SPAN', (0,0), (1,0)),
        ('SPAN', (0,1), (1,1)),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ('FONTNAME', (2,0), (3,-1), DEFAULT_FONT),
        ('FONTSIZE', (2,0), (3,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(totals_tbl)
    story.append(Spacer(1,8))

    # Notes and Terms
    if notes:
        story.append(Paragraph('<b>Notes:</b>', styles['TableCellBold']))
        story.append(Paragraph(notes.replace('\n','<br/>'), styles['TableCell']))
        story.append(Spacer(1,6))

    if terms:
        story.append(Paragraph('<b>Terms & Conditions:</b>', styles['TableCellBold']))
        story.append(Paragraph(terms.replace('\n','<br/>'), styles['TableCell']))
        story.append(Spacer(1,6))

    # Footer small print (document build will call _on_page)
    def _build_canvas(c, d):
        _on_page(c, d, company, invoice_meta)

    doc.build(story, onFirstPage=_build_canvas, onLaterPages=_build_canvas)

    return output_path
