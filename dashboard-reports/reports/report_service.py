from pdf_generator import generate_inspection_pdf


def create_inspection_report(inspection, output_path):
    """
    Create a PDF report for a completed inspection.

    This function acts as the integration layer between
    the backend inspection data and the PDF generator.
    """
    generate_inspection_pdf(
        inspection=inspection,
        output_path=output_path,
    )

    return output_path