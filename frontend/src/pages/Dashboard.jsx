import { useNavigate } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <MainLayout>

      <div className="page-header">

        <div>
          <h1>Dashboard</h1>
          <p>
            Overview of package compliance inspections
          </p>
        </div>

        <button
          className="primary-btn"
          onClick={() => navigate("/upload")}
        >
          + New Inspection
        </button>

      </div>

      <div className="stats-grid">

        <div className="stat-card">
          <p>Total Inspections</p>
          <h2>0</h2>
        </div>

        <div className="stat-card">
          <p>Compliant</p>
          <h2>0</h2>
        </div>

        <div className="stat-card">
          <p>Review Required</p>
          <h2>0</h2>
        </div>

        <div className="stat-card">
          <p>Potential Violations</p>
          <h2>0</h2>
        </div>

      </div>

      <div className="dashboard-welcome">

        <h2>Welcome to Package AI</h2>

        <p>
          Upload a package image to analyze product
          declarations and compliance information.
        </p>

        <button
          className="primary-btn"
          onClick={() => navigate("/upload")}
        >
          Start New Inspection
        </button>

      </div>

    </MainLayout>
  );
}

export default Dashboard;