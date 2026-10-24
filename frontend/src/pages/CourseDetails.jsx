import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
getCourseDetails,
getCurriculum,
} from "../services/courseService";
import CourseHero from "../components/CourseDetails/CourseHero";
import Curriculum from "../components/CourseDetails/Curriculum";
import "./CourseDetails.css";

export default function CourseDetails() {
const { slug } = useParams();

const [course, setCourse] = useState(null);
const [curriculum, setCurriculum] = useState([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");

useEffect(() => {
let cancelled = false;

async function loadCourse() {
  setLoading(true);
  setError("");
  setCourse(null);
  setCurriculum([]);

  try {
    const courseData = await getCourseDetails(slug);

    if (!courseData) {
      throw new Error(
        "Course load nahi ho paya. Please refresh karke dobara try karein."
      );
    }

    const curriculumData = await getCurriculum(courseData.id);

    if (cancelled) return;

    setCourse(courseData);
    setCurriculum(curriculumData);
  } catch (err) {
    if (!cancelled) {
      console.error("Course details loading error:", err);
      setError(
        err.message || "Course load karte waqt error aaya."
      );
    }
  } finally {
    if (!cancelled) {
      setLoading(false);
    }
  }
}

loadCourse();

return () => {
  cancelled = true;
};

}, [slug]);

if (loading) {
return <h2>Loading course...</h2>;
}

if (error || !course) {
return (
<div className="course-load-error">
<h2>Course load nahi ho paya</h2>
<p>{error || "Course nahi mila."}</p>
</div>
);
}

return (
<div>
<CourseHero course={course} />

  <Curriculum
    curriculum={curriculum}
    slug={slug}
    course={course}
  />
</div>

);
}