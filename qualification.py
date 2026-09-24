def qualify_lead(company_data,  target_keywords=None, max_employee=500):
    if target_keywords is None:
        target_keywords = ["technology", "software", "tech", "internet", "cloud"]

    score = 0
    reasons = []

    industry = company_data.get('industry', 'unknown')
    if industry != 'unknown' and any(kw in industry.lower() for kw in target_keywords):
        score += 30
        reasons.append(f"Industry match: {industry} (+30)")
    else:
        reasons.append(f"Industry did not match target '{target_keywords}' (+0)")

    employee_count = company_data.get('employee_count', 'unknown')
    if employee_count != 'unknown':
        try:
            count = int(str(employee_count).replace(',', ''))
            if count <= max_employee:
                score += 20
                reasons.append(f"Employee count {count} within target range (+20)")
            else:
                reasons.append(f"Employee count '{employee_count}' exceeds target range (+0)")
        except ValueError:
            reasons.append("Employee count unknown (+0)")
    else:
        reasons.append("Employee count unknown (+0)")

    ## add more rules to identify the better lead

    status = 'qualified' if score >= 30 else 'unqualified'

    return {
        'score': score,
        'status': status,
        'reasons': reasons
        }