from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import os

class PDFGenerator:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def generate_invoice_pdf(self, invoice_id, filename):
        """Generate PDF for an invoice"""
        try:
            # Get invoice data
            invoice = self.db.get_invoice(invoice_id)
            if not invoice:
                raise Exception("Invoice not found")
            
            # Get company settings
            settings = self.db.get_settings()
            
            # Create PDF
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            
            # Styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#0d7377'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#0d7377'),
                spaceAfter=12
            )
            
            normal_style = styles['Normal']
            
            # Company header
            company_name = settings.get('company_name', 'Travel Agency')
            story.append(Paragraph(company_name, title_style))
            
            if settings.get('company_address'):
                story.append(Paragraph(settings['company_address'], normal_style))
                story.append(Spacer(1, 0.1*inch))
            
            contact_info = []
            if settings.get('company_contact'):
                contact_info.append(f"Phone: {settings['company_contact']}")
            if settings.get('company_email'):
                contact_info.append(f"Email: {settings['company_email']}")
            if settings.get('company_gst'):
                contact_info.append(f"GST: {settings['company_gst']}")
            
            if contact_info:
                story.append(Paragraph(" | ".join(contact_info), normal_style))
            
            story.append(Spacer(1, 0.3*inch))
            
            # Invoice title
            story.append(Paragraph("INVOICE", heading_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Invoice details table
            invoice_info = [
                ['Invoice Number:', invoice['invoice_number']],
                ['Invoice Date:', datetime.strptime(invoice['invoice_date'], '%Y-%m-%d').strftime('%d-%m-%Y')],
                ['Customer Name:', invoice['customer_name']],
            ]
            
            info_table = Table(invoice_info, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Items table
            story.append(Paragraph("Items", heading_style))
            
            # Table headers
            items_data = [['#', 'Item Name', 'Ticket #', 'Sector', 'Qty', 'Price', 'Tax', 'Amount']]
            
            # Add items
            currency = settings.get('currency_symbol', '₹')
            for idx, item in enumerate(invoice['items'], 1):
                items_data.append([
                    str(idx),
                    item['item_name'],
                    item['ticket_number'] or '-',
                    item['sector'] or '-',
                    str(int(item['quantity'])),
                    f"{currency} {item['price_per_unit']:.2f}",
                    f"{item['tax_percentage']:.0f}%",
                    f"{currency} {item['amount']:.2f}"
                ])
            
            # Create items table
            items_table = Table(items_data, colWidths=[0.4*inch, 2*inch, 1*inch, 1*inch, 0.6*inch, 1*inch, 0.7*inch, 1.2*inch])
            items_table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d7377')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),
                ('ALIGN', (-3, 1), (-1, -1), 'RIGHT'),
                
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # Padding
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ]))
            story.append(items_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Totals section
            totals_data = [
                ['Subtotal:', f"{currency} {invoice['subtotal']:.2f}"],
                ['Tax Amount:', f"{currency} {invoice['tax_amount']:.2f}"],
                ['Total Amount:', f"{currency} {invoice['total_amount']:.2f}"],
                ['Received:', f"{currency} {invoice['received_amount']:.2f}"],
                ['Balance Due:', f"{currency} {invoice['balance']:.2f}"],
            ]
            
            totals_table = Table(totals_data, colWidths=[4.5*inch, 2*inch])
            totals_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -2), 'Helvetica'),
                ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LINEABOVE', (0, -2), (-1, -2), 1, colors.black),
                ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#0d7377')),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
            ]))
            story.append(totals_table)
            
            # Footer
            story.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            story.append(Paragraph("Thank you for your business!", footer_style))
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
