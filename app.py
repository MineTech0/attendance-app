from flask import Flask, render_template, request, send_file
import pandas as pd
from fpdf import FPDF
from datetime import datetime, timedelta
import os

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Läsnäololista', 0, 1, 'C')
        
    def footer(self):
        #add generated date
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Tulostettu: {datetime.now().strftime("%d.%m.%Y %H:%M")}', 0, 0, 'C')

def create_attendance_list(course_name, start_date, end_date, participants):
    pdf = PDF('P', 'mm', 'A4')  # Portrait orientation, millimeters, A4 size
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f'{course_name}', 0, 1, 'C')
    pdf.ln(5)
    
    # Generate dates for the course
    current_date = start_date
    course_dates = []
    while current_date <= end_date:
        course_dates.append(current_date)
        current_date += timedelta(weeks=1)

    # Calculate the width of each column
    col_width = (210 - 50) / (len(course_dates) + 1)  # A4 width is 210mm, leaving space for the participant column

    # Calculate the height of each row and font size
    row_height = 10
    max_rows = int((297 - 50 - 30) / row_height)  # A4 height is 297mm, leaving some space for margins and headers

    if len(participants) > max_rows:
        row_height = (297 - 50 - 30) / len(participants)  # Adjust row height to fit all participants

    # Adjust font size based on row height
    font_size = max(8, int(row_height - 2))  # Ensure font size is not too small

    # Table header
    pdf.set_font('Arial', 'B', font_size)
    pdf.cell(50, row_height, 'Osallistuja', 1)
    for date in course_dates:
        pdf.cell(col_width, row_height, date.strftime("%d.%m"), 1)
    pdf.ln()

    # Table body
    pdf.set_font('Arial', '', 10)
    for participant in participants:
        pdf.cell(50, row_height, participant, 1)
        for _ in course_dates:
            pdf.cell(col_width, row_height, '', 1)  # Empty cell for checkmark
        pdf.ln()

    name = f"{course_name}_läsnäololista.pdf"
    output_path = os.path.join('static', name)
    pdf.output(output_path)
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        course_name = request.form['course_name']
        start_date = datetime.strptime(request.form['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(request.form['end_date'], "%Y-%m-%d")
        
        participants_file = request.files['participants_file']
        participants_df = pd.read_csv(participants_file)
        participants = participants_df['name'].tolist()
        participants.sort()
        
        pdf_path = create_attendance_list(course_name, start_date, end_date, participants)
        return send_file(pdf_path, as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
