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

// import React, { useState, useEffect, useCallback } from 'react';
// import { get, post } from 'aws-amplify/api';
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/GameScreen.css';

// function GameScreen() {
//     const [gameState, setGameState] = useState({
//         scene_description: "Beginning your adventure...",
//         choices: [],
//         environment: {
//             items: [],
//             npcs: [],
//             events: []
//         }
//     });
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

//     const makeApiCall = useCallback(async (method, path, body = null) => {
//         try {
//             const session = await fetchAuthSession();
            
//             const requestConfig = {
//                 apiName: 'gameApi',
//                 path: path,
//                 options: {
//                     headers: {
//                         'Authorization': `Bearer ${session.tokens.idToken?.toString()}`,
//                         'Content-Type': 'application/json'
//                     },
//                     body: body ? JSON.stringify(body) : undefined
//                 }
//             };

//             console.log('Detailed Request Config:', JSON.stringify(requestConfig, null, 2));

//             const response = method === 'GET' 
//                 ? await get(requestConfig)
//                 : await post(requestConfig);

//             console.log('Detailed API Response:', JSON.stringify(response, null, 2));
//             return response;
//         } catch (error) {
//             console.error('API Call Error:', {
//                 message: error.message,
//                 name: error.name,
//                 stack: error.stack
//             });
//             throw error;
//         }
//     }, []);

//     const generateNewScene = useCallback(async () => {
//         try {
//             setLoading(true);
//             const response = await makeApiCall('POST', '/generate-story', {
//                 current_scene: 'start',
//                 player_choice: null,
//             });

//             const data = parseResponse(response);

//             console.log('Parsed Scene Data:', data);

//             const validatedGameState = {
//                 scene_description: 
//                     data.scene_description || 
//                     data.currentScene || 
//                     data.scene || 
//                     'Unable to generate scene',
//                 choices: 
//                     data.choices || 
//                     data.options || 
//                     [],
//                 environment: 
//                     data.environment || {
//                         items: [],
//                         npcs: [],
//                         events: []
//                     }
//             };

//             console.log('Validated Game State:', validatedGameState);

//             setGameState(validatedGameState);
//             setLoading(false);
//         } catch (error) {
//             console.error('Scene Generation Error:', error);
//             setGameState({
//                 scene_description: 'An error occurred. Please try again.',
//                 choices: [{ text: 'Retry', consequences: {} }],
//                 environment: { items: [], npcs: [], events: [] }
//             });
//             setError(error);
//             setLoading(false);
//         }
//     }, [makeApiCall, parseResponse]);

//     const makeChoice = useCallback(async (choice) => {
//         try {
//             setLoading(true);
//             const response = await makeApiCall('POST', '/generate-story', {
//                 current_scene: gameState.scene_description,
//                 player_choice: choice,
//             });

//             const data = parseResponse(response);

//             const validatedGameState = {
//                 scene_description: 
//                     data.scene_description || 
//                     data.currentScene || 
//                     data.scene || 
//                     'Unable to generate scene',
//                 choices: 
//                     data.choices || 
//                     data.options || 
//                     [],
//                 environment: 
//                     data.environment || {
//                         items: [],
//                         npcs: [],
//                         events: []
//                     }
//             };

//             setGameState(validatedGameState);
//             setLoading(false);
//         } catch (error) {
//             console.error('Choice Processing Error:', error);
//             setLoading(false);
//         }
//     }, [makeApiCall, parseResponse, gameState.scene_description]);

//     useEffect(() => {
//         generateNewScene();
//     }, [generateNewScene]);

//     if (loading) {
//         return <div className="loading">Loading your adventure...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <h2>An Error Occurred</h2>
//                 <p>Unable to load the game. Please try again later.</p>
//                 <pre>{JSON.stringify(error, null, 2)}</pre>
//                 <button onClick={generateNewScene}>Retry</button>
//             </div>
//         );
//     }

//     return (
//         <div className="game-screen">
//             <div className="scene-container">
//                 <div className="scene-description">
//                     <p>{gameState.scene_description}</p>
//                 </div>
//                 <div className="choices">
//                     {gameState.choices.map((choice, index) => (
//                         <button
//                             key={index}
//                             onClick={() => makeChoice(typeof choice === 'string' ? choice : choice.text)}
//                             className="choice-button"
//                             disabled={loading}
//                         >
//                             {typeof choice === 'string' ? choice : choice.text}
//                         </button>
//                     ))}
//                 </div>
//             </div>
//             {gameState.environment.items && gameState.environment.items.length > 0 && (
//                 <div className="environment-items">
//                     <h3>Items in the Environment:</h3>
//                     {gameState.environment.items.map((item, index) => (
//                         <div key={index} className="environment-item">
//                             {typeof item === 'string' ? item : item.name}
//                         </div>
//                     ))}
//                 </div>
//             )}
//         </div>
//     );
// }

// export default GameScreen;

// import React, { useState, useEffect, useCallback } from 'react';
// import { post } from 'aws-amplify/api';
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/GameScreen.css';

// function GameScreen() {
//     const [gameState, setGameState] = useState({
//         scene_description: "Beginning your adventure...",
//         choices: [],
//         environment: {
//             items: [],
//             npcs: [],
//             events: []
//         }
//     });
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const makeApiCall = useCallback(async (body) => {
//         try {
//             const session = await fetchAuthSession();
//             const idToken = session.tokens?.idToken?.toString();
            
//             if (!idToken) {
//                 throw new Error('Authentication required');
//             }

//             const result = await post({
//                 apiName: 'gameApi',
//                 path: '/generate-story',
//                 options: {
//                     headers: {
//                         Authorization: `Bearer ${idToken}`
//                     },
//                     body: body
//                 }
//             }).response;

//             // Parse the response if needed
//             let data = result;
//             if (typeof result === 'string') {
//                 try {
//                     data = JSON.parse(result);
//                 } catch (e) {
//                     console.error('Failed to parse response:', e);
//                     throw new Error('Invalid response format');
//                 }
//             }

//             return data;
//         } catch (error) {
//             // Log detailed error information
//             console.error('API Error Details:', {
//                 message: error.message,
//                 name: error.name,
//                 code: error.code || error.statusCode,
//                 stack: error.stack
//             });
            
//             if (error.message.includes('Unauthorized') || error.statusCode === 401) {
//                 throw new Error('Session expired. Please sign in again.');
//             }
            
//             throw error;
//         }
//     }, []);

//     const generateNewScene = useCallback(async () => {
//         try {
//             setLoading(true);
//             setError(null);

//             const data = await makeApiCall({
//                 current_scene: 'start',
//                 player_choice: null
//             });

//             const validatedGameState = {
//                 scene_description: data?.scene_description || 
//                                  data?.currentScene || 
//                                  data?.scene || 
//                                  'Start your adventure...',
//                 choices: Array.isArray(data?.choices) ? data.choices :
//                         Array.isArray(data?.options) ? data.options : 
//                         [{ text: 'Begin Adventure', consequences: {} }],
//                 environment: {
//                     items: Array.isArray(data?.environment?.items) ? data.environment.items : [],
//                     npcs: Array.isArray(data?.environment?.npcs) ? data.environment.npcs : [],
//                     events: Array.isArray(data?.environment?.events) ? data.environment.events : []
//                 }
//             };

//             setGameState(validatedGameState);
//         } catch (error) {
//             console.error('Scene Generation Error:', error);
//             setError(error);
//             setGameState(prev => ({
//                 ...prev,
//                 scene_description: error.message || 'An error occurred. Please try again.',
//                 choices: [{ text: 'Retry', consequences: {} }]
//             }));
//         } finally {
//             setLoading(false);
//         }
//     }, [makeApiCall]);

//     const makeChoice = useCallback(async (choice) => {
//         try {
//             setLoading(true);
//             setError(null);

//             const data = await makeApiCall({
//                 current_scene: gameState.scene_description,
//                 player_choice: choice
//             });

//             const validatedGameState = {
//                 scene_description: data?.scene_description || 
//                                  data?.currentScene || 
//                                  data?.scene || 
//                                  'Continue your adventure...',
//                 choices: Array.isArray(data?.choices) ? data.choices :
//                         Array.isArray(data?.options) ? data.options : 
//                         [{ text: 'Continue', consequences: {} }],
//                 environment: {
//                     items: Array.isArray(data?.environment?.items) ? data.environment.items : [],
//                     npcs: Array.isArray(data?.environment?.npcs) ? data.environment.npcs : [],
//                     events: Array.isArray(data?.environment?.events) ? data.environment.events : []
//                 }
//             };

//             setGameState(validatedGameState);
//         } catch (error) {
//             console.error('Choice Processing Error:', error);
//             setError(error);
//             setGameState(prev => ({
//                 ...prev,
//                 choices: [{ text: 'Retry', consequences: {} }]
//             }));
//         } finally {
//             setLoading(false);
//         }
//     }, [makeApiCall, gameState.scene_description]);

//     useEffect(() => {
//         generateNewScene();
//     }, [generateNewScene]);

//     if (loading) {
//         return <div className="loading">Loading your adventure...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <h2>An Error Occurred</h2>
//                 <p>{error.message || 'Unable to load the game. Please try again later.'}</p>
//                 <button onClick={generateNewScene} className="retry-button">
//                     Retry
//                 </button>
//             </div>
//         );
//     }

//     return (
//         <div className="game-screen">
//             <div className="scene-container">
//                 <div className="scene-description">
//                     <p>{gameState.scene_description}</p>
//                 </div>
//                 <div className="choices">
//                     {gameState.choices.map((choice, index) => (
//                         <button
//                             key={index}
//                             onClick={() => makeChoice(typeof choice === 'string' ? choice : choice.text)}
//                             className="choice-button"
//                             disabled={loading}
//                         >
//                             {typeof choice === 'string' ? choice : choice.text}
//                         </button>
//                     ))}
//                 </div>
//             </div>
//             {gameState.environment.items?.length > 0 && (
//                 <div className="environment-items">
//                     <h3>Items in the Environment:</h3>
//                     {gameState.environment.items.map((item, index) => (
//                         <div key={index} className="environment-item">
//                             {typeof item === 'string' ? item : item.name}
//                         </div>
//                     ))}
//                 </div>
//             )}
//             {gameState.environment.npcs?.length > 0 && (
//                 <div className="environment-npcs">
//                     <h3>Characters Present:</h3>
//                     {gameState.environment.npcs.map((npc, index) => (
//                         <div key={index} className="environment-npc">
//                             {typeof npc === 'string' ? npc : npc.name}
//                         </div>
//                     ))}
//                 </div>
//             )}
//             {gameState.environment.events?.length > 0 && (
//                 <div className="environment-events">
//                     <h3>Current Events:</h3>
//                     {gameState.environment.events.map((event, index) => (
//                         <div key={index} className="environment-event">
//                             {typeof event === 'string' ? event : event.description}
//                         </div>
//                     ))}
//                 </div>
//             )}
//         </div>
//     );
// }

// export default GameScreen;

// import React, { useState, useEffect, useCallback } from 'react';
// import { post } from 'aws-amplify/api';
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/GameScreen.css';

// function GameScreen() {
//     const [gameState, setGameState] = useState({
//         scene_description: "Beginning your adventure...",
//         choices: [],
//         environment: {
//             items: [],
//             npcs: [],
//             events: []
//         }
//     });
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const makeApiCall = useCallback(async (body) => {
//         try {
//             const session = await fetchAuthSession();
//             const idToken = session.tokens?.idToken?.toString();
            
//             if (!idToken) {
//                 throw new Error('Authentication required');
//             }

//             console.log('Making API call with body:', body);

//             const response = await post({
//                 apiName: 'gameApi',
//                 path: '/generate-story',
//                 options: {
//                     headers: {
//                         Authorization: `Bearer ${idToken}`
//                     },
//                     body: body
//                 }
//             }).response;

//             // Handle ReadableStream in the response body
//             let jsonData;
//             if (response.body instanceof ReadableStream) {
//                 const reader = response.body.getReader();
//                 let result = '';
//                 while (true) {
//                     const { done, value } = await reader.read();
//                     if (done) break;
//                     result += new TextDecoder().decode(value);
//                 }
//                 try {
//                     jsonData = JSON.parse(result);
//                 } catch (e) {
//                     console.error('Failed to parse response stream:', e);
//                     throw new Error('Invalid response format');
//                 }
//             } else {
//                 jsonData = response.body;
//             }

//             console.log('Processed API Response:', jsonData);
//             return jsonData;
//         } catch (error) {
//             console.error('API Error Details:', {
//                 message: error.message,
//                 name: error.name,
//                 code: error.code || error.statusCode,
//                 stack: error.stack
//             });
//             throw error;
//         }
//     }, []);

//     const processApiResponse = useCallback((data) => {
//         if (!data || !data.scene) {
//             throw new Error('Invalid scene data');
//         }

//         return {
//             scene_description: data.scene.description || 'No description available',
//             choices: Array.isArray(data.scene.choices) ? 
//                     data.scene.choices.map(choice => ({
//                         text: choice.text || choice,
//                         consequences: choice.consequences || {}
//                     })) :
//                     [{ text: 'Continue', consequences: {} }],
//             environment: {
//                 items: Array.isArray(data.scene.items) ? data.scene.items : [],
//                 npcs: Array.isArray(data.scene.npcs) ? data.scene.npcs : [],
//                 events: Array.isArray(data.scene.events) ? data.scene.events : []
//             }
//         };
//     }, []);

//     const generateNewScene = useCallback(async () => {
//         try {
//             setLoading(true);
//             setError(null);

//             const data = await makeApiCall({
//                 current_scene: 'start',
//                 player_choice: null
//             });

//             console.log('New scene data received:', data);
//             const validatedGameState = processApiResponse(data);
//             console.log('Validated new scene state:', validatedGameState);

//             setGameState(validatedGameState);
//         } catch (error) {
//             console.error('Scene Generation Error:', error);
//             setError(error);
//             setGameState(prev => ({
//                 ...prev,
//                 scene_description: error.message || 'An error occurred. Please try again.',
//                 choices: [{ text: 'Retry', consequences: {} }]
//             }));
//         } finally {
//             setLoading(false);
//         }
//     }, [makeApiCall, processApiResponse]);

//     const makeChoice = useCallback(async (choice, currentGameState) => {
//         try {
//             console.log('Making choice with:', { choice, currentGameState });
//             setLoading(true);
//             setError(null);

//             const data = await makeApiCall({
//                 current_scene: currentGameState.scene_description,
//                 player_choice: choice
//             });

//             console.log('Choice response data:', data);
//             const validatedGameState = processApiResponse(data);
//             console.log('Validated choice game state:', validatedGameState);

//             setGameState(validatedGameState);
//         } catch (error) {
//             console.error('Choice Processing Error:', error);
//             setError(error);
//             setGameState(prev => ({
//                 ...prev,
//                 choices: [{ text: 'Retry', consequences: {} }]
//             }));
//         } finally {
//             setLoading(false);
//         }
//     }, [makeApiCall, processApiResponse]);

//     useEffect(() => {
//         generateNewScene();
//     }, [generateNewScene]);

//     const handleChoice = useCallback((choice) => {
//         makeChoice(choice, gameState);
//     }, [makeChoice, gameState]);

//     if (loading) {
//         return <div className="loading">Loading your adventure...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <h2>An Error Occurred</h2>
//                 <p>{error.message || 'Unable to load the game. Please try again later.'}</p>
//                 <button onClick={generateNewScene} className="retry-button">
//                     Retry
//                 </button>
//             </div>
//         );
//     }

//     return (
//         <div className="game-screen">
//             <div className="scene-container">
//                 <div className="scene-description">
//                     <p>{gameState.scene_description}</p>
//                 </div>
//                 <div className="choices">
//                     {gameState.choices.map((choice, index) => (
//                         <button
//                             key={index}
//                             onClick={() => handleChoice(choice.text)}
//                             className="choice-button"
//                             disabled={loading}
//                         >
//                             {choice.text}
//                         </button>
//                     ))}
//                 </div>
//             </div>
//             {gameState.environment.items?.length > 0 && (
//                 <div className="environment-items">
//                     <h3>Items in the Environment:</h3>
//                     {gameState.environment.items.map((item, index) => (
//                         <div key={index} className="environment-item">
//                             {typeof item === 'string' ? item : item.name}
//                         </div>
//                     ))}
//                 </div>
//             )}
//             {gameState.environment.npcs?.length > 0 && (
//                 <div className="environment-npcs">
//                     <h3>Characters Present:</h3>
//                     {gameState.environment.npcs.map((npc, index) => (
//                         <div key={index} className="environment-npc">
//                             {typeof npc === 'string' ? npc : npc.name}
//                         </div>
//                     ))}
//                 </div>
//             )}
//             {gameState.environment.events?.length > 0 && (
//                 <div className="environment-events">
//                     <h3>Current Events:</h3>
//                     {gameState.environment.events.map((event, index) => (
//                         <div key={index} className="environment-event">
//                             {typeof event === 'string' ? event : event.description}
//                         </div>
//                     ))}
//                 </div>
//             )}
//         </div>
//     );
// }

// export default GameScreen;

// working before updating the code with cache and dynamoDB

// import React, { useState, useEffect, useCallback } from 'react';
// import { post } from 'aws-amplify/api';
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/GameScreen.css';

// function GameScreen() {
//     const [gameState, setGameState] = useState({
//         scene_description: "Beginning your adventure...",
//         scene_id: null,
//         choices: [],
//         environment: {
//             items: [],
//             npcs: [],
//             events: []
//         }
//     });
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const makeApiCall = useCallback(async (body) => {
//         try {
//             const session = await fetchAuthSession();
//             const idToken = session.tokens?.idToken?.toString();
            
//             if (!idToken) {
//                 throw new Error('Authentication required');
//             }

//             const response = await post({
//                 apiName: 'gameApi',
//                 path: '/generate-story',
//                 options: {
//                     headers: {
//                         Authorization: `Bearer ${idToken}`
//                     },
//                     body: body
//                 }
//             }).response;

//             // Handle ReadableStream in the response body
//             let jsonData;
//             if (response.body instanceof ReadableStream) {
//                 const reader = response.body.getReader();
//                 let result = '';
//                 while (true) {
//                     const { done, value } = await reader.read();
//                     if (done) break;
//                     result += new TextDecoder().decode(value);
//                 }
//                 try {
//                     jsonData = JSON.parse(result);
//                 } catch (e) {
//                     console.error('Failed to parse response:', e);
//                     throw new Error('Invalid response format');
//                 }
//             } else {
//                 jsonData = response.body;
//             }

//             if (!jsonData || !jsonData.scene) {
//                 throw new Error('Invalid response structure');
//             }

//             return jsonData;
//         } catch (error) {
//             console.error('API Error Details:', {
//                 message: error.message,
//                 name: error.name,
//                 code: error.code || error.statusCode,
//                 stack: error.stack
//             });
//             throw error;
//         }
//     }, []);

//     const processApiResponse = useCallback((data) => {
//         if (!data || !data.scene) {
//             throw new Error('Invalid scene data');
//         }

//         return {
//             scene_description: data.scene.scene_description || 'No description available',
//             scene_id: data.scene.scene_id,
//             choices: Array.isArray(data.scene.choices) ? 
//                     data.scene.choices.map(choice => {
//                         return {
//                             text: choice.text || choice,
//                             consequences: choice.consequences || {}
//                         };
//                     }) :
//                     [{ text: 'Continue', consequences: {} }],
//             environment: {
//                 items: Array.isArray(data.scene.environment?.items) ? data.scene.environment.items : [],
//                 npcs: Array.isArray(data.scene.environment?.npcs) ? data.scene.environment.npcs : [],
//                 events: Array.isArray(data.scene.environment?.events) ? data.scene.environment.events : []
//             }
//         };
//     }, []);

//     const generateNewScene = useCallback(async () => {
//         try {
//             setLoading(true);
//             setError(null);

//             const data = await makeApiCall({
//                 current_scene: 'start',
//                 player_choice: null
//             });

//             const validatedGameState = processApiResponse(data);
//             setGameState(validatedGameState);
//         } catch (error) {
//             console.error('Scene Generation Error:', error);
//             setError(error);
//             setGameState(prev => ({
//                 ...prev,
//                 scene_description: error.message || 'An error occurred. Please try again.',
//                 choices: [{ text: 'Retry', consequences: {} }]
//             }));
//         } finally {
//             setLoading(false);
//         }
//     }, [makeApiCall, processApiResponse]);

//     const makeChoice = useCallback(async (choice, currentGameState) => {
//         try {
//             setLoading(true);
//             setError(null);

//             const data = await makeApiCall({
//                 current_scene: currentGameState.scene_id,
//                 player_choice: choice
//             });

//             const validatedGameState = processApiResponse(data);
            
//             // Check if we're getting a meaningfully different scene
//             if (validatedGameState.scene_description === currentGameState.scene_description) {
//                 setLoading(false);
//                 return; // Don't update state with the same content
//             }

//             setGameState(validatedGameState);
//         } catch (error) {
//             console.error('Choice Processing Error:', error);
//             setError(error);
//             setGameState(prev => ({
//                 ...prev,
//                 choices: [{ text: 'Retry', consequences: {} }]
//             }));
//         } finally {
//             setLoading(false);
//         }
//     }, [makeApiCall, processApiResponse]);

//     useEffect(() => {
//         generateNewScene();
//     }, [generateNewScene]);

//     const handleChoice = useCallback((choice) => {
//         makeChoice(choice, gameState);
//     }, [makeChoice, gameState]);

//     if (loading) {
//         return <div className="loading">Loading your adventure...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <h2>An Error Occurred</h2>
//                 <p>{error.message || 'Unable to load the game. Please try again later.'}</p>
//                 <button onClick={generateNewScene} className="retry-button">
//                     Retry
//                 </button>
//             </div>
//         );
//     }

//     return (
//         <div className="game-screen">
//             <div className="scene-container">
//                 <div className="scene-description">
//                     <p>{gameState.scene_description}</p>
//                 </div>
//                 <div className="choices">
//                     {gameState.choices.map((choice, index) => (
//                         <button
//                             key={index}
//                             onClick={() => handleChoice(choice.text)}
//                             className="choice-button"
//                             disabled={loading}
//                         >
//                             {choice.text}
//                         </button>
//                     ))}
//                 </div>
//             </div>
//             {gameState.environment.items?.length > 0 && (
//                 <div className="environment-items">
//                     <h3>Items in the Environment:</h3>
//                     {gameState.environment.items.map((item, index) => (
//                         <div key={index} className="environment-item">
//                             {typeof item === 'string' ? item : item.name}
//                         </div>
//                     ))}
//                 </div>
//             )}
//             {gameState.environment.npcs?.length > 0 && (
//                 <div className="environment-npcs">
//                     <h3>Characters Present:</h3>
//                     {gameState.environment.npcs.map((npc, index) => (
//                         <div key={index} className="environment-npc">
//                             {typeof npc === 'string' ? npc : npc.name}
//                         </div>
//                     ))}
//                 </div>
//             )}
//             {gameState.environment.events?.length > 0 && (
//                 <div className="environment-events">
//                     <h3>Current Events:</h3>
//                     {gameState.environment.events.map((event, index) => (
//                         <div key={index} className="environment-event">
//                             {typeof event === 'string' ? event : event.description}
//                         </div>
//                     ))}
//                 </div>
//             )}
//         </div>
//     );
// }

// export default GameScreen;

import React, { useState, useEffect, useCallback } from 'react';
import { post } from 'aws-amplify/api';
import { fetchAuthSession } from '@aws-amplify/auth';
import '../styles/GameScreen.css';

function GameScreen() {
    const [gameState, setGameState] = useState({
        scene_description: "Beginning your adventure...",
        scene_id: null,
        choices: [],
        environment: {
            items: [],
            npcs: [],
            events: []
        }
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const makeApiCall = useCallback(async (body) => {
        try {
            console.log('Starting API call with body:', body);
            const session = await fetchAuthSession();
            const idToken = session.tokens?.idToken?.toString();
            
            if (!idToken) {
                throw new Error('Authentication required');
            }

            console.log('Making request to /generate-story');
            const response = await post({
                apiName: 'gameApi',
                path: '/generate-story',
                options: {
                    headers: {
                        Authorization: `Bearer ${idToken}`
                    },
                    body
                }
            }).response;

            console.log('Raw response:', response);

            let jsonData;
            if (response.body instanceof ReadableStream) {
                console.log('Processing ReadableStream response');
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
                console.log('Response is not a ReadableStream:', response.body);
                jsonData = response.body;
            }

            console.log('Processed response data:', jsonData);
            return jsonData;
        } catch (error) {
            console.error('Detailed API Call Error:', {
                message: error.message,
                name: error.name,
                code: error.code || error.statusCode,
                stack: error.stack,
                response: error.response
            });
            throw error;
        }
    }, []);

    const processSceneData = useCallback((data) => {
        console.log('Processing scene data:', data);
        
        // Handle both direct API responses and cached responses
        const sceneData = data.scene || data;
        console.log('Extracted scene data:', sceneData);
        
        const processed = {
            scene_description: sceneData.scene_description,
            scene_id: sceneData.scene_id,
            choices: Array.isArray(sceneData.choices) ? 
                sceneData.choices.map(choice => ({
                    text: typeof choice === 'string' ? choice : choice.text,
                    consequences: choice.consequences || {}
                })) : [],
            environment: {
                items: Array.isArray(sceneData.environment?.items) ? sceneData.environment.items : [],
                npcs: Array.isArray(sceneData.environment?.npcs) ? sceneData.environment.npcs : [],
                events: Array.isArray(sceneData.environment?.events) ? sceneData.environment.events : []
            }
        };

        console.log('Processed scene data:', processed);
        return processed;
    }, []);

    const generateNewScene = useCallback(async () => {
        try {
            console.log('Generating new scene');
            setLoading(true);
            setError(null);

            const data = await makeApiCall({
                current_scene: 'start',
                player_choice: null
            });

            console.log('Received initial scene data:', data);
            const validatedGameState = processSceneData(data);
            console.log('Setting initial game state:', validatedGameState);
            
            setGameState(validatedGameState);
        } catch (error) {
            console.error('Scene Generation Error:', error);
            setError(error);
            setGameState(prev => ({
                ...prev,
                scene_description: error.message || 'An error occurred. Please try again.',
                choices: [{ text: 'Retry', consequences: {} }]
            }));
        } finally {
            setLoading(false);
        }
    }, [makeApiCall, processSceneData]);

    const makeChoice = useCallback(async (choice, currentGameState) => {
        try {
            console.log('makeChoice called with:', { choice, currentGameState });
            setLoading(true);
            setError(null);

            const payload = {
                current_scene: currentGameState.scene_id,
                player_choice: choice
            };
            console.log('Sending choice payload:', payload);

            const data = await makeApiCall(payload);
            console.log('Received choice response:', data);

            // Check if we have a valid response
            if (!data || (!data.scene && !data.scene_description)) {
                console.error('Invalid response structure:', data);
                throw new Error('Invalid response from server');
            }

            // Process the response, which could be from cache
            const validatedGameState = processSceneData(data);
            console.log('Processed game state:', validatedGameState);

            // Only update if we got a valid scene
            if (validatedGameState.scene_description && validatedGameState.scene_id) {
                console.log('Updating game state with:', validatedGameState);
                setGameState(validatedGameState);
            } else {
                console.error('Invalid scene data:', validatedGameState);
                throw new Error('Invalid scene data received');
            }
        } catch (error) {
            console.error('Detailed Choice Processing Error:', {
                error,
                message: error.message,
                name: error.name,
                code: error.code,
                stack: error.stack
            });
            setError(error);
            setGameState(prev => ({
                ...prev,
                choices: [{ text: 'Retry', consequences: {} }]
            }));
        } finally {
            setLoading(false);
        }
    }, [makeApiCall, processSceneData]);

    useEffect(() => {
        generateNewScene();
    }, [generateNewScene]);

    const handleChoice = useCallback((choice) => {
        console.log('handleChoice called with:', choice);
        makeChoice(choice, gameState);
    }, [makeChoice, gameState]);

    if (loading) {
        return <div className="loading">Loading your adventure...</div>;
    }

    if (error) {
        return (
            <div className="error-container">
                <h2>An Error Occurred</h2>
                <p>{error.message || 'Unable to load the game. Please try again later.'}</p>
                <button onClick={generateNewScene} className="retry-button">
                    Retry
                </button>
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
                            onClick={() => handleChoice(choice.text)}
                            className="choice-button"
                            disabled={loading}
                        >
                            {choice.text}
                        </button>
                    ))}
                </div>
            </div>
            {gameState.environment.items?.length > 0 && (
                <div className="environment-items">
                    <h3>Items in the Environment:</h3>
                    {gameState.environment.items.map((item, index) => (
                        <div key={index} className="environment-item">
                            {typeof item === 'string' ? item : item.name}
                        </div>
                    ))}
                </div>
            )}
            {gameState.environment.npcs?.length > 0 && (
                <div className="environment-npcs">
                    <h3>Characters Present:</h3>
                    {gameState.environment.npcs.map((npc, index) => (
                        <div key={index} className="environment-npc">
                            {typeof npc === 'string' ? npc : npc.name}
                        </div>
                    ))}
                </div>
            )}
            {gameState.environment.events?.length > 0 && (
                <div className="environment-events">
                    <h3>Current Events:</h3>
                    {gameState.environment.events.map((event, index) => (
                        <div key={index} className="environment-event">
                            {typeof event === 'string' ? event : event.description}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default GameScreen;