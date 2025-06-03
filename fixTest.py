def process_student_data(raw_data: List[Dict[str, Any]], student_id: str) -> Dict[str, Any]:
    """Process raw student data to generate summary statistics by itemGroupCode.

    Args:
        raw_data (List[Dict[str, Any]]): Raw data from JSON file
        student_id (str): ID of the student to process
    
    Returns:
        Dict[str, Any]: Processed student data with summary statistics
    """
    # Filter data for the specific student
    student_responses = [item for item in raw_data if int(item['studentId']) == int(student_id)]
    
    if not student_responses:
        raise ValueError(f"No data found for student {student_id}")

    # Get all unique itemGroupCodes
    group_codes = {item['itemGroupCode'] for item in raw_data}
    print(f"Found group codes: {group_codes}")  # Debug log

    # Initialize summary results
    summary_results = []
    student_total_correct = 0
    student_total_responses = 0

    # Process each itemGroupCode
    for group in group_codes:
        # Get student's responses for this group
        student_group_responses = [
            item for item in student_responses 
            if item['itemGroupCode'] == group
        ]
        
        print(f"Processing group {group} with {len(student_group_responses)} responses")  # Debug log
    
        if student_group_responses:
            # Calculate student's score for this group
            group_score = sum(item['responseValue'] for item in student_group_responses)
            group_total = len(student_group_responses)
            
            if group_total == 0:  # Prevent division by zero
                print(f"Warning: No responses found for group {group}")
                continue
                
            student_score = (group_score / group_total) * 100
            print(f"Group {group} - Score: {group_score}, Total: {group_total}, Percentage: {student_score}")  # Debug log
        
            # Update overall totals
            student_total_correct += group_score
            student_total_responses += group_total
        
            # Get all students' scores for this group
            group_scores = []
            for sid in {item['studentId'] for item in raw_data}:
                responses = [
                    item for item in raw_data 
                    if item['studentId'] == sid 
                    and item['itemGroupCode'] == group
                ]
                if responses:
                    score = sum(r['responseValue'] for r in responses)
                    if len(responses) > 0:  # Prevent division by zero
                        avg_score = (score / len(responses)) * 100
                        group_scores.append(avg_score)
            
            if group_scores:  # Only add if we have scores
                summary_results.append({
                    "component": group,
                    "your_score": student_score,
                    "total_available": 100,
                    "min": min(group_scores),
                    "max": max(group_scores),
                    "mean": np.mean(group_scores),
                    "stdev": np.std(group_scores) if len(group_scores) > 1 else 0
                })

    # Calculate overall score and statistics
    if student_total_responses > 0:  # Prevent division by zero
        overall_score = (student_total_correct / student_total_responses) * 100
        print(f"Overall - Score: {student_total_correct}, Total: {student_total_responses}, Percentage: {overall_score}")  # Debug log

        # Get overall scores for all students
        all_scores = []
        for sid in {item['studentId'] for item in raw_data}:
            responses = [item for item in raw_data if item['studentId'] == sid]
            if responses:
                score = sum(r['responseValue'] for r in responses)
                if len(responses) > 0:  # Prevent division by zero
                    avg_score = (score / len(responses)) * 100
                    all_scores.append(avg_score)

        if all_scores:  # Only add if we have scores
            summary_results.insert(0, {
                "component": "Overall Scores",
                "your_score": overall_score,
                "total_available": 100,
                "min": min(all_scores),
                "max": max(all_scores),
                "mean": np.mean(all_scores),
                "stdev": np.std(all_scores) if len(all_scores) > 1 else 0
            })

            # Determine outcome based on overall score
            if overall_score >= 69.50:
                outcome = "Excellent Pass"
            elif overall_score >= 59.50:
                outcome = "Very Good Pass"
            elif overall_score >= 49.50:
                outcome = "Good Pass"
            elif overall_score >= 44.50:
                outcome = "Pass"
            elif overall_score >= 39.50:
                outcome = "Borderline Pass"
            else:
                outcome = "NOT Pass"
        else:
            outcome = "Insufficient Data"
    else:
        outcome = "No Responses"
        summary_results.insert(0, {
            "component": "Overall Scores",
            "your_score": 0,
            "total_available": 100,
            "min": 0,
            "max": 0,
            "mean": 0,
            "stdev": 0
        })

    return {
        "student_id": str(student_id),
        "overall_outcome": outcome,
        "summary_results": summary_results
    }