# from flask import Flask, request, send_file, jsonify
# from flask_cors import CORS, cross_origin
# import pandas as pd
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import io
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.utils import simpleSplit
# from fastapi import FastAPI

# app = Flask(__name__) #FastAPI("Reporter") #
# CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST"], "allow_headers": ["Content-Type"]}})

# @app.route("/")
# def generateReport():
#     return "<p>Generating report</p>"


    
# def generate_pdf(json_data):
#     df = pd.DataFrame(json_data)
#     marks_df = df.groupby(['studentId'])['responseValue'].sum().reset_index()
#     marks_df = marks_df.rename(columns={'responseValue': 'Marks'})
    
#     total_possible = 140
#     marks_df['Percentage'] = (marks_df['Marks'] / total_possible) * 100

#     summed_df = df.groupby(['studentId', 'itemGroupCode'])['responseValue'].sum().reset_index()
#     summary_table = summed_df.groupby('itemGroupCode')['responseValue'].agg(
#         Min='min', Max='max', Mean='mean', StDev='std'
#     ).reset_index().fillna(0)

#     summary_table = summary_table.rename(columns={'itemGroupCode': 'Exam Component'})
#     summary_table['Total Available'] = total_possible
#     summary_table = summary_table[['Exam Component', 'Total Available', 'Min', 'Max', 'Mean', 'StDev']]

#     overall_stats = pd.DataFrame({
#         'Exam Component': ['Overall'],
#         'Total Available': [summary_table['Total Available'].sum()],
#         'Min': [marks_df['Marks'].min()],
#         'Max': [marks_df['Marks'].max()],
#         'Mean': [marks_df['Marks'].mean()],
#         'StDev': [marks_df['Marks'].std()]
#     }).fillna(0)

#     final_table = pd.concat([summary_table, overall_stats], ignore_index=True)

#     pdf_buffer = io.BytesIO()
#     c = canvas.Canvas(pdf_buffer, pagesize=A4)
#     width, height = A4
#     c.setFont("Helvetica-Bold", 14)
#     c.drawString(50, height - 50, "Exam Report")

#     c.setFont("Helvetica-Bold", 12)
#     c.drawString(50, height - 80, "Student Marks:")
#     c.setFont("Helvetica", 10)
#     y_pos = height - 100
#     for _, row in marks_df.iterrows():
#         c.drawString(50, y_pos, f"Student {int(row['studentId'])}: {row['Marks']} marks ({row['Percentage']:.2f}%)")
#         y_pos -= 15

#     c.setFont("Helvetica-Bold", 12)
#     y_pos -= 20
#     c.drawString(50, y_pos, "Table 1: Exam Component Statistics")
#     c.setFont("Helvetica", 10)
#     y_pos -= 20

#     for _, row in final_table.iterrows():
#         text = f"{row['Exam Component']}: Min {row['Min']}, Max {row['Max']}, Mean {row['Mean']:.2f}, StDev {row['StDev']:.2f}"
#         split_text = simpleSplit(text, "Helvetica", 10, width - 100)
#         for line in split_text:
#             c.drawString(50, y_pos, line)
#             y_pos -= 15
#         y_pos -= 5

#     c.save()
#     pdf_buffer.seek(0)
#     return pdf_buffer

# @app.route("/generate_report", methods=["POST"])
# def generate_report():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "No data provided"}), 400

#         pdf_buffer = generate_pdf(data)
#         return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name="student_report.pdf")
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)


# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pandas as pd
import tempfile
import os
import json
from io import BytesIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST"], "allow_headers": ["Content-Type"]}})

@app.route("/")
def home():
    return "<p>BOE Report Generator Service</p>"

def generate_pdf_report(json_data, output_file=None):
    """Wrapper function that handles the temporary file creation"""
    # Use a temporary file if no output file specified
    if output_file is None:
        temp_output = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        output_file = temp_output.name
        temp_output.close()
    
    # Convert JSON data to string if it's a dict
    if isinstance(json_data, dict):
        json_data = json.dumps(json_data)
    
    # Import the actual report generation function
    from report_generator import generate_boe_report
    generate_boe_report(json_data, output_file)
    
    # Read the generated PDF into memory
    with open(output_file, 'rb') as f:
        pdf_data = f.read()
    
    # Clean up the temporary file
    if temp_output:
        os.unlink(output_file)
    
    return BytesIO(pdf_data)

@app.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Generate PDF
        pdf_buffer = generate_pdf_report(data)
        
        # Return the PDF as a download
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name="boe_report.pdf"
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)