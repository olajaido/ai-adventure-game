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

// import React, { useState, useEffect, useCallback } from 'react'; 
// import { getCurrentUser, signOut } from '@aws-amplify/auth'; 
// import { get } from 'aws-amplify/api'; 
// import '../styles/Profile.css';  

// function Profile({ signOut: externalSignOut }) {     
//     const [user, setUser] = useState(null);     
//     const [stats, setStats] = useState(null);     
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const parseResponse = useCallback((response) => {
//         try {
//             console.log('Raw Response:', response);
            
//             // Handle different response structures
//             if (typeof response === 'string') {
//                 return JSON.parse(response);
//             }
            
//             // Check for body in response
//             if (response.body) {
//                 const body = typeof response.body === 'string' 
//                     ? JSON.parse(response.body)
//                     : response.body;
                
//                 console.log('Parsed Body:', body);
//                 return body;
//             }
            
//             // If response is already an object
//             return response;
//         } catch (error) {
//             console.error('Response parsing error:', error);
//             return response;
//         }
//     }, []);

//     const loadUserProfile = useCallback(async () => {         
//         try {             
//             const { userId, signInDetails } = await getCurrentUser();                          
            
//             const requestConfig = {
//                 apiName: 'gameApi', 
//                 path: `/user-stats/${userId}`,
//                 options: {
//                     headers: {
//                         'Content-Type': 'application/json'
//                     }
//                 }
//             };

//             console.log('Detailed Request Config:', JSON.stringify(requestConfig, null, 2));

//             try {
//                 const userStats = await get(requestConfig);

//                 console.log('Detailed API Response:', JSON.stringify(userStats, null, 2));
                
//                 const parsedStats = parseResponse(userStats);

//                 console.log('Parsed User Stats:', parsedStats);

//                 setUser({                 
//                     id: userId,                 
//                     username: signInDetails?.loginId,                 
//                     attributes: {                     
//                         email: signInDetails?.email                 
//                     }             
//                 });              

//                 setStats(parsedStats);             
//                 setLoading(false);
//             } catch (apiError) {
//                 console.error('Detailed API Error:', {
//                     message: apiError.message,
//                     name: apiError.name,
//                     stack: apiError.stack
//                 });
//                 setError(apiError);
//                 setLoading(false);
//             }
//         } catch (error) {             
//             console.error('Authentication or Profile Load Error:', {
//                 message: error.message,
//                 name: error.name,
//                 stack: error.stack
//             });
//             setError(error);
//             setLoading(false);
//         }     
//     }, [parseResponse]);

//     useEffect(() => {         
//         loadUserProfile();     
//     }, [loadUserProfile]);      

//     const handleSignOut = async () => {
//         try {
//             await signOut();
//             if (externalSignOut) {
//                 externalSignOut();
//             }
//         } catch (error) {
//             console.error('Error signing out:', error);
//         }
//     };

//     const retryLoadProfile = () => {
//         setError(null);
//         loadUserProfile();
//     };

//     if (loading) {         
//         return <div className="loading">Loading profile...</div>;     
//     }      

//     if (error) {
//         return (
//             <div className="error-container">
//                 <h2>An Error Occurred</h2>
//                 <p>Unable to load profile. Please try again.</p>
//                 <pre>{JSON.stringify(error, null, 2)}</pre>
//                 <button onClick={retryLoadProfile}>Retry</button>
//             </div>
//         );
//     }

//     return (         
//         <div className="profile">             
//             <div className="profile-header">                 
//                 <h2>Adventurer Profile</h2>                 
//                 <button onClick={handleSignOut} className="sign-out-button">                     
//                     Sign Out                 
//                 </button>             
//             </div>             
//             <div className="profile-content">                 
//                 <div className="profile-section">                     
//                     <h3>Player Info</h3>                     
//                     <p>Username: {user?.username || 'Unknown'}</p>                     
//                     <p>Email: {user?.attributes?.email || 'No email'}</p>                     
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
//                                 <span className="achievement-icon">{achievement.icon || '🏆'}</span>                                 
//                                 <span className="achievement-name">{achievement.name || 'Unnamed Achievement'}</span>                                 
//                                 <span className="achievement-description">{achievement.description || 'No description'}</span>                             
//                             </div>                         ))}                     
//                     </div>                 
//                 </div>             
//             </div>         
//         </div>     
//     ); 
// }  

// export default Profile;

import React, { useState, useEffect, useCallback } from 'react';
import { get } from 'aws-amplify/api';
import { fetchAuthSession, getCurrentUser } from '@aws-amplify/auth';
import '../styles/Profile.css';

function Profile({ signOut: externalSignOut }) {
    const [user, setUser] = useState(null);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const loadUserProfile = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);

            // Get current user and auth session
            const currentUser = await getCurrentUser();
            const session = await fetchAuthSession();
            const idToken = session.tokens?.idToken?.toString();

            if (!idToken) {
                throw new Error('Authentication required');
            }

            const response = await get({
                apiName: 'gameApi',
                path: `/user-stats/${currentUser.userId}`,
                options: {
                    headers: {
                        Authorization: `Bearer ${idToken}`
                    }
                }
            }).response;

            // Handle ReadableStream in the response body
            let jsonData;
            if (response.body instanceof ReadableStream) {
                const reader = response.body.getReader();
                let result = '';
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    result += new TextDecoder().decode(value);
                }
                try {
                    jsonData = JSON.parse(result);
                } catch (e) {
                    console.error('Failed to parse response:', e);
                    throw new Error('Invalid response format');
                }
            } else {
                jsonData = response.body;
            }

            console.log('Profile Response:', jsonData);

            // Set user data
            setUser({
                id: currentUser.userId,
                username: currentUser.username,
                attributes: {
                    email: currentUser.signInDetails?.email
                }
            });

            // Set stats with default values if data is missing
            setStats({
                gamesPlayed: jsonData?.stats?.gamesPlayed || 0,
                highestLevel: jsonData?.stats?.highestLevel || 1,
                itemsCollected: jsonData?.stats?.itemsCollected || 0,
                experience: jsonData?.stats?.experience || 0,
                level: jsonData?.stats?.level || 1,
                rank: jsonData?.stats?.rank || 'Novice Adventurer',
                playTime: jsonData?.stats?.playTime || 0,
                achievements: Array.isArray(jsonData?.stats?.achievements) 
                    ? jsonData.stats.achievements.map(achievement => ({
                        name: achievement.name || 'Unknown Achievement',
                        description: achievement.description || 'No description available',
                        icon: achievement.icon || '🏆',
                        dateEarned: achievement.dateEarned || null,
                        progress: achievement.progress || 100
                    }))
                    : []
            });

        } catch (error) {
            console.error('Profile Load Error:', error);
            setError(error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadUserProfile();
    }, [loadUserProfile]);

    const handleSignOut = async () => {
        try {
            await externalSignOut();
        } catch (error) {
            console.error('Sign Out Error:', error);
        }
    };

    if (loading) {
        return <div className="loading">Loading profile...</div>;
    }

    if (error) {
        return (
            <div className="error-container">
                <h2>An Error Occurred</h2>
                <p>{error.message || 'Unable to load profile. Please try again.'}</p>
                <button onClick={loadUserProfile} className="retry-button">
                    Retry
                </button>
            </div>
        );
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
                    <div className="player-info">
                        <p>Username: {user?.username || 'Unknown'}</p>
                        <p>Email: {user?.attributes?.email || 'No email'}</p>
                        <p>Rank: {stats?.rank || 'Novice Adventurer'}</p>
                        <p>Level: {stats?.level || 1}</p>
                        <p>Experience: {stats?.experience || 0} XP</p>
                    </div>
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
                        {stats?.playTime !== undefined && (
                            <div className="stat-item">
                                <span className="stat-label">Play Time</span>
                                <span className="stat-value">
                                    {`${Math.floor(stats.playTime / 60)}h ${stats.playTime % 60}m`}
                                </span>
                            </div>
                        )}
                    </div>
                </div>

                {stats?.achievements?.length > 0 && (
                    <div className="profile-section">
                        <h3>Achievements</h3>
                        <div className="achievements-list">
                            {stats.achievements.map((achievement, index) => (
                                <div key={index} className="achievement-item">
                                    <span className="achievement-icon">
                                        {achievement.icon}
                                    </span>
                                    <div className="achievement-info">
                                        <span className="achievement-name">
                                            {achievement.name}
                                        </span>
                                        <span className="achievement-description">
                                            {achievement.description}
                                        </span>
                                        {achievement.dateEarned && (
                                            <span className="achievement-date">
                                                Earned: {new Date(achievement.dateEarned).toLocaleDateString()}
                                            </span>
                                        )}
                                        {achievement.progress < 100 && (
                                            <div className="achievement-progress">
                                                <div 
                                                    className="progress-bar"
                                                    style={{ width: `${achievement.progress}%` }}
                                                />
                                                <span className="progress-text">
                                                    {achievement.progress}%
                                                </span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Profile;