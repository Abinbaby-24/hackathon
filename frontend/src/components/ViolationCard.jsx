function ViolationCard({ violation }) {

  const severity =
    violation.severity || "UNKNOWN";

  return (
    <div className="violation-card">

      <div className="violation-header">

        <h3>
          ⚠️ {violation.type || "Violation"}
        </h3>

        <span
          className={`severity severity-${severity.toLowerCase()}`}
        >
          {severity}
        </span>

      </div>

      <p>
        <strong>Field:</strong>{" "}
        {violation.field || "Unknown"}
      </p>

      <p>
        {violation.message}
      </p>

    </div>
  );
}

export default ViolationCard;