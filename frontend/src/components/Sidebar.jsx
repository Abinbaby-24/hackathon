import { NavLink, useNavigate } from "react-router-dom";

function Sidebar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");

    navigate("/login");
  };

  return (
    <aside className="sidebar">

      <div className="logo">
        <h2>🔍 Package AI</h2>
        <p>Compliance Inspector</p>
      </div>

      <nav className="nav-links">

        <NavLink to="/dashboard">
          📊 Dashboard
        </NavLink>

        <NavLink to="/upload">
          🔍 New Inspection
        </NavLink>

        <NavLink to="/history">
          📜 Inspection History
        </NavLink>

      </nav>

      <button className="logout-btn" onClick={logout}>
        🚪 Logout
      </button>

    </aside>
  );
}

export default Sidebar;