import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      try {
        const url = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
        console.log('Fetching Workouts from:', url);
        
        const response = await fetch(url);
        const data = await response.json();
        
        console.log('Workouts response:', data);
        
        // Handle both paginated and plain array responses
        const workoutsList = data.results || data;
        setWorkouts(Array.isArray(workoutsList) ? workoutsList : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) return <div className="alert alert-info"><strong>Loading Workouts...</strong></div>;
  if (error) return <div className="alert alert-danger"><strong>Error:</strong> {error}</div>;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2>💪 Workouts</h2>
        </div>
        <div className="card-body">
          {workouts.length === 0 ? (
            <div className="empty-state">
              <p className="no-data">No workouts found.</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Workout Name</th>
                    <th>Suggested For</th>
                  </tr>
                </thead>
                <tbody>
                  {workouts.map((workout, index) => (
                    <tr key={workout._id || index}>
                      <td><strong>{workout.name}</strong></td>
                      <td><span className="badge bg-warning text-dark">{workout.suggested_for}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Workouts;
