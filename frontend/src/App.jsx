import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import InspectionResult from "./pages/InspectionResult";
import InspectionHistory from "./pages/InspectionHistory";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/upload" element={<Upload />} />
      <Route path="/result" element={<InspectionResult />} />
      <Route path="/history" element={<InspectionHistory />} />
    </Routes>
  );
}

export default App;