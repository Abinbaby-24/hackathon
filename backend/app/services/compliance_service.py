def check_compliance(product_data):
    checks = []
    violations = []

    # MRP
    if product_data.get("mrp"):
        checks.append({
            "field": "mrp",
            "status": "PASS",
            "message": "MRP detected"
        })
    else:
        checks.append({
            "field": "mrp",
            "status": "FAIL",
            "message": "MRP not detected"
        })

        violations.append({
            "type": "MISSING_DECLARATION",
            "severity": "HIGH",
            "field": "mrp",
            "message": "MRP not detected"
        })

    # Manufacturer
    if product_data.get("manufacturer"):
        checks.append({
            "field": "manufacturer",
            "status": "PASS",
            "message": "Manufacturer detected"
        })
    else:
        checks.append({
            "field": "manufacturer",
            "status": "FAIL",
            "message": "Manufacturer not detected"
        })

        violations.append({
            "type": "MISSING_DECLARATION",
            "severity": "HIGH",
            "field": "manufacturer",
            "message": "Manufacturer not detected"
        })

    # Net quantity
    if product_data.get("net_quantity"):
        checks.append({
            "field": "net_quantity",
            "status": "PASS",
            "message": "Net quantity detected"
        })
    else:
        checks.append({
            "field": "net_quantity",
            "status": "FAIL",
            "message": "Net quantity not detected"
        })

    # Consumer care
    if product_data.get("consumer_care"):
        checks.append({
            "field": "consumer_care",
            "status": "PASS",
            "message": "Consumer-care information detected"
        })
    else:
        checks.append({
            "field": "consumer_care",
            "status": "FAIL",
            "message": "Consumer-care information not detected"
        })

        violations.append({
            "type": "MISSING_DECLARATION",
            "severity": "HIGH",
            "field": "consumer_care",
            "message": "Consumer-care information not detected"
        })

    # Simple MVP score
    passed = sum(
        1 for check in checks
        if check["status"] == "PASS"
    )

    score = round((passed / len(checks)) * 100) if checks else 0

    if violations:
        status = "REVIEW_REQUIRED"
    else:
        status = "COMPLIANT"

    return {
        "score": score,
        "status": status,
        "checks": checks,
        "violations": violations
    }