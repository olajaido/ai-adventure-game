import React, { useState, useEffect } from 'react';
import { Auth } from 'aws-amplify';
import { generateClient } from 'aws-amplify/api';
import '../styles/Profile.css';

const api = generateClient();

function Profile() {
    const [user, setUser] = useState(null);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadUserProfile();
    }, []);

    const loadUserProfile = async () => {
        try {
            const userData = await Auth.currentAuthenticatedUser();
            setUser(userData);

            const userStats = await api.get('gameApi', '/user-stats');
            setStats(userStats.data);
            setLoading(false);
        } catch (error) {
            console.error('Error loading profile:', error);
            setLoading(false);
        }
    };

    const signOut = async () => {
        try {
            await Auth.signOut();
        } catch (error) {
            console.error('Error signing out:', error);
        }
    };

    if (loading) {
        return <div className="loading">Loading profile...</div>;
    }

    return (
        <div className="profile">
            <div className="profile-header">
                <h2>Adventurer Profile</h2>
                <button onClick={signOut} className="sign-out-button">
                    Sign Out
                </button>
            </div>
            <div className="profile-content">
                <div className="profile-section">
                    <h3>Player Info</h3>
                    <p>Username: {user?.username}</p>
                    <p>Email: {user?.attributes?.email}</p>
                </div>
                <div className="profile-section">
                    <h3>Game Statistics</h3>
                    <div className="stats-grid">
                        <div className="stat-item">
                            <span className="stat-label">Games Played</span>
                            <span className="stat-value">{stats?.gamesPlayed || 0}</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-label">Highest Level</span>
                            <span className="stat-value">{stats?.highestLevel || 1}</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-label">Items Collected</span>
                            <span className="stat-value">{stats?.itemsCollected || 0}</span>
                        </div>
                    </div>
                </div>
                <div className="profile-section">
                    <h3>Achievements</h3>
                    <div className="achievements-list">
                        {stats?.achievements?.map((achievement, index) => (
                            <div key={index} className="achievement-item">
                                <span className="achievement-icon">{achievement.icon}</span>
                                <span className="achievement-name">{achievement.name}</span>
                                <span className="achievement-description">{achievement.description}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Profile;