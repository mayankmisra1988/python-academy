import { useEffect, useState } from "react";
import {
  getProfile,
  updateProfile,
} from "../services/profileService";

import "./Profile.css";

function Profile() {
  const [profile, setProfile] = useState({
    first_name: "",
    last_name: "",
    phone: "",
    bio: "",
    date_of_birth: "",
    profile_image: null,
    email: "",
    username: "",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await getProfile();
      setProfile(data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setSaving(true);

    try {
      const data = await updateProfile(profile);

      setProfile(data);

      alert("Profile Updated Successfully");
    } catch (error) {
      console.log(error);
      alert("Unable to update profile.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <h2>Loading Profile...</h2>;
  }

  return (
    <div className="profile-page">

      <div className="profile-card">

        <h1>👤 My Profile</h1>

        <form onSubmit={handleSubmit}>

          <div className="profile-grid">

            <div>

              <label>First Name</label>

              <input
                type="text"
                name="first_name"
                value={profile.first_name}
                onChange={handleChange}
              />

            </div>

            <div>

              <label>Last Name</label>

              <input
                type="text"
                name="last_name"
                value={profile.last_name}
                onChange={handleChange}
              />

            </div>

            <div>

              <label>Email</label>

              <input
                value={profile.email}
                disabled
              />

            </div>

            <div>

              <label>Username</label>

              <input
                value={profile.username}
                disabled
              />

            </div>

            <div>

              <label>Phone</label>

              <input
                type="text"
                name="phone"
                value={profile.phone || ""}
                onChange={handleChange}
              />

            </div>

            <div>

              <label>Date of Birth</label>

              <input
                type="date"
                name="date_of_birth"
                value={profile.date_of_birth || ""}
                onChange={handleChange}
              />

            </div>

          </div>

          <div className="bio-box">

            <label>Bio</label>

            <textarea
              rows="5"
              name="bio"
              value={profile.bio || ""}
              onChange={handleChange}
            />

          </div>

          <button
            type="submit"
            disabled={saving}
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>

        </form>

      </div>

    </div>
  );
}

export default Profile;