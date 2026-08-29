import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";

import "./Auth.css";
import { registerUser } from "../../services/authService";

export default function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    confirm_password: "",
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

    // Password confirmation
    if (formData.password !== formData.confirm_password) {
      toast.error("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      await registerUser(formData);

      // Success Toast
      toast.success("Registration Successful! 🎉");

      // Login page par redirect
      navigate("/login");

    } catch (error) {
      console.error("Registration Error:", error);

      if (error.response?.data) {
        const data = error.response.data;

        // Backend detail message
        if (data.detail) {
          toast.error(data.detail);
        }

        // Backend validation errors
        else if (typeof data === "object") {
          const firstError = Object.values(data)[0];

          if (Array.isArray(firstError)) {
            toast.error(firstError[0]);
          } else {
            toast.error(String(firstError));
          }
        }

        else {
          toast.error("Registration Failed");
        }

      } else {
        toast.error("Registration Failed");
      }

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">

      <div className="auth-card">

        <h2>Create Your Account</h2>

        <p>
          Join Python Academy and start learning today.
        </p>

        <form onSubmit={handleSubmit}>

          {/* First & Last Name */}

          <div className="form-row">

            <input
              type="text"
              name="first_name"
              placeholder="First Name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />

            <input
              type="text"
              name="last_name"
              placeholder="Last Name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />

          </div>

          {/* Username */}

          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />

          {/* Email */}

          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />

          {/* Password */}

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />

          {/* Confirm Password */}

          <input
            type="password"
            name="confirm_password"
            placeholder="Confirm Password"
            value={formData.confirm_password}
            onChange={handleChange}
            required
          />

          {/* Register Button */}

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Creating Account..."
              : "Register"}
          </button>

        </form>

        <div className="bottom-link">

          Already have an account?{" "}

          <Link to="/login">
            Login
          </Link>

        </div>

      </div>

    </div>
  );
}