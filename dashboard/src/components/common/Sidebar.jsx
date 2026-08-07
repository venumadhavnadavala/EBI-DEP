import {
  MdDashboard,
  MdBarChart,
  MdInventory,
  MdInsights,
  MdSettings,
} from "react-icons/md";
import { NavLink } from "react-router-dom";

export default function Sidebar() {
  const linkStyle = ({ isActive }) => ({
    background: isActive ? "#4F8EF7" : "transparent",
    color: "#fff",
  });

  return (
    <aside className="sidebar">
      <div className="logo">
        <h2>Enterprise BI</h2>
        <p>Business Intelligence</p>
      </div>

      <nav>
        <NavLink to="/" style={linkStyle}>
          <MdDashboard />
          <span>Dashboard</span>
        </NavLink>

        <NavLink to="/sales" style={linkStyle}>
          <MdBarChart />
          <span>Sales</span>
        </NavLink>

        <NavLink to="/inventory" style={linkStyle}>
          <MdInventory />
          <span>Inventory</span>
        </NavLink>

        <NavLink to="/insights" style={linkStyle}>
          <MdInsights />
          <span>AI Insights</span>
        </NavLink>

        <NavLink to="/settings" style={linkStyle}>
          <MdSettings />
          <span>Settings</span>
        </NavLink>
      </nav>
    </aside>
  );
}