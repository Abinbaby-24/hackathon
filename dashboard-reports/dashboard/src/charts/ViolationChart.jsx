const ViolationChart = ({ data = [] }) => {
  const maxValue = Math.max(...data.map((item) => item.count), 1)

  return (
    <section
      style={{
        background: '#fff',
        borderRadius: 20,
        padding: '1.5rem',
        boxShadow: '0 10px 30px rgba(15, 23, 42, 0.08)',
      }}
    >
      <h2 style={{ marginTop: 0, marginBottom: 20, fontSize: 22 }}>Violation Types</h2>

      <div style={{ display: 'grid', gap: 14 }}>
        {data.map((item) => (
          <div key={item.name}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
              <span style={{ color: '#334155', fontWeight: 600 }}>{item.name}</span>
              <span style={{ color: '#64748b' }}>{item.count}</span>
            </div>
            <div style={{ height: 10, background: '#e2e8f0', borderRadius: 999, overflow: 'hidden' }}>
              <div
                style={{
                  width: `${(item.count / maxValue) * 100}%`,
                  height: '100%',
                  background: '#f59e0b',
                  borderRadius: 999,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default ViolationChart
