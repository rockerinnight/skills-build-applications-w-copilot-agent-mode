import React, { useState, useEffect } from 'react';
import { fetchAllPages } from '../utils/api';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const teamsList = await fetchAllPages('teams');
        setTeams(teamsList);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching teams:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) return <div className="alert alert-info"><strong>Loading Teams...</strong></div>;
  if (error) return <div className="alert alert-danger"><strong>Error:</strong> {error}</div>;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2>🏆 Teams</h2>
        </div>
        <div className="card-body">
          {teams.length === 0 ? (
            <div className="empty-state">
              <p className="no-data">No teams found.</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Team Name</th>
                    <th className="text-end">Members</th>
                  </tr>
                </thead>
                <tbody>
                  {teams.map((team, index) => (
                    <tr key={team._id || index}>
                      <td><strong>{team.name}</strong></td>
                      <td className="text-end"><span className="badge bg-success">{Array.isArray(team.members) ? team.members.length : 0}</span></td>
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

export default Teams;
