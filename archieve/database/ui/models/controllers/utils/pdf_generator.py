from fpdf import FPDF

def generate_invoice(filename, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Travel Billing Invoice", ln=True, align="C")
    pdf.ln(10)
    for line in data:
        pdf.cell(200, 10, txt=str(line), ln=True)
    pdf.output(filename)
    print(f"✅ PDF generated: {filename}")
