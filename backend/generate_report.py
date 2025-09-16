# generate_report.py

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Web Security Toolkit - Security Report', ln=True, align='C')
        self.ln(10)

    def section_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def section_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 8, text)
        self.ln(5)

def format_section(data):
    """Helper to format each section nicely."""
    if not data or data == "Not Scanned":
        return "Not scanned."
    if isinstance(data, dict) or isinstance(data, list):
        import json
        return json.dumps(data, indent=2)
    return str(data)

def generate_report(scan_data, filename="security_report.pdf"):
    try:
        pdf = PDF()
        pdf.add_page()

        pdf.set_font('Arial', '', 12)

        sections = [
            ('Email Security Check', scan_data.get('email')),
            ('Dark Web Monitoring', scan_data.get('darkweb')),
            ('SSL Certificate Check', scan_data.get('ssl')),
            ('Web Vulnerability Scan', scan_data.get('vulnerability')),
            ('Threat Intelligence Check', scan_data.get('threat')),
            ('Subdomain Enumeration', scan_data.get('subdomain')),
            ('Open Port Scan', scan_data.get('ports')),
        ]

        for title, data in sections:
            pdf.section_title(title)
            pdf.section_body(format_section(data))

        pdf.output(filename)
        return {"message": "PDF generated successfully"}

    except Exception as e:
        return {"error": f"Failed to generate PDF: {str(e)}"}
