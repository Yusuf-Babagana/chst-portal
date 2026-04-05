from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from django.conf import settings
import os


def generate_application_pdf(application):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    title = Paragraph("COLLEGE OF HEALTH SCIENCES AND TECHNOLOGY HADEJIA", title_style)
    story.append(title)

    subtitle = Paragraph("ADMISSION APPLICATION FORM", title_style)
    story.append(subtitle)
    story.append(Spacer(1, 0.2 * inch))

    app_number = Paragraph(f"<b>Application Number:</b> {application.application_number}", styles['Normal'])
    story.append(app_number)
    story.append(Spacer(1, 0.3 * inch))

    if application.passport_photo:
        try:
            photo_path = os.path.join(settings.MEDIA_ROOT, str(application.passport_photo))
            if os.path.exists(photo_path):
                img = Image(photo_path, width=1.5*inch, height=1.5*inch)
                story.append(img)
                story.append(Spacer(1, 0.2 * inch))
        except:
            pass

    story.append(Paragraph("SECTION A: PERSONAL INFORMATION", heading_style))
    personal_data = [
        ['First Name:', application.first_name or ''],
        ['Surname:', application.surname or ''],
        ['Other Names:', application.other_names or ''],
        ['Date of Birth:', str(application.date_of_birth) if application.date_of_birth else ''],
        ['JAMB Number:', application.jamb_number or ''],
        ['JAMB Score:', str(application.jamb_score) if application.jamb_score else ''],
        ['Phone:', application.phone or ''],
        ['Email:', application.email or ''],
        ['Address:', application.address or ''],
        ['LGA:', application.lga or ''],
        ['State of Origin:', application.state_of_origin or ''],
    ]

    personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
    personal_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(personal_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Guardian/Next of Kin Information", heading_style))
    guardian_data = [
        ['Full Name:', application.guardian_name or ''],
        ['Phone:', application.guardian_phone or ''],
        ['Address:', application.guardian_address or ''],
        ['Relationship:', application.guardian_relationship or ''],
    ]

    guardian_table = Table(guardian_data, colWidths=[2*inch, 4*inch])
    guardian_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(guardian_table)
    story.append(Spacer(1, 0.3 * inch))

    schools = application.schools_attended.all()
    if schools.exists():
        story.append(Paragraph("SECTION B: SCHOOLS ATTENDED", heading_style))
        school_data = [['School Name', 'From', 'To']]
        for school in schools:
            school_data.append([
                school.school_name or '',
                school.from_year or '',
                school.to_year or ''
            ])

        school_table = Table(school_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        school_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(school_table)
        story.append(Spacer(1, 0.3 * inch))

    results = application.ssce_results.all()
    if results.exists():
        story.append(Paragraph("SECTION C: SSCE RESULTS", heading_style))
        for result in results:
            result_heading = Paragraph(
                f"<b>{result.get_exam_type_display()} - {result.year}</b>",
                styles['Normal']
            )
            story.append(result_heading)
            story.append(Spacer(1, 0.1 * inch))

            result_info = [
                ['Exam Number:', result.exam_number or ''],
                ['Centre Number:', result.centre_number or ''],
                ['Centre Name:', result.centre_name or ''],
            ]

            if result.awaiting_result:
                result_info.append(['Status:', 'Awaiting Result'])

            result_table = Table(result_info, colWidths=[2*inch, 4*inch])
            result_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(result_table)
            story.append(Spacer(1, 0.1 * inch))

            if not result.awaiting_result:
                grades_data = [['Subject', 'Grade']]
                grades_data.extend([
                    ['English', result.english or ''],
                    ['Mathematics', result.mathematics or ''],
                    ['Biology', result.biology or ''],
                    ['Chemistry', result.chemistry or ''],
                    ['Physics', result.physics or ''],
                ])

                if result.subject_6:
                    grades_data.append([result.subject_6, result.grade_6 or ''])
                if result.subject_7:
                    grades_data.append([result.subject_7, result.grade_7 or ''])
                if result.subject_8:
                    grades_data.append([result.subject_8, result.grade_8 or ''])
                if result.subject_9:
                    grades_data.append([result.subject_9, result.grade_9 or ''])

                grades_table = Table(grades_data, colWidths=[4*inch, 2*inch])
                grades_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]))
                story.append(grades_table)

            story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("SECTION D: COURSE SELECTION", heading_style))
    course_data = [
        ['First Choice:', application.get_first_choice_display() if application.first_choice else ''],
        ['Second Choice:', application.get_second_choice_display() if application.second_choice else ''],
    ]

    course_table = Table(course_data, colWidths=[2*inch, 4*inch])
    course_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(course_table)
    story.append(Spacer(1, 0.3 * inch))

    if application.declaration_text:
        story.append(Paragraph("SECTION E: DECLARATION", heading_style))
        declaration = Paragraph(application.declaration_text, styles['Normal'])
        story.append(declaration)
        story.append(Spacer(1, 0.3 * inch))

    story.append(Spacer(1, 0.5 * inch))
    footer_text = Paragraph(
        f"<i>Application submitted on: {application.submitted_at.strftime('%B %d, %Y') if application.submitted_at else 'Not yet submitted'}</i>",
        styles['Normal']
    )
    story.append(footer_text)

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
