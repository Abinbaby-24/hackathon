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
        <div>
          <p className="eyebrow">Compliance Dashboard</p>
          <h1>Food Safety Inspection Overview</h1>
        </div>
        <button className="primary-btn">Export Report</button>
      </header>

      <section className="stats-grid">
        <StatCard label="Total Inspections" value={dashboardStats.totalInspections} tone="accent" />
        <StatCard label="Compliant" value={dashboardStats.compliant} tone="success" />
        <StatCard label="Non-Compliant" value={dashboardStats.nonCompliant} tone="danger" />
        <StatCard label="Compliance Rate" value={`${dashboardStats.complianceRate}%`} tone="neutral" />
      </section>

      <section className="content-grid">
        <ComplianceChart stats={dashboardStats} />
        <ViolationChart data={violationData} />
      </section>

      <div className="history-panel">
        <InspectionHistory inspections={inspections} />
      </div>
    </div>
  )
}

export default App
