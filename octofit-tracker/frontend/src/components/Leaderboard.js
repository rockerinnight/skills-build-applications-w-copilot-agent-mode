import React, { useState, useEffect } from 'react';
import { buildApiUrl } from '../utils/api';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const url = buildApiUrl('leaderboard');
        console.log('Fetching Leaderboard from:', url);
        
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Leaderboard request failed with status ${response.status}`);
        }
        const data = await response.json();
        
        console.log('Leaderboard response:', data);
        
        // Handle both paginated and plain array responses
        const leaderboardList = data.results || data;
        const sortedList = (Array.isArray(leaderboardList) ? leaderboardList : [])
          .sort((a, b) => (b.points || 0) - (a.points || 0));
        setLeaderboard(sortedList);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return <div className="alert alert-info"><strong>Loading Leaderboard...</strong></div>;
  if (error) return <div className="alert alert-danger"><strong>Error:</strong> {error}</div>;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2>🥇 Leaderboard</h2>
        </div>
        <div className="card-body">
          {leaderboard.length === 0 ? (
            <div className="empty-state">
              <p className="no-data">No leaderboard entries found.</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead className="table-light">
                  <tr>
                    <th className="text-center">Rank</th>
                    <th>User</th>
                    <th className="text-end">Points</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry, index) => (
                    <tr key={entry._id || index}>
                      <td className="text-center">
                        {index === 0 ? (
                          <span className="badge bg-warning text-dark">🥇 1st</span>
                        ) : index === 1 ? (
                          <span className="badge bg-secondary">🥈 2nd</span>
                        ) : index === 2 ? (
                          <span className="badge bg-danger">🥉 3rd</span>
                        ) : (
                          <span className="badge bg-dark">#{index + 1}</span>
                        )}
                      </td>
                      <td><strong>{entry.user || 'N/A'}</strong></td>
                      <td className="text-end"><span className="badge bg-primary" style={{fontSize: '1rem'}}>{entry.points}</span></td>
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

export default Leaderboard;
