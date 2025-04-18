from fpdf import FPDF
from datetime import datetime

class CaseBriefPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Legal Case Brief", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Generated on {datetime.now().strftime('%d %b %Y')}", 0, 0, "C")

def generate_pdf(case_data: dict, output_path: str):
    pdf = CaseBriefPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 14)
    pdf.multi_cell(0, 10, f"Case: {case_data['case_name']}", align="L")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    for section, text in case_data["structured_summary"].items():
        title = section.capitalize()
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 8, f"{title}:", align="L")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 8, text)
        pdf.ln(4)

    if "evaluation" in case_data:
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 10, "Evaluation Metrics:", align="L")
        pdf.set_font("Helvetica", "", 11)
        for metric, value in case_data["evaluation"].items():
            if isinstance(value, float):
                value = f"{value:.2f}"
            elif isinstance(value, list):
                value = ", ".join(value)
            pdf.multi_cell(0, 8, f"{metric.replace('_', ' ').title()}: {value}")
    
    pdf.output(output_path)
