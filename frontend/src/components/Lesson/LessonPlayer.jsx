import { useCallback, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import "./Lesson.css";

function getYouTubeVideoId(url) {
  if (!url) return null;
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtube.com") && u.searchParams.get("v"))
      return u.searchParams.get("v");
    if (u.hostname === "youtu.be") return u.pathname.replace("/", "");
    if (u.hostname.includes("youtube.com") && u.pathname.startsWith("/embed/"))
      return u.pathname.split("/embed/")[1];
  } catch (error) {
    console.error("Invalid YouTube URL:", error);
  }
  return null;
}

function loadYouTubeAPI() {
  return new Promise((resolve) => {
    if (window.YT?.Player) return resolve(window.YT);

    const previous = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => {
      if (previous) previous();
      resolve(window.YT);
    };

    if (!document.querySelector('script[src="https://www.youtube.com/iframe_api"]')) {
      const script = document.createElement("script");
      script.src = "https://www.youtube.com/iframe_api";
      script.async = true;
      document.body.appendChild(script);
    }
  });
}

function LessonPlayer({ lesson, progress = 0, onProgress, onComplete }) {
  const playerRef = useRef(null);
  const intervalRef = useRef(null);
  const restoredRef = useRef(false);
  const progressRef = useRef(progress);
  const onProgressRef = useRef(onProgress);
  const onCompleteRef = useRef(onComplete);

  const videoId = getYouTubeVideoId(lesson?.video_url);

  useEffect(() => { progressRef.current = Number(progress) || 0; }, [progress]);
  useEffect(() => { onProgressRef.current = onProgress; }, [onProgress]);
  useEffect(() => { onCompleteRef.current = onComplete; }, [onComplete]);

  const stopProgressTracking = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
      console.log("⏹ Progress tracking stopped");
    }
  }, []);

  const startProgressTracking = useCallback(() => {
    if (intervalRef.current) return;

    intervalRef.current = setInterval(() => {
      const player = playerRef.current;
      if (!player) return;

      try {
        const current = player.getCurrentTime();
        const duration = player.getDuration();
        if (!duration || duration <= 0) return;

        const percentage = Math.min(100, Math.round((current / duration) * 100));

        console.log("📊 Video Progress:", percentage + "%");
        onProgressRef.current?.(percentage);

        if (percentage >= 95) {
          onCompleteRef.current?.();
          stopProgressTracking();
        }
      } catch (error) {
        console.error("Video progress error:", error);
      }
    }, 5000);
  }, [stopProgressTracking]);

  const restoreSavedPosition = useCallback(() => {
    const player = playerRef.current;
    if (!player || restoredRef.current) return;

    const saved = Math.min(100, Math.max(0, Number(progressRef.current) || 0));
    if (saved <= 0 || saved >= 100) {
      restoredRef.current = true;
      return;
    }

    try {
      const duration = player.getDuration();
      if (!duration || duration <= 0) return;

      const resumeTime = (duration * saved) / 100;
      player.seekTo(resumeTime, true);
      restoredRef.current = true;

      console.log(`⏩ Resumed from ${saved}%`);
    } catch (error) {
      console.error("Resume position error:", error);
    }
  }, []);

  useEffect(() => {
    if (playerRef.current && Number(progress) > 0) restoreSavedPosition();
  }, [progress, restoreSavedPosition]);

  useEffect(() => {
    if (!videoId) return undefined;

    let mounted = true;
    restoredRef.current = false;

    const init = async () => {
      try {
        const YT = await loadYouTubeAPI();
        if (!mounted) return;

        const container = document.getElementById("youtube-player");
        if (!container) return;

        playerRef.current?.destroy?.();

        playerRef.current = new YT.Player("youtube-player", {
          videoId,
          playerVars: { rel: 0, modestbranding: 1, playsinline: 1 },
          events: {
            onReady: () => {
              console.log("✅ YouTube player ready");
              restoreSavedPosition();
            },
            onStateChange: (event) => {
              if (event.data === YT.PlayerState.PLAYING) {
                restoreSavedPosition();
                startProgressTracking();
              } else {
                stopProgressTracking();
              }

              if (event.data === YT.PlayerState.ENDED) {
                onProgressRef.current?.(100);
                onCompleteRef.current?.();
              }
            },
          },
        });
      } catch (error) {
        console.error("YouTube Player Error:", error);
      }
    };

    init();

    return () => {
      mounted = false;
      stopProgressTracking();
      try { playerRef.current?.destroy?.(); } catch (error) {
        console.error("YouTube destroy error:", error);
      }
      playerRef.current = null;
    };
  }, [videoId, restoreSavedPosition, startProgressTracking, stopProgressTracking]);

  if (!lesson) return null;

  return (
    <>
      <div className="video-section">
        {videoId ? (
          <div className="video-wrapper">
            <div id="youtube-player" style={{ width: "100%", height: "100%" }} />
          </div>
        ) : (
          <div className="video-wrapper no-video">
            <div className="no-video-content">
              <span>🎬</span>
              <h3>No Video Available</h3>
              <p>This lesson does not have a valid video URL.</p>
            </div>
          </div>
        )}
      </div>

      <div className="lesson-info-card">
        <div className="lesson-info-header">
          <div>
            <span className="lesson-info-label">DESCRIPTION</span>
            <p className="lesson-description">
              {lesson.description || "No description available."}
            </p>
          </div>
          {lesson.is_published && (
            <span className="lesson-status-badge">✓ Published</span>
          )}
        </div>

        <div className="lesson-action-row">
          {lesson.quiz && (
            <Link to={`/lesson/${lesson.id}/quiz`} className="start-quiz-btn">
              📝 Start Quiz
            </Link>
          )}
        </div>

        <div className="lesson-meta-row">
          <div className="lesson-meta-item">
            <span className="meta-icon">⏱</span>
            <div><small>Duration</small><strong>{lesson.duration || 0} Minutes</strong></div>
          </div>

          {lesson.is_preview && (
            <div className="lesson-meta-item">
              <span className="meta-icon">👁</span>
              <div><small>Access</small><strong>Preview Lesson</strong></div>
            </div>
          )}
        </div>

        <div className="lesson-notes-card">
          <div className="notes-icon">📄</div>
          <div className="notes-content">
            <h3>Lesson Notes</h3>
            {(lesson.notes_url || lesson.notes) ? (
              <a href={lesson.notes_url || lesson.notes} target="_blank" rel="noreferrer" className="download-notes-btn">
                📄 Download Notes
              </a>
            ) : <p>No notes available for this lesson.</p>}
          </div>
        </div>
      </div>
    </>
  );
}

export default LessonPlayer;