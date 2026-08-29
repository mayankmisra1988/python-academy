import "./ProgressBar.css";

function ProgressBar({
    progress = 0,
    completed = false,
    onComplete,
}) {

    const percentage = Math.min(
        100,
        Math.max(
            0,
            Number(progress) || 0
        )
    );


    return (
        <div className="lesson-progress">
            <h3 style={{'margin-top': '10px', 'margin-bottom': '10px'}}>
                Lesson Progress
            </h3>
            <div className="progress-track">
                <div
                    className="progress-fill " 
                    style={{
                        width: `${percentage}%`,margin: '0px 0px 0px 0px',borderRadius: '20px',transition: 'width 0.4s ease'    
                    }}
                />
            </div>
            <div className="progress-details">

                <span>
                    {percentage}% Watched
                </span>


                {completed && (

                    <span className="completed-badge">
                        ✓ Completed
                    </span>

                )}

            </div>


            {!completed && onComplete && (

                <button
                    type="button"
                    className="complete-btn"
                    onClick={onComplete}
                >
                    Mark as Complete
                </button>

            )}


            {completed && (

                <button
                    type="button"
                    className="complete-btn completed"
                    disabled
                >
                    ✓ Completed
                </button>

            )}

        </div>

    );
}

export default ProgressBar;