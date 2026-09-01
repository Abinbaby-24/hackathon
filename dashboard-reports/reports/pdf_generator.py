from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_inspection_pdf(inspection, output_path):
    """
    Generate a PDF compliance inspection report.

    Parameters:
        inspection (dict): Inspection data.
        output_path (str): Path where the PDF will be saved.
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
    )

    elements = []

    # --------------------------------------------------
    # Title
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "Packaged Commodity Compliance Report",
            title_style,
        )
    )

    elements.append(
        Paragraph(
            "Legal Metrology Inspection",
            body_style,
        )
    )

    elements.append(Spacer(1, 15))

    # --------------------------------------------------
    # Inspection details
    # --------------------------------------------------

    product_name = inspection.get("productName", "N/A")
    inspection_id = inspection.get("id", "N/A")
    date = inspection.get("date", "N/A")
    status = inspection.get("status", "N/A")
    score = inspection.get("complianceScore", 0)

    details = [
        ["Product Name", str(product_name)],
        ["Inspection ID", str(inspection_id)],
        ["Inspection Date", str(date)],
        ["Compliance Status", str(status)],
        ["Compliance Score", f"{score}%"],
    ]

    details_table = Table(
        details,
        colWidths=[50 * mm, 110 * mm],
    )

    details_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#e2e8f0"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#1e293b"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#cbd5e1"),
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    elements.append(details_table)

    # --------------------------------------------------
    # Violations
    # --------------------------------------------------

    elements.append(
        Paragraph(
            "Violations Detected",
            heading_style,
        )
    )

    violations = inspection.get("violations", [])

    if violations:
        violation_data = [["#", "Violation"]]

        for index, violation in enumerate(violations, start=1):
            violation_data.append(
                [str(index), str(violation)]
            )

        violation_table = Table(
            violation_data,
            colWidths=[15 * mm, 145 * mm],
        )

        violation_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#fee2e2"),
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.HexColor("#cbd5e1"),
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP",
                    ),
                ]
            )
        )

        elements.append(violation_table)

    else:
        elements.append(
            Paragraph(
                "No violations detected. The product is compliant "
                "with the evaluated requirements.",
                body_style,
            )
        )

    # --------------------------------------------------
    # Footer / note
    # --------------------------------------------------

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "This report was generated by the Packaged Commodity Inspector system.",
            body_style,
        )
    )

    # --------------------------------------------------
    # Generate PDF
    # --------------------------------------------------

    doc.build(elements)