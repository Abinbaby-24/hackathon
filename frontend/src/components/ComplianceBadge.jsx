function ComplianceBadge({ status }) {

  const normalizedStatus = status || "UNKNOWN";

  let className = "status-unknown";
  let label = normalizedStatus;

  if (normalizedStatus === "COMPLIANT") {
    className = "status-compliant";
    label = "🟢 COMPLIANT";
  }

  if (normalizedStatus === "REVIEW_REQUIRED") {
    className = "status-review";
    label = "🟡 REVIEW REQUIRED";
  }

  if (
    normalizedStatus === "POTENTIAL_NON_COMPLIANCE"
  ) {
    className = "status-danger";
    label = "🔴 POTENTIAL NON-COMPLIANCE";
  }

  return (
    <span className={`status-badge ${className}`}>
      {label}
    </span>
  );
}

export default ComplianceBadge;