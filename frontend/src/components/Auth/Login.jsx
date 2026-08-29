import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import "./Auth.css";
import { loginUser } from "../../services/authService";

export default function Login() {
  const navigate = useNavigate();

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

      // Success Toast
      toast.success("Login Successful! 🎉");

      // Dashboard par redirect
      navigate("/dashboard");

    } catch (error) {
      console.error("Login Error:", error);

      if (error.response?.data) {
        const data = error.response.data;

        // Backend ka detail message
        if (data.detail) {
          toast.error(data.detail);
        }

        // Validation errors
        else if (typeof data === "object") {
          const firstError = Object.values(data)[0];

          if (Array.isArray(firstError)) {
            toast.error(firstError[0]);
          } else {
            toast.error(String(firstError));
          }
        }

        else {
          toast.error("Invalid email or password.");
        }
      } else {
        toast.error("Invalid email or password.");
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">

      <div className="auth-card">

        <h2>Welcome Back</h2>

        <p>
          Login to continue your learning journey.
        </p>

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

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Logging in..."
              : "Login"}
          </button>

        </form>

        <div className="bottom-link">

          Don't have an account?{" "}

          <Link to="/register">
            Register
          </Link>

        </div>

      </div>

    </div>
  );
}