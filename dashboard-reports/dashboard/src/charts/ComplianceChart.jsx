import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

const ComplianceChart = ({ stats = {} }) => {
  const compliant = Number(stats.compliant) || 0
  const nonCompliant = Number(stats.nonCompliant) || 0
  const total = compliant + nonCompliant

  const data = [
    { name: 'Compliant', value: compliant },
    { name: 'Non-Compliant', value: nonCompliant },
  ]

  if (total === 0) {
    return (
      <section className="panel chart-card">
        <div className="panel-header">
          <h2>Compliance Summary</h2>
        </div>
        <div className="empty-state">No inspection data available.</div>
      </section>
    )
  }

  return (
    <section className="panel chart-card">
      <div className="panel-header">
        <h2>Compliance Summary</h2>
        <span className="panel-caption">{total} total records</span>
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="42%"
            cy="50%"
            innerRadius={0}
            outerRadius={82}
            paddingAngle={2}
            stroke="#ffffff"
            strokeWidth={2}
          >
            <Cell fill="#16a34a" />
            <Cell fill="#dc2626" />
          </Pie>

          <Tooltip
            formatter={(value) => [`${value}`, 'Count']}
            contentStyle={{
              borderRadius: 12,
              border: '1px solid #e2e8f0',
              boxShadow: '0 12px 24px rgba(15, 23, 42, 0.08)',
            }}
          />

          <Legend
            layout="vertical"
            verticalAlign="middle"
            align="right"
            wrapperStyle={{
              fontSize: '12px',
              color: '#334155',
              paddingLeft: '8px',
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </section>
  )
}

export default ComplianceChart