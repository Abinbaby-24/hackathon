const ComplianceChart = ({ stats = {} }) => {
  const compliant = stats.compliant || 0
  const nonCompliant = stats.nonCompliant || 0

  return (
    <section
      style={{
        background: '#fff',
        borderRadius: 20,
        padding: '1.5rem',
        boxShadow: '0 10px 30px rgba(15, 23, 42, 0.08)',
      }}
    >
      <h2 style={{ marginTop: 0, marginBottom: 20, fontSize: 22 }}>Compliance Summary</h2>

      <div style={{ display: 'flex', gap: 14, marginBottom: 20 }}>
        <div style={{ flex: 1, height: 12, background: '#e2e8f0', borderRadius: 999, overflow: 'hidden' }}>
          <div
            style={{
              width: `${(compliant / (compliant + nonCompliant || 1)) * 100}%`,
              height: '100%',
              background: '#22c55e',
              borderRadius: 999,
            }}
          />
        </div>
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', color: '#475569' }}>
        <div>
          <div style={{ fontWeight: 700, fontSize: 20 }}>{compliant}</div>
          <div>Compliant</div>
        </div>
        <div>
          <div style={{ fontWeight: 700, fontSize: 20 }}>{nonCompliant}</div>
          <div>Non-compliant</div>
        </div>
      </div>
    </section>
  )
}

export default ComplianceChart
