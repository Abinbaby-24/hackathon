const InspectionHistory = ({ inspections = [] }) => {
  return (
    <section
      style={{
        background: '#fff',
        borderRadius: 20,
        padding: '1.5rem',
        boxShadow: '0 10px 30px rgba(15, 23, 42, 0.08)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h2 style={{ margin: 0, fontSize: 22 }}>Inspection History</h2>
        <span style={{ color: '#64748b', fontSize: 14 }}>Last 5 records</span>
      </div>

      <div style={{ display: 'grid', gap: 12 }}>
        {inspections.map((item) => (
          <div
            key={item.id}
            style={{
              display: 'grid',
              gridTemplateColumns: '1.5fr 1fr 1fr 1fr',
              gap: 12,
              alignItems: 'center',
              padding: '0.9rem 1rem',
              borderRadius: 12,
              background: '#f8fafc',
              border: '1px solid #e2e8f0',
            }}
          >
            <div>
              <div style={{ fontWeight: 700 }}>{item.productName}</div>
              <div style={{ color: '#64748b', fontSize: 13 }}>ID: {item.id}</div>
            </div>
            <div style={{ color: '#475569' }}>{item.date}</div>
            <div>
              <span
                style={{
                  display: 'inline-block',
                  padding: '0.35rem 0.7rem',
                  borderRadius: 999,
                  fontSize: 12,
                  fontWeight: 600,
                  background: item.status === 'Compliant' ? '#dcfce7' : '#fee2e2',
                  color: item.status === 'Compliant' ? '#166534' : '#b91c1c',
                }}
              >
                {item.status}
              </span>
            </div>
            <div style={{ fontWeight: 700, textAlign: 'right' }}>{item.complianceScore}%</div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default InspectionHistory
