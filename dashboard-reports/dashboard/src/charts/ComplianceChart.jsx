import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const ComplianceChart = ({ stats = {} }) => {
  const compliant = stats.compliant || 0
  const nonCompliant = stats.nonCompliant || 0

  const data = [
    { name: 'Compliant', value: compliant },
    { name: 'Non-Compliant', value: nonCompliant },
  ]

  return (
    <section
      style={{
        background: '#fff',
        borderRadius: 20,
        padding: '1.5rem',
        boxShadow: '0 10px 30px rgba(15, 23, 42, 0.08)',
      }}
    >
      <h2 style={{ marginTop: 0, marginBottom: 20, fontSize: 22 }}>
        Compliance Summary
      </h2>

      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={90}
            label
          >
            <Cell fill="#22c55e" />
            <Cell fill="#ef4444" />
          </Pie>

          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </section>
  )
}

export default ComplianceChart