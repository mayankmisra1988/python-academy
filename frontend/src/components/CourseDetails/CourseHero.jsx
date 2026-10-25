import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { enrollCourse } from "../../services/enrollmentService";
import "./CourseHero.css";

export default function CourseHero({ course }) {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleEnroll = async () => {
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
      navigate("/login", {
        state: {
          from: `/courses/${course.slug}`,
        },
      });
      return;
    }

    if (!course.is_free) {
      toast.error(
        "This is a paid course. Payment verification is not available yet."
      );
      return;
    }

    try {
      setLoading(true);
      await enrollCourse(course.id);
      toast.success("Enrollment successful!");
      navigate("/my-courses");
    } catch (error) {
      const data = error.response?.data;
      const message =
        data?.course?.[0] ||
        data?.detail ||
        "Enrollment failed. Please try again.";

      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="course-hero">
      <div className="hero-image">
        <img src={course.thumbnail} alt={course.title} />
      </div>

      <div className="hero-content">
        <span className="course-level">
          {course.level?.toUpperCase()}
        </span>

        <h1>{course.title}</h1>

        <p className="short-description">
          {course.short_description}
        </p>

        <div className="course-badges">
          <span>
            {course.is_free ? "FREE" : `₹ ${course.price}`}
          </span>
          <span>{course.total_students} Students</span>
          <span>{course.total_lessons} Lessons</span>
          <span>{course.total_sections} Sections</span>
          <span>{course.total_duration} Minutes</span>
        </div>

        <div className="course-description">
          {course.description}
        </div>

        <div className="course-progress">
          <h4>Progress: {course.progress}%</h4>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${course.progress}%` }}
            />
          </div>
        </div>

<div className="course-actions">
  {course.enrolled ? (
    course.progress < 100 ? (
      <Link to={`/courses/${course.slug}/lesson/1`}>
        <button className="continue-btn">
          Continue Learning →
        </button>
      </Link>
    ) : null
  ) : (
            <button
              className="enroll-btn"
              onClick={handleEnroll}
              disabled={loading}
            >
              {loading ? "Enrolling..." : "Enroll Now"}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
