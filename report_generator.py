import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from io import BytesIO
import tempfile
import os
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generate_boe_report(json_data, output_file="BOE_Report.pdf"):
    """
    Generate a comprehensive BOE report PDF from JSON data.
    
    Args:
        json_data: Input data as JSON string or Python dict
        output_file: Path to save the PDF report
    """
    # Convert JSON to DataFrame
    if isinstance(json_data, str):
        data = json.loads(json_data)
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame(json_data)
    
    # 1. Calculate each student's total marks
    marks_df = df.groupby(['studentId'])['responseValue'].sum().reset_index()
    marks_df = marks_df.rename(columns={'responseValue': 'Marks'})
    
    # Define total possible marks
    total_possible = 140
    marks_df['Percentage'] = (marks_df['Marks'] / total_possible) * 100
    
    # 2. Create the histogram visualization with matching fonts
    plt.style.use('seaborn-v0_8')
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': 'Helvetica',
        'axes.titlesize': 16,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10
    })
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(marks_df['Percentage'], bins=20, kde=False, 
                 stat='density', alpha=0.5, color='skyblue', 
                 edgecolor='black', ax=ax)
    sns.kdeplot(marks_df['Percentage'], color='darkblue', linewidth=2, ax=ax)
    
    ax.set_title('Overall Performance', pad=20, fontweight='bold')
    ax.set_xlabel('Overall Percentage Marks', fontweight='bold')
    ax.set_ylabel('Density Function', fontweight='bold')
    ax.set_xlim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Save the plot to a temporary file
    temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(temp_img.name, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Generate the exam component statistics table
    summed_df = df.groupby(['studentId', 'itemGroupCode'])['responseValue'].sum().reset_index()
    summary_table = summed_df.groupby('itemGroupCode')['responseValue'].agg(
        Min='min',
        Max='max',
        Mean='mean',
        StDev='std'
    ).reset_index().fillna(0)
    
    summary_table = summary_table.rename(columns={'itemGroupCode': 'Exam Component'})
    summary_table['Total Available'] = total_possible
    summary_table = summary_table[['Exam Component', 'Total Available', 'Min', 'Max', 'Mean', 'StDev']].round(2)
    
    overall_stats = pd.DataFrame({
        'Exam Component': ['Overall'],
        'Total Available': [summary_table['Total Available'].sum()], 
        'Min': [marks_df['Marks'].min()],
        'Max': [marks_df['Marks'].max()],
        'Mean': [marks_df['Marks'].mean()],
        'StDev': [marks_df['Marks'].std()]
    }).fillna(0).round(2)
    
    final_table = pd.concat([summary_table, overall_stats], ignore_index=True)
    
    # 4. Generate subgroup statistics for each item group
    group_codes = df['itemGroupCode'].unique()
    subgroup_tables = []
    
    for group_code in group_codes:
        group_df = df[df['itemGroupCode'] == group_code]
        summed_df = group_df.groupby(['studentId', 'itemSubGroupName'])['responseValue'].sum().reset_index()
        
        summary_table = summed_df.groupby('itemSubGroupName')['responseValue'].agg(
            Min='min',
            Max='max',
            Mean='mean',
            StDev='std'
        ).reset_index().fillna(0).round(2)
        
        summary_table = summary_table.rename(columns={'itemSubGroupName': 'Block'})
        summary_table['Total'] = total_possible
        summary_table = summary_table[['Block', 'Total', 'Min', 'Max', 'Mean', 'StDev']]
        
        # Calculate overall stats for this group
        overall_min = summed_df['responseValue'].min()
        overall_max = summed_df['responseValue'].max()
        overall_mean = summed_df['responseValue'].mean()
        overall_std = summed_df['responseValue'].std()
        
        subgroup_tables.append({
            'group_code': group_code,
            'table': summary_table,
            'overall_stats': {
                'Min': overall_min,
                'Max': overall_max,
                'Mean': overall_mean,
                'StDev': overall_std
            }
        })
    
    # Generate PDF Report
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 50, "B.O.E Report")
    
    # Add the histogram image to PDF
    c.drawImage(temp_img.name, 50, height - 350, width=500, height=250)
    
    # Current y position for content
    y_pos = height - 400
    
    # 5. Add the exam component statistics table
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, "Exam Component Statistics:")
    y_pos -= 20
    
    # Create data for the table
    table_data = [final_table.columns.tolist()] + final_table.values.tolist()
    
    # Create and style the table
    exam_table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    exam_table.setStyle(style)
    
    # Draw the table on the canvas
    exam_table.wrapOn(c, width - 100, height)
    exam_table.drawOn(c, 50, y_pos - (len(table_data) * 20))
    
    # Update y_pos for remaining content
    y_pos = y_pos - (len(table_data) * 20) - 30
    
    # 6. Add subgroup statistics tables for each item group
    for group_data in subgroup_tables:
        # Check if we need a new page
        if y_pos < 150:  # Leave room for next section
            c.showPage()
            y_pos = height - 50
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width/2, height - 50, "B.O.E Report(cont.)")
            y_pos = height - 80
        
        # Add group header
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_pos, f"Statistics for Item Group: {group_data['group_code']}")
        y_pos -= 20
        
        # Create data for subgroup table
        table_data = [group_data['table'].columns.tolist()] + group_data['table'].values.tolist()
        
        # Create and style the table
        subgroup_table = Table(table_data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        subgroup_table.setStyle(style)
        
        # Draw the table on the canvas
        subgroup_table.wrapOn(c, width - 100, height)
        subgroup_table.drawOn(c, 50, y_pos - (len(table_data) * 20))
        
        # Update y_pos
        y_pos = y_pos - (len(table_data) * 20) - 20
        
        # Add overall stats for this group
        stats = group_data['overall_stats']
        c.setFont("Helvetica", 10)
        c.drawString(50, y_pos, 
                    f"Overall: Min: {stats['Min']:.2f} | Max: {stats['Max']:.2f} | " +
                    f"Mean: {stats['Mean']:.2f} | Std Dev: {stats['StDev']:.2f}")
        y_pos -= 30
    
    # 7. Add Student Marks Summary at the end
    # Check if we need a new page
    if y_pos < 100:
        c.showPage()
        y_pos = height - 50
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height - 50, "B.O.E Report(cont.)")
        y_pos = height - 80
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, "Student Marks Summary:")
    c.setFont("Helvetica", 10)
    y_pos -= 20
    
    stats_text = [
        f"Number of Students: {len(marks_df)}",
        f"Average Marks: {marks_df['Marks'].mean():.1f}",
        f"Average Percentage: {marks_df['Percentage'].mean():.1f}%",
        f"Highest Score: {marks_df['Marks'].max()}",
        f"Lowest Score: {marks_df['Marks'].min()}"
    ]
    
    for text in stats_text:
        c.drawString(50, y_pos, text)
        y_pos -= 20
    
    # Clean up and save PDF
    c.save()
    temp_img.close()
    os.unlink(temp_img.name)
    print(f"Report generated successfully at {output_file}")

