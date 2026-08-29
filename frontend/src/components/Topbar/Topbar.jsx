import "./Topbar.css";

function Topbar() {

  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <header className="topbar">

      <div>
        <h2>Student Dashboard</h2>
      </div>

      <div className="topbar-right">

        <span>
          Welcome,
          {" "}
          {user?.first_name || user?.username || "Student"}
        </span>

      </div>

    </header>
  );
}

export default Topbar;