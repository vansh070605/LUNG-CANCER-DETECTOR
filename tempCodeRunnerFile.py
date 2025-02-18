def generate_pdf():
    # Create a BytesIO buffer for the PDF file
    buffer = BytesIO()

    # Create a PDF canvas and write content
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Lung Cancer Risk Report")
    c.drawString(100, 730, "Prediction: High risk (Example)")  # You can replace this with actual prediction results

    # Save the PDF
    c.save()

    # Move the buffer cursor to the start
    buffer.seek(0)

    # Return the PDF as a downloadable file
    return send_file(buffer, as_attachment=True, download_name="lung_cancer_report.pdf", mimetype="application/pdf")

if __name__ == '__main__':