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
        Violation Types
      </h2>

      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={data}
          margin={{
            top: 10,
            right: 10,
            left: 0,
            bottom: 10,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="name" />

          <YAxis allowDecimals={false} />

          <Tooltip />

          <Bar
            dataKey="count"
            fill="#f59e0b"
            radius={[6, 6, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </section>
  )
}

export default ViolationChart