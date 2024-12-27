// import React, { useState, useEffect } from 'react';
// import { Auth } from 'aws-amplify/auth';
// import { generateClient } from 'aws-amplify/api';
// import '../styles/Profile.css';

// const api = generateClient();

// function Profile() {
//     const [user, setUser] = useState(null);
//     const [stats, setStats] = useState(null);
//     const [loading, setLoading] = useState(true);

//     useEffect(() => {
//         loadUserProfile();
//     }, []);

//     const loadUserProfile = async () => {
//         try {
//             const userData = await Auth.currentAuthenticatedUser();
//             setUser(userData);

//             const userStats = await api.get('gameApi', '/user-stats');
//             setStats(userStats.data);
//             setLoading(false);
//         } catch (error) {
//             console.error('Error loading profile:', error);
//             setLoading(false);
//         }
//     };

//     const signOut = async () => {
//         try {
//             await Auth.signOut();
//         } catch (error) {
//             console.error('Error signing out:', error);
//         }
//     };

//     if (loading) {
//         return <div className="loading">Loading profile...</div>;
//     }

//     return (
//         <div className="profile">
//             <div className="profile-header">
//                 <h2>Adventurer Profile</h2>
//                 <button onClick={signOut} className="sign-out-button">
//                     Sign Out
//                 </button>
//             </div>
//             <div className="profile-content">
//                 <div className="profile-section">
//                     <h3>Player Info</h3>
//                     <p>Username: {user?.username}</p>
//                     <p>Email: {user?.attributes?.email}</p>
//                 </div>
//                 <div className="profile-section">
//                     <h3>Game Statistics</h3>
//                     <div className="stats-grid">
//                         <div className="stat-item">
//                             <span className="stat-label">Games Played</span>
//                             <span className="stat-value">{stats?.gamesPlayed || 0}</span>
//                         </div>
//                         <div className="stat-item">
//                             <span className="stat-label">Highest Level</span>
//                             <span className="stat-value">{stats?.highestLevel || 1}</span>
//                         </div>
//                         <div className="stat-item">
//                             <span className="stat-label">Items Collected</span>
//                             <span className="stat-value">{stats?.itemsCollected || 0}</span>
//                         </div>
//                     </div>
//                 </div>
//                 <div className="profile-section">
//                     <h3>Achievements</h3>
//                     <div className="achievements-list">
//                         {stats?.achievements?.map((achievement, index) => (
//                             <div key={index} className="achievement-item">
//                                 <span className="achievement-icon">{achievement.icon}</span>
//                                 <span className="achievement-name">{achievement.name}</span>
//                                 <span className="achievement-description">{achievement.description}</span>
//                             </div>
//                         ))}
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default Profile;

// import React, { useState, useEffect } from 'react';
// import { getCurrentUser, signOut as amplifySignOut } from 'aws-amplify/auth';
// import { generateClient } from 'aws-amplify/api';
// import '../styles/Profile.css';

// const api = generateClient();

// function Profile() {
//     const [user, setUser] = useState(null);
//     const [stats, setStats] = useState(null);
//     const [loading, setLoading] = useState(true);

//     useEffect(() => {
//         loadUserProfile();
//     }, []);

//     const loadUserProfile = async () => {
//         try {
//             const { userId, signInDetails } = await getCurrentUser();
//             setUser({
//                 username: signInDetails?.loginId,
//                 attributes: {
//                     email: signInDetails?.email
//                 }
//             });

//             const userStats = await api.get('gameApi', '/user-stats');
//             setStats(userStats.data);
//             setLoading(false);
//         } catch (error) {
//             console.error('Error loading profile:', error);
//             setLoading(false);
//         }
//     };

//     const signOut = async () => {
//         try {
//             await amplifySignOut();
//             // You might want to redirect to login page or update app state
//         } catch (error) {
//             console.error('Error signing out:', error);
//         }
//     };

//     if (loading) {
//         return <div className="loading">Loading profile...</div>;
//     }

//     return (
//         <div className="profile">
//             <div className="profile-header">
//                 <h2>Adventurer Profile</h2>
//                 <button onClick={signOut} className="sign-out-button">
//                     Sign Out
//                 </button>
//             </div>
//             <div className="profile-content">
//                 <div className="profile-section">
//                     <h3>Player Info</h3>
//                     <p>Username: {user?.username}</p>
//                     <p>Email: {user?.attributes?.email}</p>
//                 </div>
//                 <div className="profile-section">
//                     <h3>Game Statistics</h3>
//                     <div className="stats-grid">
//                         <div className="stat-item">
//                             <span className="stat-label">Games Played</span>
//                             <span className="stat-value">{stats?.gamesPlayed || 0}</span>
//                         </div>
//                         <div className="stat-item">
//                             <span className="stat-label">Highest Level</span>
//                             <span className="stat-value">{stats?.highestLevel || 1}</span>
//                         </div>
//                         <div className="stat-item">
//                             <span className="stat-label">Items Collected</span>
//                             <span className="stat-value">{stats?.itemsCollected || 0}</span>
//                         </div>
//                     </div>
//                 </div>
//                 <div className="profile-section">
//                     <h3>Achievements</h3>
//                     <div className="achievements-list">
//                         {stats?.achievements?.map((achievement, index) => (
//                             <div key={index} className="achievement-item">
//                                 <span className="achievement-icon">{achievement.icon}</span>
//                                 <span className="achievement-name">{achievement.name}</span>
//                                 <span className="achievement-description">{achievement.description}</span>
//                             </div>
//                         ))}
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default Profile;


// import React, { useState, useEffect } from 'react';
// import { getCurrentUser, signOut as amplifySignOut } from 'aws-amplify/auth';
// import { generateClient } from 'aws-amplify/api';
// import '../styles/Profile.css';

// const api = generateClient();

// function Profile() {
//     const [user, setUser] = useState(null);
//     const [stats, setStats] = useState(null);
//     const [loading, setLoading] = useState(true);

//     useEffect(() => {
//         loadUserProfile();
//     }, []);

//     const loadUserProfile = async () => {
//         try {
//             const { userId, signInDetails } = await getCurrentUser();
            
//             // Fetch user-specific stats using userId
//             const userStats = await api.get('gameApi', `/user-stats/${userId}`);
            
//             setUser({
//                 id: userId, // Store the userId
//                 username: signInDetails?.loginId,
//                 attributes: {
//                     email: signInDetails?.email
//                 }
//             });

//             setStats(userStats.data);
//             setLoading(false);
//         } catch (error) {
//             console.error('Error loading profile:', error);
//             setLoading(false);
//         }
//     };

//     const signOut = async () => {
//         try {
//             await amplifySignOut();
//             // You might want to redirect to login page or update app state
//         } catch (error) {
//             console.error('Error signing out:', error);
//         }
//     };

//     if (loading) {
//         return <div className="loading">Loading profile...</div>;
//     }

//     return (
//         <div className="profile">
//             <div className="profile-header">
//                 <h2>Adventurer Profile</h2>
//                 <button onClick={signOut} className="sign-out-button">
//                     Sign Out
//                 </button>
//             </div>
//             <div className="profile-content">
//                 <div className="profile-section">
//                     <h3>Player Info</h3>
//                     <p>Username: {user?.username}</p>
//                     <p>Email: {user?.attributes?.email}</p>
//                     {/* Optional: Display User ID for debugging or future use */}
//                     <p>User ID: {user?.id}</p>
//                 </div>
//                 <div className="profile-section">
//                     <h3>Game Statistics</h3>
//                     <div className="stats-grid">
//                         <div className="stat-item">
//                             <span className="stat-label">Games Played</span>
//                             <span className="stat-value">{stats?.gamesPlayed || 0}</span>
//                         </div>
//                         <div className="stat-item">
//                             <span className="stat-label">Highest Level</span>
//                             <span className="stat-value">{stats?.highestLevel || 1}</span>
//                         </div>
//                         <div className="stat-item">
//                             <span className="stat-label">Items Collected</span>
//                             <span className="stat-value">{stats?.itemsCollected || 0}</span>
//                         </div>
//                     </div>
//                 </div>
//                 <div className="profile-section">
//                     <h3>Achievements</h3>
//                     <div className="achievements-list">
//                         {stats?.achievements?.map((achievement, index) => (
//                             <div key={index} className="achievement-item">
//                                 <span className="achievement-icon">{achievement.icon}</span>
//                                 <span className="achievement-name">{achievement.name}</span>
//                                 <span className="achievement-description">{achievement.description}</span>
//                             </div>
//                         ))}
//                     </div>
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default Profile;

import React, { useState, useEffect, useCallback } from 'react'; 
import { getCurrentUser, signOut } from '@aws-amplify/auth'; 
import { get } from 'aws-amplify/api'; 
import '../styles/Profile.css';  

function Profile({ signOut: externalSignOut }) {     
    const [user, setUser] = useState(null);     
    const [stats, setStats] = useState(null);     
    const [loading, setLoading] = useState(true);      

    const parseResponse = (response) => {
        try {
            if (typeof response === 'string') {
                return JSON.parse(response);
            }
            
            if (response.body) {
                return typeof response.body === 'string' 
                    ? JSON.parse(response.body)
                    : response.body;
            }
            
            return response;
        } catch (error) {
            console.error('Response parsing error:', error);
            return response;
        }
    };

    const loadUserProfile = useCallback(async () => {         
        try {             
            const { userId, signInDetails } = await getCurrentUser();                          
            
            const requestConfig = {
                apiName: 'gameApi', 
                path: `/user-stats/${userId}`,
                options: {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            };

            const userStats = await get(requestConfig);
            
            const parsedStats = parseResponse(userStats);

            setUser({                 
                id: userId,                 
                username: signInDetails?.loginId,                 
                attributes: {                     
                    email: signInDetails?.email                 
                }             
            });              

            setStats(parsedStats);             
            setLoading(false);         
        } catch (error) {             
            console.error('Error loading profile:', error);             
            setLoading(false);         
        }     
    }, []);

    const handleSignOut = async () => {
        try {
            await signOut();
            if (externalSignOut) {
                externalSignOut();
            }
        } catch (error) {
            console.error('Error signing out:', error);
        }
    };

    useEffect(() => {         
        loadUserProfile();     
    }, [loadUserProfile]);      

    if (loading) {         
        return <div className="loading">Loading profile...</div>;     
    }      

    return (         
        <div className="profile">             
            <div className="profile-header">                 
                <h2>Adventurer Profile</h2>                 
                <button onClick={handleSignOut} className="sign-out-button">                     
                    Sign Out                 
                </button>             
            </div>             
            <div className="profile-content">                 
                <div className="profile-section">                     
                    <h3>Player Info</h3>                     
                    <p>Username: {user?.username || 'Unknown'}</p>                     
                    <p>Email: {user?.attributes?.email || 'No email'}</p>                     
                    <p>User ID: {user?.id}</p>                 
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
                                <span className="achievement-icon">{achievement.icon || '🏆'}</span>                                 
                                <span className="achievement-name">{achievement.name || 'Unnamed Achievement'}</span>                                 
                                <span className="achievement-description">{achievement.description || 'No description'}</span>                             
                            </div>                         ))}                     
                    </div>                 
                </div>             
            </div>         
        </div>     
    ); 
}  

export default Profile;