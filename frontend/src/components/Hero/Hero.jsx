import { Link } from "react-router-dom";
import "./Hero.css";
import hero_python_logo11 from "../../assets/images/hero_python_logo11.png";

export default function Hero() {

  const isLoggedIn = !!localStorage.getItem("access");

  return (
    <section className="hero">

      <div className="hero-left">

        <span className="badge">
          #1 Online Python Learning Platform
        </span>

        <h1>
          Learn Python Programming
          <br />
          From <span>Basic to Advanced</span>
        </h1>

        <p>
          Join 500+ students and start your journey
          from beginner to expert.
        </p>

        <div className="hero-buttons">

          {isLoggedIn ? (
            <>
              <Link to="/dashboard">
                <button>
                  🚀 Go to Dashboard
                </button>
              </Link>

              <Link to="/my-courses">
                <button className="outline">
                  📚 My Courses
                </button>
              </Link>
            </>
          ) : (
            <>
              <Link to="/register">
                <button>
                  Register Now
                </button>
              </Link>

              <Link to="/login">
                <button className="outline">
                  Login
                </button>
              </Link>
            </>
          )}

        </div>

      </div>

      <div className="hero-right">
        <img
          src={hero_python_logo11}
          alt="Python Academy"
        />
      </div>

    </section>
  );
}