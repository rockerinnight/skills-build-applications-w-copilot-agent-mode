import React, { useState, useEffect } from 'react';
import { fetchAllPages } from '../utils/api';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        const activitiesList = await fetchAllPages('activities');
        setActivities(activitiesList);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching activities:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (loading) return <div className="alert alert-info"><strong>Loading Activities...</strong></div>;
  if (error) return <div className="alert alert-danger"><strong>Error:</strong> {error}</div>;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2>📋 Activities</h2>
        </div>
        <div className="card-body">
          {activities.length === 0 ? (
            <div className="empty-state">
              <p className="no-data">No activities found.</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead className="table-light">
                  <tr>
                    <th>User</th>
                    <th>Activity</th>
                    <th className="text-end">Duration (min)</th>
                  </tr>
                </thead>
                <tbody>
                  {activities.map((activity, index) => (
                    <tr key={activity._id || index}>
                      <td><strong>{activity.user || 'N/A'}</strong></td>
                      <td>{activity.activity}</td>
                      <td className="text-end">
                        <span className="badge bg-primary">{activity.duration}</span>
                      </td>
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

export default Activities;
