import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import CourseCard from "./CourseCard";
import { getCourses } from "../../services/courseService";

import "./Courses.css";

export default function Courses() {

  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCourses();
  }, []);

  async function loadCourses() {
    try {
      const data = await getCourses();
      setCourses(data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <section className="courses-section">
        <h2>Loading Courses...</h2>
      </section>
    );
  }

  return (
    <section className="courses-section">

      <div className="courses-header">

        <div>
          <h2>Popular Courses</h2>
          <p>Choose from our most loved Python courses</p>
        </div>

        <Link to="/courses">
          <button className="view-btn">
            View All Courses →
          </button>
        </Link>

      </div>

      <div className="courses-grid">

        {courses.map((course) => (
          <CourseCard
            key={course.id}
            course={course}
          />
        ))}

      </div>

    </section>
  );
}