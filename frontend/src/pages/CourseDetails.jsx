import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {getCourseDetails,getCurriculum,} from "../services/courseService";
import CourseHero from "../components/CourseDetails/CourseHero";
import Curriculum from "../components/CourseDetails/Curriculum";
import "./CourseDetails.css";

export default function CourseDetails() {

  const { slug } = useParams();

  const [course, setCourse] = useState(null);
  const [curriculum, setCurriculum] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {

    loadCourse();

  }, [slug]);

  async function loadCourse() {

    try {

      const courseData =
        await getCourseDetails(slug);

      setCourse(courseData);

      const curriculumData =
        await getCurriculum(courseData.id);

      setCurriculum(curriculumData);

    } catch (error) {

      console.log(error);

    } finally {

      setLoading(false);

    }

  }

  if (loading)
    return <h2>Loading...</h2>;

  return (

    <div>

      <CourseHero
        course={course}
      />

    <Curriculum
      curriculum={curriculum}
      slug={slug}
    />
    </div>

  );
}