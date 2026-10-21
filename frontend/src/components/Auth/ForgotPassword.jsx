import { useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";

import "./Auth.css";
import { forgotPassword } from "../../services/authService";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await forgotPassword(email);
      setSubmitted(true);
      toast.success(
        response.detail ||
          "If your account exists, a reset link has been sent to your email."
      );
    } catch (error) {
      toast.error(
        error.response?.data?.detail ||
          "Unable to process your request. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Forgot Password?</h2>

        {submitted ? (
          <>
            <p>
              If an account exists for this email, you will receive
              instructions to reset your password.
            </p>
            <Link to="/login">Back to Login</Link>
          </>
        ) : (
          <>
            <p>Enter your registered email address to reset your password.</p>

            <form onSubmit={handleSubmit}>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <button type="submit" disabled={loading}>
                {loading ? "Sending..." : "Send Reset Link"}
              </button>
            </form>

            <p style={{margin:'25px'}}>
              Remember your password? <Link to="/login">Login</Link>
            </p>
          </>
        )}
      </div>
    </div>
  );
}