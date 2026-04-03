from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import io

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- GENERATE FANCY PDF ----------------
@app.route('/generate', methods=['POST'])
def generate_resume():
    data = request.get_json()

    name = data.get('name', '')
    skills = data.get('skills', '')
    experience = data.get('experience', '')
    education = data.get('education', '')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    # Custom Styles
    name_style = ParagraphStyle(
        'nameStyle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        spaceAfter=10
    )

    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    content = []

    # NAME (CENTER + BOLD)
    content.append(Paragraph(f"<b>{name}</b>", name_style))
    content.append(Spacer(1, 10))

    # LINE
    content.append(HRFlowable(width="100%"))
    content.append(Spacer(1, 15))

    # SKILLS
    content.append(Paragraph("<b>Skills</b>", heading_style))
    content.append(Spacer(1, 8))
    content.append(Paragraph(skills, normal_style))
    content.append(Spacer(1, 15))

    # EXPERIENCE
    content.append(Paragraph("<b>Experience</b>", heading_style))
    content.append(Spacer(1, 8))
    content.append(Paragraph(experience, normal_style))
    content.append(Spacer(1, 15))

    # EDUCATION
    content.append(Paragraph("<b>Education</b>", heading_style))
    content.append(Spacer(1, 8))
    content.append(Paragraph(education, normal_style))
    content.append(Spacer(1, 15))

    # BUILD PDF
    doc.build(content)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="resume.pdf",
        mimetype='application/pdf'
    )


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)