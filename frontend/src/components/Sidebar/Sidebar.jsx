import { NavLink, Link} from "react-router-dom";
import "./Sidebar.css";

function Sidebar() {
  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");

    window.location.href = "/";
  };
  return (
    <aside className="sidebar">

      {/* Top */}
      <div className="sidebar-top">

        {/* Logo */}
        <div className="logo">
          <Link to="/" className="logo-link">
            <h2>🐍 Python Academy</h2>
          </Link>
        </div>

        {/* Navigation */}
        <nav>

          <NavLink
            to="/dashboard"
            end
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            🏠 Dashboard
          </NavLink>

          <NavLink
            to="/my-courses"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            📚 My Courses
          </NavLink>

          <NavLink
            to="/certificates"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            🎓 Certificates
          </NavLink>

          <NavLink
            to="/profile"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            👤 Profile
          </NavLink>

          <NavLink
            to="/settings"
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            ⚙️ Settings
          </NavLink>

        </nav>

      </div>

      {/* Bottom */}
      <div className="sidebar-bottom">

        <button
          className="logout-btn"
          onClick={logout}
        >
          🚪 Logout
        </button>

      </div>

    </aside>
  );
}

export default Sidebar;