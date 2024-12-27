// import React, { useState, useEffect, useCallback } from 'react';
// import { get, post } from '@aws-amplify/api';
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/GameScreen.css';

// function GameScreen() {
//     const [currentScene, setCurrentScene] = useState(null);
//     const [choices, setChoices] = useState([]);
//     const [gameHistory, setGameHistory] = useState([]);
//     const [loading, setLoading] = useState(true);
//     const [gameStats, setGameStats] = useState({
//         health: 100,
//         experience: 0,
//         level: 1
//     });

//     const makeApiCall = useCallback(async (method, path, body = null) => {
//         try {
//             const { tokens } = await fetchAuthSession();

//             const requestConfig = {
//                 apiName: 'gameApi',
//                 path: path,
//                 options: {
//                     headers: {
//                         'Authorization': `Bearer ${tokens.idToken?.toString()}`,
//                         'Content-Type': 'application/json'
//                     },
//                     body: body ? JSON.stringify(body) : undefined
//                 }
//             };

//             console.log('Request Config:', requestConfig);
//             const response = await (method === 'GET' ? get(requestConfig) : post(requestConfig));
//             console.log('Response:', response);
            
//             return response;
//         } catch (error) {
//             console.error('API Call Error:', {
//                 message: error.message,
//                 status: error.status,
//                 name: error.name,
//                 details: error
//             });
//             throw error;
//         }
//     }, []);

//     const generateNewScene = useCallback(async () => {
//         try {
//             const response = await makeApiCall('POST', '/generate-story', {
//                 current_scene: 'start',
//                 player_choice: null,
//             });

//             console.log('Generate Scene Response:', response);
//             if (response?.body) {
//                 const data = JSON.parse(response.body);
//                 setCurrentScene(data.scene);
//                 setChoices(data.choices || []);
//             }
//             setLoading(false);
//         } catch (error) {
//             console.error('Error generating new scene:', error);
//             setLoading(false);
//         }
//     }, [makeApiCall]);

//     const loadGameState = useCallback(async () => {
//         try {
//             const response = await makeApiCall('GET', '/game-state');
//             console.log('Load Game State Response:', response);
            
//             if (response?.body) {
//                 const data = JSON.parse(response.body);
//                 setCurrentScene(data.currentScene);
//                 setGameHistory(data.playerChoices || []);
//                 setGameStats(data.stats || {
//                     health: 100,
//                     experience: 0,
//                     level: 1
//                 });
                
//                 if (!data.currentScene) {
//                     generateNewScene();
//                 } else {
//                     setLoading(false);
//                 }
//             } else {
//                 generateNewScene();
//             }
//         } catch (error) {
//             console.error('Error loading game state:', error);
//             setLoading(false);
//         }
//     }, [makeApiCall, generateNewScene]);

//     useEffect(() => {
//         loadGameState();
//     }, [loadGameState]);

//     const makeChoice = async (choice) => {
//         try {
//             setLoading(true);
            
//             const response = await makeApiCall('POST', '/generate-story', {
//                 current_scene: currentScene,
//                 player_choice: choice,
//             });

//             console.log('Make Choice Response:', response);
//             if (response?.body) {
//                 const data = JSON.parse(response.body);
//                 setCurrentScene(data.scene);
//                 setChoices(data.choices || []);
                
//                 const newStats = {
//                     ...gameStats,
//                     experience: gameStats.experience + 10,
//                     health: Math.max(0, Math.min(100, gameStats.health + (data.healthChange || 0)))
//                 };

//                 if (newStats.experience >= newStats.level * 100) {
//                     newStats.level += 1;
//                 }

//                 setGameStats(newStats);
                
//                 await makeApiCall('POST', '/save-game', {
//                     currentScene: data.scene,
//                     playerChoices: [...gameHistory, choice],
//                     stats: newStats
//                 });

//                 setGameHistory([...gameHistory, choice]);
//             }
//             setLoading(false);
//         } catch (error) {
//             console.error('Error processing choice:', error);
//             setLoading(false);
//         }
//     };

//     if (loading) {
//         return <div className="loading">Loading your adventure...</div>;
//     }

//     return (
//         <div className="game-screen">
//             <div className="game-stats">
//                 <div className="stat">❤️ Health: {gameStats.health}</div>
//                 <div className="stat">⭐ Level: {gameStats.level}</div>
//                 <div className="stat">📈 XP: {gameStats.experience}</div>
//             </div>
//             <div className="scene-container">
//                 <div className="scene-description">
//                     <p>{currentScene}</p>
//                 </div>
//                 <div className="choices">
//                     {choices.map((choice, index) => (
//                         <button
//                             key={index}
//                             onClick={() => makeChoice(choice)}
//                             className="choice-button"
//                             disabled={loading}
//                         >
//                             {choice}
//                         </button>
//                     ))}
//                 </div>
//             </div>
//             <div className="game-history">
//                 <h3>Adventure Log</h3>
//                 <div className="history-list">
//                     {gameHistory.map((choice, index) => (
//                         <div key={index} className="history-item">
//                             {choice}
//                         </div>
//                     ))}
//                 </div>
//             </div>
//         </div>
//     );
// }

// export default GameScreen;

import React, { useState, useEffect, useCallback } from 'react';
import { generateClient } from 'aws-amplify/api';
import { fetchAuthSession } from '@aws-amplify/auth';
import '../styles/GameScreen.css';

function GameScreen() {
    const client = generateClient();
    const [gameState, setGameState] = useState({
        scene_description: "Beginning your adventure...",
        choices: [],
        environment: {
            items: [],
            npcs: [],
            events: []
        }
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const makeApiCall = useCallback(async (method, path, body = null) => {
        try {
            console.log('Attempting API call:', { method, path, body });
            
            const session = await fetchAuthSession();
            console.log('Session retrieved:', session);

            const requestConfig = {
                apiName: 'gameApi',
                path: path,
                options: {
                    headers: {
                        'Authorization': `Bearer ${session.tokens.idToken?.toString()}`,
                        'Content-Type': 'application/json'
                    },
                    body: body ? JSON.stringify(body) : undefined
                }
            };

            console.log('Full Request Config:', JSON.stringify(requestConfig, null, 2));

            let response;
            try {
                response = method === 'GET' 
                    ? await client.get(requestConfig) 
                    : await client.post(requestConfig);
            } catch (apiError) {
                console.error('Detailed API Error:', {
                    message: apiError.message,
                    name: apiError.name,
                    stack: apiError.stack,
                    config: requestConfig
                });
                throw apiError;
            }

            console.log('Full Response:', response);
            return response;
        } catch (error) {
            console.error('Comprehensive API Call Error:', {
                message: error.message,
                name: error.name,
                stack: error.stack
            });
            throw error;
        }
    }, [client]);

    const generateNewScene = useCallback(async () => {
        try {
            setLoading(true);
            const response = await makeApiCall('POST', '/generate-story', {
                current_scene: 'start',
                player_choice: null,
            });

            console.log('Generate Scene Full Response:', response);

            // Extremely flexible parsing
            let data;
            if (typeof response === 'string') {
                try {
                    data = JSON.parse(response);
                } catch {
                    data = response;
                }
            } else if (response.body) {
                try {
                    data = typeof response.body === 'string' 
                        ? JSON.parse(response.body) 
                        : response.body;
                } catch {
                    data = response.body;
                }
            } else {
                data = response;
            }

            console.log('Parsed Scene Data:', JSON.stringify(data, null, 2));

            // Validate the data structure with extensive fallbacks
            const validatedGameState = {
                scene_description: 
                    data.scene_description || 
                    data.currentScene || 
                    data.scene || 
                    'Unable to generate scene',
                choices: 
                    data.choices || 
                    data.options || 
                    (typeof data === 'object' && Object.keys(data).filter(k => k.includes('choice'))) || 
                    [],
                environment: 
                    data.environment || {
                        items: [],
                        npcs: [],
                        events: []
                    }
            };

            console.log('Validated Game State:', JSON.stringify(validatedGameState, null, 2));

            setGameState(validatedGameState);
            setLoading(false);
        } catch (error) {
            console.error('Scene Generation Full Error:', {
                message: error.message,
                name: error.name,
                stack: error.stack
            });
            
            setGameState({
                scene_description: 'An unexpected error occurred. Please try again.',
                choices: [{ text: 'Retry', consequences: {} }],
                environment: { items: [], npcs: [], events: [] }
            });
            setError(error);
            setLoading(false);
        }
    }, [makeApiCall]);

    const makeChoice = async (choice) => {
        try {
            setLoading(true);
            const response = await makeApiCall('POST', '/generate-story', {
                current_scene: gameState.scene_description,
                player_choice: choice,
            });

            // Similar parsing logic as generateNewScene
            let data;
            if (typeof response === 'string') {
                try {
                    data = JSON.parse(response);
                } catch {
                    data = response;
                }
            } else if (response.body) {
                try {
                    data = typeof response.body === 'string' 
                        ? JSON.parse(response.body) 
                        : response.body;
                } catch {
                    data = response.body;
                }
            } else {
                data = response;
            }

            const validatedGameState = {
                scene_description: 
                    data.scene_description || 
                    data.currentScene || 
                    data.scene || 
                    'Unable to generate scene',
                choices: 
                    data.choices || 
                    data.options || 
                    (typeof data === 'object' && Object.keys(data).filter(k => k.includes('choice'))) || 
                    [],
                environment: 
                    data.environment || {
                        items: [],
                        npcs: [],
                        events: []
                    }
            };

            setGameState(validatedGameState);
            setLoading(false);
        } catch (error) {
            console.error('Choice Processing Error:', error);
            setLoading(false);
        }
    };

    useEffect(() => {
        generateNewScene();
    }, [generateNewScene]);

    if (loading) {
        return <div className="loading">Loading your adventure...</div>;
    }

    if (error) {
        return (
            <div className="error-container">
                <h2>An Error Occurred</h2>
                <p>Unable to load the game. Please try again later.</p>
                <pre>{JSON.stringify(error, null, 2)}</pre>
                <button onClick={generateNewScene}>Retry</button>
            </div>
        );
    }

    return (
        <div className="game-screen">
            <div className="scene-container">
                <div className="scene-description">
                    <p>{gameState.scene_description}</p>
                </div>
                <div className="choices">
                    {gameState.choices.map((choice, index) => (
                        <button
                            key={index}
                            onClick={() => makeChoice(typeof choice === 'string' ? choice : choice.text)}
                            className="choice-button"
                            disabled={loading}
                        >
                            {typeof choice === 'string' ? choice : choice.text}
                        </button>
                    ))}
                </div>
            </div>
            {gameState.environment.items && gameState.environment.items.length > 0 && (
                <div className="environment-items">
                    <h3>Items in the Environment:</h3>
                    {gameState.environment.items.map((item, index) => (
                        <div key={index} className="environment-item">
                            {typeof item === 'string' ? item : item.name}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default GameScreen;