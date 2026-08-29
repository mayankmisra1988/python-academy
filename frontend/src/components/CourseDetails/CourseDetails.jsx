import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { useParams } from "react-router-dom";

import {
  getCourseDetails,
  getCurriculum,
} from "../../services/courseService";

import CourseHero from "./CourseHero";
import Curriculum from "./Curriculum";

import "./CourseDetails.css";


export default function CourseDetails() {

  const { slug } = useParams();

  const [course, setCourse] = useState(null);

  const [curriculum, setCurriculum] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");


  // =====================================================
  // LOAD COURSE
  // =====================================================

  const loadCourse = useCallback(
    async () => {

      try {

        setLoading(true);
        setError("");

        // Course details
        const courseData =
          await getCourseDetails(slug);

        setCourse(courseData);


        // Curriculum
        if (courseData?.id) {

          const curriculumData =
            await getCurriculum(
              courseData.id
            );

          setCurriculum(
            curriculumData
          );

        } else {

          setCurriculum([]);

        }

      } catch (err) {

        console.error(
          "Course loading error:",
          err
        );

        setError(
          "Unable to load this course."
        );

        setCourse(null);
        setCurriculum([]);

      } finally {

        setLoading(false);

      }

    },
    [slug]
  );


  // =====================================================
  // LOAD COURSE WHEN SLUG CHANGES
  // =====================================================

  useEffect(() => {

    loadCourse();

  }, [loadCourse]);


  // =====================================================
  // LOADING
  // =====================================================

  if (loading) {

    return (

      <div className="course-loading">

        <h2>
          Loading course...
        </h2>

      </div>

    );

  }


  // =====================================================
  // ERROR
  // =====================================================

  if (error || !course) {

    return (

      <div className="course-error">

        <h2>
          Course not found
        </h2>

        <p>
          {error ||
            "This course could not be loaded."}
        </p>

      </div>

    );

  }


  // =====================================================
  // COURSE DETAILS PAGE
  // =====================================================

  return (

    <div className="course-details-page">

      {/* Course Hero */}

      <CourseHero
        course={course}
      />


      <Curriculum
        curriculum={curriculum}
        slug={slug}
        course={course}
      />

    </div>

  );

}