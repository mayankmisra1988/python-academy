import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar/Sidebar";
import Topbar from "../components/Topbar/Topbar";
import "./DashboardLayout.css";

function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <Sidebar />

      <div className="dashboard-main">
        <Topbar />

        <div className="dashboard-content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default DashboardLayout;