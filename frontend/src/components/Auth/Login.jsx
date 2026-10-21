import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import "./Auth.css";
import { loginUser } from "../../services/authService";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      await loginUser(formData);

      toast.success("Login successful!");

      const redirectTo = location.state?.from;

      if (
        typeof redirectTo === "string" &&
        redirectTo.startsWith("/") &&
        !redirectTo.startsWith("//")
      ) {
        navigate(redirectTo, { replace: true });
      } else {
        navigate("/dashboard", { replace: true });
      }
    } catch (error) {
      console.error("Login Error:", error);

      const data = error.response?.data;

      if (data?.detail) {
        toast.error(data.detail);
      } else if (data && typeof data === "object") {
        const firstError = Object.values(data)[0];

        if (Array.isArray(firstError)) {
          toast.error(String(firstError[0]));
        } else if (firstError) {
          toast.error(String(firstError));
        } else {
          toast.error("Invalid email or password.");
        }
      } else {
        toast.error("Login failed. Please check your connection and credentials.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Welcome Back</h2>

        <p>Login to continue your learning journey.</p>

        <form onSubmit={handleSubmit}>
          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <div className="bottom-link">
          Don't have an account? <Link to="/register">Register</Link>

          <div style={{ marginTop: "8px" }}>
            <Link to="/forgot-password" style={{ fontSize: "13px" }}>
              Forgot Password?
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
