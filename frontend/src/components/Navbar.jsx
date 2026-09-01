function Navbar() {
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  return (
    <header className="navbar">

      <div>
        <h2>Package Compliance Inspection System</h2>
      </div>

      <div className="user-info">
        👤 {user.name || "Inspector"}
      </div>

    </header>
  );
}

export default Navbar;