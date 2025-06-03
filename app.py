from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import tempfile
import os
import json
from io import BytesIO
from student_report import process_student_data, generate_student_report


app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route("/")
def home():
    return "<p>BOE Report Generator Service</p>"


def generate_pdf_report(json_data, output_file=None):
    """Wrapper function that handles the temporary file creation"""
    temp_output = None
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


@app.route("/generate_student_report/<student_id>", methods=["POST"])
def generate_student_report_endpoint(student_id):
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Process student data
        processed_data = process_student_data(data, student_id)

        # Create temporary file for the PDF
        temp_output = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        output_file = temp_output.name
        temp_output.close()

        # Generate PDF report
        generate_student_report(processed_data, output_file)

        # Read the generated PDF
        with open(output_file, 'rb') as f:
            pdf_data = f.read()

        # Clean up
        os.unlink(output_file)

        # Return the PDF
        pdf_buffer = BytesIO(pdf_data)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"student_report_{student_id}.pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)