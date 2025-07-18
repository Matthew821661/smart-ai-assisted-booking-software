from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile

def export_pdf_report(ledger_df, tb_df, vat_df):
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    c = canvas.Canvas(temp_path, pagesize=A4)
    c.setFont("Helvetica", 12)
    y = 800
    c.drawString(50, y, "AI Bookkeeping Financial Report")
    y -= 30

    def draw_table(dataframe, title):
        nonlocal y
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, title)
        y -= 20
        c.setFont("Helvetica", 8)
        for _, row in dataframe.iterrows():
            row_str = " | ".join([str(i) for i in row.values])
            c.drawString(50, y, row_str[:120])
            y -= 12
            if y < 100:
                c.showPage()
                y = 800

    draw_table(ledger_df, "General Ledger")
    draw_table(tb_df, "Trial Balance")
    draw_table(vat_df, "VAT Summary")
    c.save()
    return temp_path
