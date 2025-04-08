

# import json
# import numpy as np
# import matplotlib.pyplot as plt
# from io import BytesIO
# from typing import Dict, List, Any
# from reportlab.lib import colors
# from reportlab.lib.pagesizes import A4
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import (
#     SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image,
#     Table
# )
# from reportlab.platypus.tables import TableStyle

# def create_introduction_section(student_id: str) -> List[Any]:
#     """Create the introduction section of the report.

#     Args:
#         student_id (str): The student's ID number

#     Returns:
#         List[Any]: List of flowable elements for the PDF
#     """
#     styles = getSampleStyleSheet()
#     custom_style = ParagraphStyle(
#         'CustomStyle',
#         parent=styles['Normal'],
#         spaceBefore=12,
#         spaceAfter=12,
#         leading=16
#     )

#     # Create elements list
#     elements = []

#     # Add student ID
#     student_id_text = Paragraph(
#         f"Student's ID: {student_id}", styles['Heading1']
#     )
#     elements.append(student_id_text)
#     elements.append(Spacer(1, 12))

#     # Add Introduction heading
#     intro_heading = Paragraph("Introduction", styles['Heading2'])
#     elements.append(intro_heading)
#     elements.append(Spacer(1, 12))

#     # Add introduction text
#     intro_text = Paragraph(
#         ("To help you interpret the information and tables of data in this "
#          "feedback please note:"),
#         custom_style
#     )
#     elements.append(intro_text)
#     # Add bullet points
#     bullet_points = [
#         "The score is the number of correct answers you achieved at SBAs.",
#         ("All scores were then converted into Action University's Generic Marking "
#          "Scale (AUGMS) for undergraduate programmes, with pass-mark fixed at 35.50%."),
#         ("A pass-score was determined by means of a standard setting methodology, "
#          "equivalent to the 35.50% pass-mark in AUGMS. So to find out if you have "
#          "achieved a pass, please check if your overall mark is equal to or over "
#          "35.50%."),
#         ("It may help you understand what question format (SBA) you need to work at "
#          "further, by looking at your raw scores for each format. However, please "
#          "note that in this exam there is considerable compensation across question "
#          "formats, and in any one exam you will only need to achieve an overall "
#          "pass for question formats combined."),
#         ("You will also want to look at your performance in each domain: since this "
#          "gives some idea of your relative strengths. However, when the total number "
#          "of questions in each domain is low, this will not be very accurate, so "
#          "please use this information as a guide only."),
#         ("When you have low scores in a number of domains it usually means you need "
#          "to study all domains more thoroughly - this is an important take-home "
#          "message.")
#     ]

#     bullet_list = ListFlowable(
#         [ListItem(Paragraph(point, custom_style)) for point in bullet_points],
#         bulletType='bullet',
#         start='bulletchar',
#         bulletFontSize=8,
#         leftIndent=20,
#         bulletOffsetY=2
#     )
#     elements.append(bullet_list)

#     return elements

# def create_performance_chart(overall_scores: Dict[str, float]) -> BytesIO:
#     """Create a bell curve performance chart.

#     Args:
#         overall_scores (Dict[str, float]): Dictionary containing overall score statistics
    
#     Returns:
#         BytesIO: The chart image data
#     """
#     # Create bell curve data
#     x = np.linspace(0, 100, 100)
#     mu = overall_scores['mean']  # Mean of the distribution
#     sigma = overall_scores['stdev']  # Standard deviation
#     y = ((1/(sigma * np.sqrt(2 * np.pi))) * 
#         np.exp(-(x - mu)**2 / (2 * sigma**2)))

#     # Create the plot
#     plt.figure(figsize=(8, 6))
#     plt.plot(x, y, 'k-', linewidth=1)

#     # Add pass mark line
#     plt.axvline(x=35.5, color='gray', linestyle='--', linewidth=1)
#     plt.text(36, plt.ylim()[1], 'Pass-mark = 35.50%', rotation=0)

#     # Add your mark line and text
#     your_mark = overall_scores['your_score']
#     plt.axvline(x=your_mark, color='black', linestyle='-', linewidth=1)
#     plt.text(your_mark + 1, plt.ylim()[1] * 0.95, 
#             f'Your mark\n{your_mark:.1f}', rotation=0)

#     # Customize the plot
#     plt.xlabel('Overall Percentage Marks')
#     plt.ylabel('Density Function')
#     plt.grid(True, alpha=0.3)
#     plt.title('Your Performance')

#     # Save plot to memory
#     img_data = BytesIO()
#     plt.savefig(img_data, format='png', dpi=300, bbox_inches='tight')
#     plt.close()
#     img_data.seek(0)

#     return img_data

# def create_performance_section(json_data: Dict[str, Any]) -> List[Any]:
#     """Create the performance section of the report.

#     Args:
#         json_data (Dict[str, Any]): The student's data
    
#     Returns:
#         List[Any]: List of flowable elements for the PDF
#     """

#     styles = getSampleStyleSheet()
#     custom_style = ParagraphStyle(
#         'CustomStyle',
#         parent=styles['Normal'],
#         spaceBefore=12,
#         spaceAfter=12,
#         leading=16
#     )

#     elements = []

#     # Add section title
#     title = Paragraph("Performance", styles['Heading1'])
#     elements.append(title)
#     elements.append(Spacer(1, 12))

#     # Add summary text
#     summary_text = Paragraph(
#         "Your summary of results (RAW SCORES)\n\n"
#         "The table below summarises your SCORES for the overall exam (%). SBAs. The "
#         "class min, max, mean and standard deviation of scores are also displayed.",
#         custom_style
#     )
#     elements.append(summary_text)
#     elements.append(Spacer(1, 12))

#     # Create summary results table
#     table_style = TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 10),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ])

#     # Create summary table header
#     summary_header = [
#         'Exam component', 'Your score', 'Total Available', 'Min', 'Max', 'Mean', 'StDev'
#     ]

#     # Create summary table rows
#     summary_rows = []
#     for result in json_data['summary_results']:
#         summary_rows.append([
#             result['component'],
#             f"{result['your_score']:.1f}",
#             str(result['total_available']),
#             f"{result['min']:.1f}",
#             f"{result['max']:.1f}",
#             f"{result['mean']:.1f}",
#             f"{result['stdev']:.2f}"
#         ])

#     # Create and style the summary table
#     summary_table = Table([summary_header] + summary_rows)
#     summary_table.setStyle(table_style)
#     elements.append(summary_table)
#     elements.append(Spacer(1, 24))

#     # Add chart title
#     chart_title = Paragraph("Your overall performance (MARKS)", styles['Heading2'])
#     elements.append(chart_title)
#     elements.append(Spacer(1, 12))

#     # Add chart description
#     desc = Paragraph(
#         "The graph below shows your maximum percentage MARK for all "
#         "question formats combined and the overall pass-mark fixed at "
#         "35.50% (rounded to 40% and equivalent to the overall pass-score "
#         "obtained via the Angoff standard setting method, equal to 55.8 "
#         "out of 100).",
#         custom_style
#     )
#     elements.append(desc)
#     elements.append(Spacer(1, 12))

#     # Get overall scores for chart
#     overall_scores = next(
#         (item for item in json_data['summary_results']
#          if item['component'] == 'Overall Scores'),
#         {'your_score': 0, 'mean': 70, 'stdev': 10}
#     )

#     # Create and add the performance chart
#     chart_data = create_performance_chart(overall_scores)
#     chart = Image(chart_data, width=400, height=300)
#     elements.append(chart)
#     elements.append(Spacer(1, 12))

#     # Add outcome text
#     outcome_text = Paragraph(
#         f"<i>Your Overall Outcome at the Current Exam: {json_data['overall_outcome']}</i>",
#         custom_style
#     )
#     elements.append(outcome_text)
#     elements.append(Spacer(1, 12))

#     # Create mark ranges table
#     grade_table_data = [
#         ['Mark Range (Lower\nBound)', 'Mark Range (Upper\nBound)', 'Descriptor', 'Grade'],
#         ['69.50%', '>', 'Excellent Pass', 'A'],
#         ['59.50%', '69.49%', 'Very Good Pass', 'B'],
#         ['49.50%', '59.49%', 'Good Pass', 'C'],
#         ['44.50%', '49.49%', 'Pass', 'D1'],
#         ['39.50%', '44.49%', 'Borderline Pass', 'D2'],
#         ['<', '39.49%', 'NOT Pass', 'E']
#     ]

#     grade_table = Table(grade_table_data)
#     grade_table.setStyle(table_style)
#     elements.append(grade_table)
#     elements.append(Spacer(1, 12))

#     # Add explanatory note
#     note_text = (
#         "Please note: If your outcome was Borderline Pass, that means that you "
#         "have passed the current exam, but it should draw your attention to how "
#         "close your performance was to the pass-score. Grades and Descriptors "
#         "listed are indicative purposes only. Please note your end of year "
#         "transcript for summative grades will only list marks and decisions."
#     )
#     note = Paragraph(note_text, custom_style)
#     elements.append(note)
#     elements.append(Spacer(1, 24))

#     return elements

# def generate_student_report(
#     json_data: Dict[str, Any], output_filename: str
# ) -> None:
#     """Generate a PDF report for a student.

#     Args:
#         json_data (Dict[str, Any]): The student's data
#         output_filename (str): The name of the output PDF file
#     """
#     # Create the PDF document
#     doc = SimpleDocTemplate(
#         output_filename,
#         pagesize=A4,
#         rightMargin=72,
#         leftMargin=72,
#         topMargin=72,
#         bottomMargin=72
#     )

#     # Create the elements list
#     elements = []

#     # Add introduction section
#     elements.extend(create_introduction_section(str(json_data['student_id'])))

#     # Add performance section
#     elements.extend(create_performance_section(json_data))

#     # Add domain analysis section
#     elements.extend(create_domain_analysis_section(json_data))

#     # Add decile ranking section
#     elements.extend(create_decile_section(json_data))

#     # Build the PDF
#     doc.build(elements)


# def create_domain_analysis_section(json_data: Dict[str, Any]) -> List[Any]:
#     """Create the domain analysis section of the report.

#     Args:
#         json_data (Dict[str, Any]): The student's data

#     Returns:
#         List[Any]: List of flowable elements for the PDF
#     """
#     styles = getSampleStyleSheet()
#     custom_style = ParagraphStyle(
#         'CustomStyle',
#         parent=styles['Normal'],
#         spaceBefore=12,
#         spaceAfter=12,
#         leading=16
#     )

#     elements = []

#     # Add section title
#     title = Paragraph("Your summary of results (RAW SCORES)", styles['Heading1'])
#     elements.append(title)
#     elements.append(Spacer(1, 12))

#     # Add introduction text
#     intro_text = Paragraph(
#         "The table below summarises your SCORES for the overall exam (%). SBAs. The "
#         "class min, max, mean and standard deviation of scores are also displayed.",
#         custom_style
#     )
#     elements.append(intro_text)
#     elements.append(Spacer(1, 12))

#     # Create summary table
#     table_style = TableStyle([
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('FONTSIZE', (0, 0), (-1, 0), 10),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ])

#     # Create table header
#     table_data = [
#         ['Exam component', 'Your score', 'Total Available', 'Min', 'Max', 'Mean', 'StDev']
#     ]

#     # Add data rows for each component
#     for result in json_data['summary_results']:
#         table_data.append([
#             result['component'],
#             f"{result['your_score']:.0f}",
#             "100",
#             f"{result['min']:.0f}",
#             f"{result['max']:.0f}",
#             f"{result['mean']:.2f}",
#             f"{result['stdev']:.2f}"
#         ])

#     # Create and style the table
#     summary_table = Table(table_data)
#     summary_table.setStyle(table_style)
#     elements.append(summary_table)
#     elements.append(Spacer(1, 24))

#     # Add recommendations
#     recommendations = []
#     for result in json_data['summary_results']:
#         score = result['your_score']
#         avg = result['mean']
#         if score <= avg - result['stdev']:
#             recommendations.append(
#                 f"• {result['component']}: Consider focusing more on this "
#                 f"component as your score ({score:.0f}%) is below the class "
#                 f"average ({avg:.2f}%)."
#             )

#     if recommendations:
#         rec_title = Paragraph("Recommendations", styles['Heading2'])
#         elements.append(rec_title)
#         elements.append(Spacer(1, 12))

#         for rec in recommendations:
#             rec_text = Paragraph(rec, custom_style)
#             elements.append(rec_text)
#             elements.append(Spacer(1, 6))

#     return elements

# def create_decile_section(json_data: Dict[str, Any]) -> List[Any]:
#     """Create the decile ranking section of the report.

#     Args:
#         json_data (Dict[str, Any]): The student's data

#     Returns:
#         List[Any]: List of flowable elements for the PDF
#     """
#     styles = getSampleStyleSheet()
#     custom_style = ParagraphStyle(
#         'CustomStyle',
#         parent=styles['Normal'],
#         spaceBefore=12,
#         spaceAfter=12,
#         leading=16
#     )

#     elements = []

#     # Add section title
#     title = Paragraph("Decile ranking", styles['Heading1'])
#     elements.append(title)
#     elements.append(Spacer(1, 12))

#     # Add introduction text
#     intro_text = Paragraph(
#         "Your decile rank is reported below. This is a measure of your performance in "
#         "comparison to the performance of the other students who sat the exam.",
#         custom_style
#     )
#     elements.append(intro_text)
#     elements.append(Spacer(1, 12))

#     # Calculate decile based on overall score
#     overall_scores = next(
#         (item for item in json_data['summary_results']
#          if item['component'] == 'Overall Scores'),
#         None
#     )
#     if overall_scores:
#         score = overall_scores['your_score']
#         all_scores = []
#         # Get scores for all students
#         for result in json_data['summary_results']:
#             if result['component'] == 'Overall Scores':
#                 all_scores = [score for score in range(
#                     int(result['min']), 
#                     int(result['max']) + 1
#                 )]
#                 break
        
#         # Calculate decile
#         all_scores.sort()
#         position = sum(1 for s in all_scores if s <= score)
#         decile = ((len(all_scores) - position) // (len(all_scores) // 10)) + 1
        
#         # Function to get the ordinal suffix
#         def get_ordinal_suffix(decile):
#             if decile == 1:
#                 return "st"
#             elif decile == 2:
#                 return "nd"
#             elif decile == 3:
#                 return "rd"
#             else:
#                 return "th"
        
#         # Determine the ordinal suffix
#         ordinal_suffix = get_ordinal_suffix(decile)
        
#         # Add decile text
#         decile_text = Paragraph(
#             f"You are in the {decile}{ordinal_suffix} decile.",
#             ParagraphStyle(
#                 'DecileStyle',
#                 parent=styles['Normal'],
#                 fontSize=14,
#                 alignment=1,  # Center alignment
#                 spaceAfter=12
#             )
#         )
#         elements.append(decile_text)
#         elements.append(Spacer(1, 12))

#     # Add interpretation text
#     elements.append(Paragraph("How to interpret your rank:", custom_style))
#     elements.append(Spacer(1, 6))

#     # Add decile explanations
#     decile_explanations = [
#         "If you are in the 1st decile, then you are in the top 10% of the cohort.",
#         "If you are in the 2nd decile, then you are in the top 20% of the cohort.",
#         "If you are in the 3rd decile, then you are in the top 30% of the cohort.",
#         "If you are in the 4th decile, then you are in the top 40% of the cohort.",
#         "If you are in the 5th decile, then you are in the top 50% of the cohort.",
#         "If you are in the 6th decile, then you are in the bottom 50% of the cohort.",
#         "If you are in the 7th decile, then you are in the bottom 40% of the cohort.",
#         "If you are in the 8th decile, then you are in the bottom 30% of the cohort.",
#         "If you are in the 9th decile, then you are in the bottom 20% of the cohort.",
#         "If you are in the 10th decile, then you are in the bottom 10% of the cohort."
#     ]

#     bullet_list = ListFlowable(
#         [ListItem(Paragraph(point, custom_style)) for point in decile_explanations],
#         bulletType='bullet',
#         start='bulletchar',
#         bulletFontSize=8,
#         leftIndent=20,
#         bulletOffsetY=2
#     )
#     elements.append(bullet_list)

#     elements.append(Spacer(1, 12))

#     # Add disclaimer text
#     elements.append(Paragraph("In reading this information, please bear in mind:", custom_style))
#     elements.append(Spacer(1, 6))

#     disclaimers = [
#         "The decile rank here presented does NOT imply any pass / fail decision nor "
#         "does it correspond to any prize or merit.",
#         "This decile rank does NOT translate directly into the ranking for the UK "
#         "Foundation Programme, the latter being the result of weighting across all "
#         "summative exams in the MBChB, from Year 1 to Year 5.",
#         "Students may leave or join your cohort later in the programme, and this could "
#         "shift the final ranking for the UK Foundation Programme."
#     ]

#     disclaimer_list = ListFlowable(
#         [ListItem(Paragraph(point, custom_style)) for point in disclaimers],
#         bulletType='bullet',
#         start='bulletchar',
#         bulletFontSize=8,
#         leftIndent=20,
#         bulletOffsetY=2
#     )
#     elements.append(disclaimer_list)

#     elements.append(Spacer(1, 12))

#     # Add final note
#     final_note = Paragraph(
#         "For all the reasons listed above, please only use this information formatively, aiming "
#         "to inform and improve your future learning.",
#         custom_style
#     )
#     elements.append(final_note)
#     elements.append(Spacer(1, 24))

#     return elements

# def process_student_data(raw_data: List[Dict[str, Any]], student_id: int) -> Dict[str, Any]:
#     """Process raw student data to generate summary statistics by itemGroupCode.

#     Args:
#         raw_data (List[Dict[str, Any]]): Raw data from JSON file
#         student_id (int): ID of the student to process
    
#     Returns:
#         Dict[str, Any]: Processed student data with summary statistics
#     """
#     # Filter data for the specific student
#     student_responses = [item for item in raw_data if item['studentId'] == student_id]

#     if not student_responses:
#         raise ValueError(f"No data found for student {student_id}")

#     # Get all unique itemGroupCodes
#     group_codes = {item['itemGroupCode'] for item in raw_data}

#     # Initialize summary results
#     summary_results = []
#     student_total_correct = 0
#     student_total_responses = 0

#     # Process each itemGroupCode
#     for group in group_codes:
#         # Get student's responses for this group
#         student_group_responses = [
#             item for item in student_responses 
#             if item['itemGroupCode'] == group
#         ]
    
#         if student_group_responses:
#             # Calculate student's score for this group
#             group_correct = sum(
#                 1 for item in student_group_responses 
#                 if item['responseValue'] > 0
#             )
#             group_total = len(student_group_responses)
#             student_score = (group_correct / group_total) * 100
        
#             # Update overall totals
#             student_total_correct += group_correct
#             student_total_responses += group_total
        
#             # Get all students' scores for this group
#             group_scores = []
#             for sid in {item['studentId'] for item in raw_data}:
#                 responses = [
#                     item for item in raw_data 
#                     if item['studentId'] == sid 
#                     and item['itemGroupCode'] == group
#                 ]
#                 if responses:
#                     correct = sum(1 for r in responses if r['responseValue'] > 0)
#                     score = (correct / len(responses)) * 100
#                     group_scores.append(score)
        
#             # Calculate group statistics
#             summary_results.append({
#                 "component": group,
#                 "your_score": student_score,
#                 "total_available": 100,
#                 "min": min(group_scores),
#                 "max": max(group_scores),
#                 "mean": np.mean(group_scores),
#                 "stdev": np.std(group_scores)
#             })

#     # Calculate overall score and statistics
#     overall_score = (student_total_correct / student_total_responses) * 100

#     # Get overall scores for all students
#     all_scores = []
#     for sid in {item['studentId'] for item in raw_data}:
#         responses = [item for item in raw_data if item['studentId'] == sid]
#         if responses:
#             correct = sum(1 for r in responses if r['responseValue'] > 0)
#             score = (correct / len(responses)) * 100
#             all_scores.append(score)

#     # Add overall scores to summary
#     summary_results.insert(0, {
#         "component": "Overall Scores",
#         "your_score": overall_score,
#         "total_available": 100,
#         "min": min(all_scores),
#         "max": max(all_scores),
#         "mean": np.mean(all_scores),
#         "stdev": np.std(all_scores)
#     })

#     # Determine outcome based on overall score
#     if overall_score >= 69.50:
#         outcome = "Excellent Pass"
#     elif overall_score >= 59.50:
#         outcome = "Very Good Pass"
#     elif overall_score >= 49.50:
#         outcome = "Good Pass"
#     elif overall_score >= 44.50:
#         outcome = "Pass"
#     elif overall_score >= 39.50:
#         outcome = "Borderline Pass"
#     else:
#         outcome = "NOT Pass"

#     return {
#         "student_id": str(student_id),
#         "overall_outcome": outcome,
#         "summary_results": summary_results
#     }

# if __name__ == "__main__":
#     # Load and process data for one student
#     with open('jsData.json', 'r') as f:
#         raw_data = json.load(f)

#     # Process first student's data
#     first_student_id = raw_data[0]['studentId']
#     processed_data = process_student_data(raw_data, first_student_id)

#     # Generate the report
#     generate_student_report(processed_data, "student_report.pdf")
#     print("Report generated successfully as student_report.pdf")
