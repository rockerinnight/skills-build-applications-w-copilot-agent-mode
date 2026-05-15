import React, { useState, useEffect } from 'react';
import { buildApiUrl } from '../utils/api';

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const url = buildApiUrl('users');
        console.log('Fetching Users from:', url);
        
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Users request failed with status ${response.status}`);
        }
        const data = await response.json();
        
        console.log('Users response:', data);
        
        // Handle both paginated and plain array responses
        const usersList = data.results || data;
        setUsers(Array.isArray(usersList) ? usersList : []);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError(err.message);
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) return <div className="alert alert-info"><strong>Loading Users...</strong></div>;
  if (error) return <div className="alert alert-danger"><strong>Error:</strong> {error}</div>;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2>👥 Users</h2>
        </div>
        <div className="card-body">
          {users.length === 0 ? (
            <div className="empty-state">
              <p className="no-data">No users found.</p>
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-striped table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Team</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user, index) => (
                    <tr key={user._id || index}>
                      <td><strong>{user.name}</strong></td>
                      <td>{user.email || 'Private'}</td>
                      <td><span className="badge bg-info">{user.team}</span></td>
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

export default Users;
