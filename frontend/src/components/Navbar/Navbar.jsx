// import { Link } from "react-router-dom";
// import logo1 from "../../assets/images/logo1.webp";
// import "./Navbar.css";

// export default function Navbar() {

//   const isLoggedIn = !!localStorage.getItem("access");

//   const logout = () => {
//     localStorage.removeItem("access");
//     localStorage.removeItem("refresh");

//     window.location.href = "/";
//   };

//   return (
//     <>
//       <div className="topbar">
//         <span>📞 +91 9807535595</span>
//         <span>✉ info@pythonacademy.com</span>
//       </div>

//       <nav className="navbar">
//         <div className="logo">
//           <Link to="/" className="logo">
//             <img src={logo1} alt="Python Academy Logo" />
//             <h2>Python Academy</h2>
//           </Link>
//         </div>

//         <ul>
//           <li>
//             <Link to="/">Home</Link>  
//           </li>

//           <li>
//             <Link to="/about">About</Link>
//           </li>

//           <li>
//             <Link to="/courses">Courses</Link>
//           </li>

//           <li>Testimonials</li>

//           <li>Contact</li>
//         </ul>

//         <div className="buttons">

//           {isLoggedIn ? (
//             <>
//               <Link to="/dashboard">
//                 <button className="login">
//                   Dashboard
//                 </button>
//               </Link>

//               <button
//                 className="register"
//                 onClick={logout}
//               >
//                 Logout
//               </button>
//             </>
//           ) : (
//             <>
//               <Link to="/login">
//                 <button className="login">
//                   Login
//                 </button>
//               </Link>

//               <Link to="/register">
//                 <button className="register">
//                   Register
//                 </button>
//               </Link>
//             </>
//           )}

//         </div>
//       </nav>
//     </>
//   );
// }








import { Link } from "react-router-dom";
import logo1 from "../../assets/images/logo1.webp";
import "./Navbar.css";

export default function Navbar() {

  const isLoggedIn = !!localStorage.getItem("access");

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");

    window.location.href = "/";
  };

  return (
    <>
      <div className="topbar">
        <span>📞 +91 9807535595</span>
        <span>✉ info@pythonacademy.com</span>
      </div>

      <nav className="navbar">
        <div className="logo">
          <Link to="/" className="logo">
            <img src={logo1} alt="Python Academy Logo" />
            <h2>Python Academy</h2>
          </Link>
        </div>

        <ul>
          <li>
            <Link to="/">Home</Link>  
          </li>

          <li>
            <Link to="/about">About</Link>
          </li>

          <li>
            <Link to="/courses">Courses</Link>
          </li>

          <li>Testimonials</li>

          <li>Contact</li>
        </ul>

        <div className="buttons">

          {isLoggedIn ? (
            <>
              <Link to="/dashboard">
                <button className="login">
                  Dashboard
                </button>
              </Link>

              <button
                className="register"
                onClick={logout}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login">
                <button className="login">
                  Login
                </button>
              </Link>

              <Link to="/register">
                <button className="register">
                  Register
                </button>
              </Link>
            </>
          )}

        </div>
      </nav>
    </>
  );
}