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
import { get, post } from 'aws-amplify/api';
import { fetchAuthSession } from '@aws-amplify/auth';
import '../styles/GameScreen.css';

function GameScreen() {
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

    const parseResponse = useCallback((response) => {
        try {
            console.log('Parsing Response:', response);
            
            if (typeof response === 'string') {
                return JSON.parse(response);
            }
            
            if (response.body) {
                const parsedBody = typeof response.body === 'string' 
                    ? JSON.parse(response.body)
                    : response.body;
                
                console.log('Parsed Body:', parsedBody);
                return parsedBody;
            }
            
            return response;
        } catch (error) {
            console.error('Response parsing error:', error);
            return response;
        }
    }, []);

    const makeApiCall = useCallback(async (method, path, body = null) => {
        try {
            const session = await fetchAuthSession();
            
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

            console.log('Detailed Request Config:', JSON.stringify(requestConfig, null, 2));

            try {
                const response = method === 'GET' 
                    ? await get(requestConfig)
                    : await post(requestConfig);

                console.log('Detailed API Response:', JSON.stringify(response, null, 2));
                return response;
            } catch (apiError) {
                console.error('Detailed API Error:', {
                    message: apiError.message,
                    name: apiError.name,
                    stack: apiError.stack,
                    config: requestConfig
                });
                throw apiError;
            }
        } catch (error) {
            console.error('Authentication or API Call Error:', {
                message: error.message,
                name: error.name,
                stack: error.stack
            });
            throw error;
        }
    }, []);

    const generateNewScene = useCallback(async () => {
        try {
            setLoading(true);
            const response = await makeApiCall('POST', '/generate-story', {
                current_scene: 'start',
                player_choice: null,
            });

            const data = parseResponse(response);

            console.log('Parsed Scene Data:', data);

            const validatedGameState = {
                scene_description: 
                    data.scene_description || 
                    data.currentScene || 
                    data.scene || 
                    'Unable to generate scene',
                choices: 
                    data.choices || 
                    data.options || 
                    [],
                environment: 
                    data.environment || {
                        items: [],
                        npcs: [],
                        events: []
                    }
            };

            console.log('Validated Game State:', validatedGameState);

            setGameState(validatedGameState);
            setLoading(false);
        } catch (error) {
            console.error('Scene Generation Error:', error);
            setGameState({
                scene_description: 'An error occurred. Please try again.',
                choices: [{ text: 'Retry', consequences: {} }],
                environment: { items: [], npcs: [], events: [] }
            });
            setError(error);
            setLoading(false);
        }
    }, [makeApiCall, parseResponse]);

    const makeChoice = useCallback(async (choice) => {
        try {
            setLoading(true);
            const response = await makeApiCall('POST', '/generate-story', {
                current_scene: gameState.scene_description,
                player_choice: choice,
            });

            const data = parseResponse(response);

            const validatedGameState = {
                scene_description: 
                    data.scene_description || 
                    data.currentScene || 
                    data.scene || 
                    'Unable to generate scene',
                choices: 
                    data.choices || 
                    data.options || 
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
    }, [makeApiCall, parseResponse, gameState.scene_description]);

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