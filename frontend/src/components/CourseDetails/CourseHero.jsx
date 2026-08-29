import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { enrollCourse } from "../../services/enrollmentService";
import "./CourseHero.css";

export default function CourseHero({ course }) {

  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const handleEnroll = async () => {

    try {

      setLoading(true);

      await enrollCourse(course.id);

      alert("🎉 Enrollment Successful!");

      navigate("/my-courses");

    } catch (error) {

      if (error.response?.data?.course) {
        alert(error.response.data.course[0]);
      } else {
        alert("Enrollment Failed.");
      }

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="course-hero">

      {/* ================= IMAGE ================= */}

      <div className="hero-image">

        <img
          src={course.thumbnail}
          alt={course.title}
        />

      </div>


      {/* ================= CONTENT ================= */}

      <div className="hero-content">

        <span className="course-level">
          {course.level.toUpperCase()}
        </span>


        <h1>
          {course.title}
        </h1>


        <p className="short-description">
          {course.short_description}
        </p>


        {/* ================= COURSE BADGES ================= */}

        <div className="course-badges">

          <span>
            💰{" "}
            {course.is_free
              ? "FREE"
              : `₹ ${course.price}`}
          </span>

          <span>
            👨‍🎓 {course.total_students} Students
          </span>

          <span>
            📚 {course.total_lessons} Lessons
          </span>

          <span>
            📂 {course.total_sections} Sections
          </span>

          <span>
            ⏱ {course.total_duration} Minutes
          </span>

        </div>


        {/* ================= DESCRIPTION ================= */}

        <div className="course-description">

          {course.description}

        </div>


        {/* ================= PROGRESS ================= */}

        <div className="course-progress">

          <h4>
            Progress : {course.progress}%
          </h4>

          <div className="progress-bar">

            <div
              className="progress-fill"
              style={{
                width: `${course.progress}%`,
              }}
            ></div>

          </div>

        </div>


        {/* ================= ACTION ================= */}

        <div className="course-actions">

          {course.enrolled ? (

            <Link
              to={`/courses/${course.slug}/lesson/1`}
            >

              <button className="continue-btn">
                Continue Learning →
              </button>

            </Link>

          ) : (

            <button
              className="enroll-btn"
              onClick={handleEnroll}
              disabled={loading}
            >

              {loading
                ? "Enrolling..."
                : "Enroll Now"}

            </button>

          )}

        </div>

      </div>

    </div>

  );

}