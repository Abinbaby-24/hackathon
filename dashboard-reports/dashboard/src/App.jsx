import './App.css'
import StatCard from './components/StatCard'
import InspectionHistory from './components/InspectionHistory'
import ComplianceChart from './charts/ComplianceChart'
import ViolationChart from './charts/ViolationChart'
import { inspections, dashboardStats, violationData } from './data/mockData'

function App() {
  return (
    <div className="dashboard-shell">
      <header className="topbar">
        <div className="header-copy">
          <p className="eyebrow">Compliance Dashboard</p>
          <h1>Packaged Commodity Inspector</h1>
          <p className="header-subtitle">Legal Metrology Compliance Dashboard</p>
          <p className="header-meta">Last updated: Today</p>
        </div>
        <button type="button" className="primary-btn">
          Export Report
        </button>
      </header>

      <section className="stats-grid">
        <StatCard
          label="Total Inspections"
          value={dashboardStats.totalInspections}
          tone="accent"
          meta="Across all inspections"
        />
        <StatCard
          label="Compliant"
          value={dashboardStats.compliant}
          tone="success"
          meta="Within compliance threshold"
        />
        <StatCard
          label="Non-Compliant"
          value={dashboardStats.nonCompliant}
          tone="danger"
          meta="Requires follow-up"
        />
        <StatCard
          label="Compliance Rate"
          value={`${dashboardStats.complianceRate}%`}
          tone="neutral"
          meta="Overall pass rate"
        />
      </section>

      <section className="content-grid">
        <ComplianceChart stats={dashboardStats} />
        <ViolationChart data={violationData} />
      </section>

      <section className="history-panel">
        <InspectionHistory inspections={inspections} />
      </section>
    </div>
  )
}

export default App
