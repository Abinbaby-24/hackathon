const InspectionHistory = ({ inspections = [] }) => {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Inspection History</h2>
        <span className="panel-caption">
          {inspections.length ? `Last ${Math.min(inspections.length, 5)} records` : 'No records'}
        </span>
      </div>

      {inspections.length === 0 ? (
        <div className="empty-state">No inspection records available.</div>
      ) : (
        <div className="table-wrap">
          <table className="inspection-table">
            <thead>
              <tr>
                <th>Product Name</th>
                <th>Inspection ID</th>
                <th>Date</th>
                <th>Status</th>
                <th>Compliance Score</th>
              </tr>
            </thead>
            <tbody>
              {inspections.map((item) => {
                const statusClass = item.status === 'Compliant' ? 'success' : 'danger'

                return (
                  <tr key={item.id}>
                    <td>
                      <div className="product-cell">
                        <span className="product-name">{item.productName}</span>
                      </div>
                    </td>
                    <td>{item.id}</td>
                    <td>{item.date}</td>
                    <td>
                      <span className={`status-badge ${statusClass}`}>{item.status}</span>
                    </td>
                    <td>
                      <span className="score-pill">{item.complianceScore}%</span>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  )
}

export default InspectionHistory
