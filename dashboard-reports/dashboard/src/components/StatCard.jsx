const StatCard = ({ label, value, tone = 'neutral' }) => {
  const toneStyles = {
    neutral: { background: '#f4f6fb', color: '#1f2937' },
    success: { background: '#eafaf1', color: '#166534' },
    danger: { background: '#fff1f2', color: '#b91c1c' },
    accent: { background: '#eef2ff', color: '#4338ca' },
  }

  return (
    <div
      style={{
        background: toneStyles[tone].background,
        color: toneStyles[tone].color,
        borderRadius: 16,
        padding: '1.25rem',
        boxShadow: '0 8px 24px rgba(15, 23, 42, 0.06)',
      }}
    >
      <div style={{ fontSize: 14, opacity: 0.8, marginBottom: 8 }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 700, lineHeight: 1.2 }}>{value}</div>
    </div>
  )
}

export default StatCard
