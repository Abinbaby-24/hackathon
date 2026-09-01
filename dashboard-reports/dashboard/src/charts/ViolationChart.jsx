import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const ViolationChart = ({ data = [] }) => {
  if (!data || data.length === 0) {
    return (
      <section className="panel chart-card">
        <div className="panel-header">
          <h2>Violation Types</h2>
        </div>
        <div className="empty-state">No violations detected.</div>
      </section>
    )
  }

  return (
    <section className="panel chart-card">
      <div className="panel-header">
        <h2>Violation Types</h2>
        <span className="panel-caption">Most common issues</span>
      </div>

      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={data}
          margin={{
            top: 16,
            right: 12,
            left: 0,
            bottom: 12,
          }}
        >
          <CartesianGrid strokeDasharray="4 4" vertical={false} stroke="#e2e8f0" />

          <XAxis
            dataKey="name"
            tickLine={false}
            axisLine={false}
            tick={{ fill: '#475569', fontSize: 12 }}
          />

          <YAxis
            allowDecimals={false}
            tickLine={false}
            axisLine={false}
            tick={{ fill: '#475569', fontSize: 12 }}
          />

          <Tooltip
            formatter={(value) => [`${value}`, 'Count']}
            contentStyle={{
              borderRadius: 12,
              border: '1px solid #e2e8f0',
              boxShadow: '0 12px 24px rgba(15, 23, 42, 0.08)',
            }}
          />

          <Bar dataKey="count" fill="#f59e0b" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </section>
  )
}

export default ViolationChart