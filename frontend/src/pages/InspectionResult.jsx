import MainLayout from "../layouts/MainLayout";
import ComplianceBadge from "../components/ComplianceBadge";
import ViolationCard from "../components/ViolationCard";

function InspectionResult() {

  const savedResult =
    localStorage.getItem("inspectionResult");

  if (!savedResult) {
    return (
      <MainLayout>
        <h1>No inspection result found.</h1>
      </MainLayout>
    );
  }

  const result = JSON.parse(savedResult);

  /*
    Supports multiple possible backend structures.

    Preferred structure:

    {
      inspection_id,
      product: {...},
      compliance: {...}
    }
  */

  const product =
    result.product ||
    result.extracted_data ||
    result.data ||
    {};

  const compliance =
    result.compliance ||
    result.result ||
    result;

  const checks =
    compliance.checks || [];

  const violations =
    compliance.violations || [];

  const inspectionId =
    result.inspection_id ||
    result.id ||
    "N/A";

  return (
    <MainLayout>

      <div className="page-header">

        <div>
          <h1>Inspection Result</h1>

          <p>
            Inspection ID: {inspectionId}
          </p>
        </div>

      </div>

      {/* COMPLIANCE SUMMARY */}

      <div className="result-summary">

        <div className="score-box">

          <p>Compliance Score</p>

          <h1>
            {compliance.score ?? "N/A"}%
          </h1>

        </div>

        <div>

          <p>Overall Status</p>

          <ComplianceBadge
            status={compliance.status}
          />

        </div>

      </div>

      {/* PRODUCT INFORMATION */}

      <section className="result-section">

        <h2>📦 Extracted Product Information</h2>

        <div className="product-grid">

          <Info
            label="Product Name"
            value={product.product_name}
          />

          <Info
            label="Manufacturer"
            value={product.manufacturer}
          />

          <Info
            label="MRP"
            value={product.mrp}
          />

          <Info
            label="Net Quantity"
            value={product.net_quantity}
          />

          <Info
            label="Packing Date"
            value={product.packing_date}
          />

          <Info
            label="Consumer Care"
            value={product.consumer_care}
          />

          <Info
            label="Country of Origin"
            value={product.country_of_origin}
          />

          <Info
            label="Best Before"
            value={product.best_before}
          />

        </div>

      </section>

      {/* COMPLIANCE CHECKS */}

      <section className="result-section">

        <h2>✓ Compliance Checks</h2>

        {checks.length === 0 ? (

          <p>No compliance checks available.</p>

        ) : (

          checks.map((check, index) => (

            <div
              className="check-row"
              key={index}
            >

              <div>

                <strong>
                  {check.status === "PASS"
                    ? "✅"
                    : check.status === "FAIL"
                    ? "❌"
                    : "⚠️"
                  }

                  {" "}

                  {check.field}

                </strong>

                <p>{check.message}</p>

              </div>

            </div>

          ))

        )}

      </section>

      {/* VIOLATIONS */}

      <section className="result-section">

        <h2>⚠️ Potential Violations</h2>

        {violations.length === 0 ? (

          <p className="success-message">
            🎉 No potential violations detected.
          </p>

        ) : (

          violations.map(
            (violation, index) => (

              <ViolationCard
                key={index}
                violation={violation}
              />

            )
          )

        )}

      </section>

    </MainLayout>
  );
}


function Info({ label, value }) {

  return (
    <div className="info-card">

      <p>{label}</p>

      <h3>
        {value ?? "Not Detected"}
      </h3>

    </div>
  );
}


export default InspectionResult;