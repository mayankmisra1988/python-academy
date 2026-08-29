import { useState } from "react";
import { changePassword } from "../services/authService";
import "./Settings.css";

export default function Settings() {

    const [formData, setFormData] = useState({
        old_password: "",
        new_password: "",
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

        try {
            setLoading(true);
            const res = await changePassword(formData);
            alert(res.message);
            setFormData({
                old_password: "",
                new_password: "",
                confirm_password: "",
            });

        } catch (error) {
            alert(
                error.response?.data?.error ||
                JSON.stringify(error.response?.data)
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="settings-page">

            <div className="settings-card">

                <h1>⚙️ Change Password</h1>

                <form onSubmit={handleSubmit}>

                    <input
                        type="password"
                        name="old_password"
                        placeholder="Current Password"
                        value={formData.old_password}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="password"
                        name="new_password"
                        placeholder="New Password"
                        value={formData.new_password}
                        onChange={handleChange}
                        required
                    />

                    <input
                        type="password"
                        name="confirm_password"
                        placeholder="Confirm Password"
                        value={formData.confirm_password}
                        onChange={handleChange}
                        required
                    />

                    <button disabled={loading}>
                        {loading
                            ? "Updating..."
                            : "Change Password"}
                    </button>

                </form>

            </div>

        </div>
    );
}