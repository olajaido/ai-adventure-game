// import React, { useState, useEffect, useCallback } from 'react';
// import { get, post } from 'aws-amplify/api';
// import { fetchAuthSession } from 'aws-amplify/auth';
// import '../styles/GameScreen.css';

// function GameScreen() {
//    const [currentScene, setCurrentScene] = useState(null);
//    const [choices, setChoices] = useState([]);
//    const [gameHistory, setGameHistory] = useState([]);
//    const [loading, setLoading] = useState(true);
//    const [gameStats, setGameStats] = useState({
//        health: 100,
//        experience: 0,
//        level: 1
//    });

//    const makeApiCall = useCallback(async (method, path, body = null) => {
//        try {
//            const { tokens } = await fetchAuthSession();
           
//            const requestConfig = {
//                apiName: 'gameApi',
//                path: path.startsWith('/') ? path.slice(1) : path,
//                options: {
//                    headers: {
//                        'Authorization': `Bearer ${tokens.idToken.toString()}`,
//                        'Content-Type': 'application/json'
//                    }
//                }
//            };

//            if (body) {
//                requestConfig.options.body = JSON.stringify(body);
//            }

//            console.log('Request Config:', requestConfig);

//            const response = await (method === 'GET' ? get(requestConfig) : post(requestConfig));
//            console.log('Raw Response:', response);
           
//            return response;
//        } catch (error) {
//            console.error('API Call Error:', {
//                message: error.message,
//                status: error.status,
//                name: error.name,
//                details: error
//            });
//            throw error;
//        }
//    }, []);

//    const generateNewScene = useCallback(async () => {
//        try {
//            const response = await makeApiCall('POST', 'generate-story', {
//                current_scene: 'start',
//                player_choice: null,
//            });

//            console.log('Generate Scene Response:', response);
//            if (response?.body) {
//                const data = JSON.parse(response.body);
//                setCurrentScene(data.scene);
//                setChoices(data.choices || []);
//            }
//            setLoading(false);
//        } catch (error) {
//            console.error('Error generating new scene:', error);
//            setLoading(false);
//        }
//    }, [makeApiCall]);

//    const loadGameState = useCallback(async () => {
//        try {
//            const response = await makeApiCall('GET', 'game-state');
//            console.log('Load Game State Response:', response);
           
//            if (response?.body) {
//                const data = JSON.parse(response.body);
//                setCurrentScene(data.currentScene);
//                setGameHistory(data.playerChoices || []);
//                setGameStats(data.stats || {
//                    health: 100,
//                    experience: 0,
//                    level: 1
//                });
               
//                if (!data.currentScene) {
//                    generateNewScene();
//                } else {
//                    setLoading(false);
//                }
//            } else {
//                generateNewScene();
//            }
//        } catch (error) {
//            console.error('Error loading game state:', error);
//            setLoading(false);
//        }
//    }, [makeApiCall, generateNewScene]);

//    useEffect(() => {
//        loadGameState();
//    }, [loadGameState]);

//    const makeChoice = async (choice) => {
//        try {
//            setLoading(true);
           
//            const response = await makeApiCall('POST', 'generate-story', {
//                current_scene: currentScene,
//                player_choice: choice,
//            });

//            console.log('Make Choice Response:', response);
//            if (response?.body) {
//                const data = JSON.parse(response.body);
//                setCurrentScene(data.scene);
//                setChoices(data.choices || []);
               
//                const newStats = {
//                    ...gameStats,
//                    experience: gameStats.experience + 10,
//                    health: Math.max(0, Math.min(100, gameStats.health + (data.healthChange || 0)))
//                };

//                if (newStats.experience >= newStats.level * 100) {
//                    newStats.level += 1;
//                }

//                setGameStats(newStats);
               
//                await makeApiCall('POST', 'save-game', {
//                    currentScene: data.scene,
//                    playerChoices: [...gameHistory, choice],
//                    stats: newStats
//                });

//                setGameHistory([...gameHistory, choice]);
//            }
//            setLoading(false);
//        } catch (error) {
//            console.error('Error processing choice:', error);
//            setLoading(false);
//        }
//    };

//    if (loading) {
//        return <div className="loading">Loading your adventure...</div>;
//    }

//    return (
//        <div className="game-screen">
//            <div className="game-stats">
//                <div className="stat">❤️ Health: {gameStats.health}</div>
//                <div className="stat">⭐ Level: {gameStats.level}</div>
//                <div className="stat">📈 XP: {gameStats.experience}</div>
//            </div>
//            <div className="scene-container">
//                <div className="scene-description">
//                    <p>{currentScene}</p>
//                </div>
//                <div className="choices">
//                    {choices.map((choice, index) => (
//                        <button
//                            key={index}
//                            onClick={() => makeChoice(choice)}
//                            className="choice-button"
//                            disabled={loading}
//                        >
//                            {choice}
//                        </button>
//                    ))}
//                </div>
//            </div>
//            <div className="game-history">
//                <h3>Adventure Log</h3>
//                <div className="history-list">
//                    {gameHistory.map((choice, index) => (
//                        <div key={index} className="history-item">
//                            {choice}
//                        </div>
//                    ))}
//                </div>
//            </div>
//        </div>
//    );
// }

// export default GameScreen;

// import React, { useState, useEffect, useCallback } from 'react';
// //import { defaultConfig } from '@aws-sdk/client-lambda';
// import { SignatureV4 } from '@aws-sdk/signature-v4';
// import { Sha256 } from '@aws-crypto/sha256-browser';
// import { get, post } from '@aws-amplify/api';
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/GameScreen.css';

// function GameScreen() {
//    const [currentScene, setCurrentScene] = useState(null);
//    const [choices, setChoices] = useState([]);
//    const [gameHistory, setGameHistory] = useState([]);
//    const [loading, setLoading] = useState(true);
//    const [gameStats, setGameStats] = useState({
//        health: 100,
//        experience: 0,
//        level: 1
//    });

//    const makeApiCall = useCallback(async (method, path, body = null) => {
//        try {
//            const { credentials } = await fetchAuthSession();
//            const signer = new SignatureV4({
//                credentials,
//                region: process.env.REACT_APP_AWS_REGION,
//                service: 'lambda',
//                sha256: Sha256
//            });

//            const url = new URL(path, process.env.REACT_APP_LAMBDA_ENDPOINT);
//            const signed = await signer.sign({
//                method,
//                headers: {
//                    'Content-Type': 'application/json',
//                    host: url.host
//                },
//                body: body ? JSON.stringify(body) : undefined,
//                uri: url.href
//            });

//            const requestConfig = {
//                apiName: 'gameApi',
//                path,
//                options: {
//                    headers: signed.headers,
//                    body: body ? JSON.stringify(body) : undefined
//                }
//            };

//            console.log('Request Config:', requestConfig);
//            const response = await (method === 'GET' ? get(requestConfig) : post(requestConfig));
//            console.log('Response:', response);
           
//            return response;
//        } catch (error) {
//            console.error('API Call Error:', {
//                message: error.message,
//                status: error.status,
//                name: error.name,
//                details: error
//            });
//            throw error;
//        }
//    }, []);

//    const generateNewScene = useCallback(async () => {
//        try {
//            const response = await makeApiCall('POST', 'generate-story', {
//                current_scene: 'start',
//                player_choice: null,
//            });

//            console.log('Generate Scene Response:', response);
//            if (response?.body) {
//                const data = JSON.parse(response.body);
//                setCurrentScene(data.scene);
//                setChoices(data.choices || []);
//            }
//            setLoading(false);
//        } catch (error) {
//            console.error('Error generating new scene:', error);
//            setLoading(false);
//        }
//    }, [makeApiCall]);

//    const loadGameState = useCallback(async () => {
//        try {
//            const response = await makeApiCall('GET', 'game-state');
//            console.log('Load Game State Response:', response);
           
//            if (response?.body) {
//                const data = JSON.parse(response.body);
//                setCurrentScene(data.currentScene);
//                setGameHistory(data.playerChoices || []);
//                setGameStats(data.stats || {
//                    health: 100,
//                    experience: 0,
//                    level: 1
//                });
               
//                if (!data.currentScene) {
//                    generateNewScene();
//                } else {
//                    setLoading(false);
//                }
//            } else {
//                generateNewScene();
//            }
//        } catch (error) {
//            console.error('Error loading game state:', error);
//            setLoading(false);
//        }
//    }, [makeApiCall, generateNewScene]);

//    useEffect(() => {
//        loadGameState();
//    }, [loadGameState]);

//    const makeChoice = async (choice) => {
//        try {
//            setLoading(true);
           
//            const response = await makeApiCall('POST', 'generate-story', {
//                current_scene: currentScene,
//                player_choice: choice,
//            });

//            console.log('Make Choice Response:', response);
//            if (response?.body) {
//                const data = JSON.parse(response.body);
//                setCurrentScene(data.scene);
//                setChoices(data.choices || []);
               
//                const newStats = {
//                    ...gameStats,
//                    experience: gameStats.experience + 10,
//                    health: Math.max(0, Math.min(100, gameStats.health + (data.healthChange || 0)))
//                };

//                if (newStats.experience >= newStats.level * 100) {
//                    newStats.level += 1;
//                }

//                setGameStats(newStats);
               
//                await makeApiCall('POST', 'save-game', {
//                    currentScene: data.scene,
//                    playerChoices: [...gameHistory, choice],
//                    stats: newStats
//                });

//                setGameHistory([...gameHistory, choice]);
//            }
//            setLoading(false);
//        } catch (error) {
//            console.error('Error processing choice:', error);
//            setLoading(false);
//        }
//    };

//    if (loading) {
//        return <div className="loading">Loading your adventure...</div>;
//    }

//    return (
//        <div className="game-screen">
//            <div className="game-stats">
//                <div className="stat">❤️ Health: {gameStats.health}</div>
//                <div className="stat">⭐ Level: {gameStats.level}</div>
//                <div className="stat">📈 XP: {gameStats.experience}</div>
//            </div>
//            <div className="scene-container">
//                <div className="scene-description">
//                    <p>{currentScene}</p>
//                </div>
//                <div className="choices">
//                    {choices.map((choice, index) => (
//                        <button
//                            key={index}
//                            onClick={() => makeChoice(choice)}
//                            className="choice-button"
//                            disabled={loading}
//                        >
//                            {choice}
//                        </button>
//                    ))}
//                </div>
//            </div>
//            <div className="game-history">
//                <h3>Adventure Log</h3>
//                <div className="history-list">
//                    {gameHistory.map((choice, index) => (
//                        <div key={index} className="history-item">
//                            {choice}
//                        </div>
//                    ))}
//                </div>
//            </div>
//        </div>
//    );
// }

// export default GameScreen;

import React, { useState, useEffect, useCallback } from 'react';
import { SignatureV4 } from '@aws-sdk/signature-v4';
import { Sha256 } from '@aws-crypto/sha256-browser';
import { get, post } from '@aws-amplify/api';
import { fetchAuthSession } from '@aws-amplify/auth';
import '../styles/GameScreen.css';

function GameScreen() {
    const [currentScene, setCurrentScene] = useState(null);
    const [choices, setChoices] = useState([]);
    const [gameHistory, setGameHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [gameStats, setGameStats] = useState({
        health: 100,
        experience: 0,
        level: 1
    });

    const makeApiCall = useCallback(async (method, path, body = null) => {
        try {
            const { credentials } = await fetchAuthSession();
            const signer = new SignatureV4({
                service: 'lambda',
                region: process.env.REACT_APP_AWS_REGION,
                credentials: {
                    accessKeyId: credentials.accessKeyId,
                    secretAccessKey: credentials.secretAccessKey,
                    sessionToken: credentials.sessionToken
                },
                sha256: Sha256
            });

            // Ensure path is properly formatted
            const fullUrl = new URL(
                path.startsWith('/') ? path.slice(1) : path,
                process.env.REACT_APP_LAMBDA_ENDPOINT
            ).toString();

            const request = {
                method,
                hostname: new URL(fullUrl).hostname,
                path: new URL(fullUrl).pathname,
                protocol: 'https:',
                headers: {
                    'Content-Type': 'application/json',
                    host: new URL(fullUrl).host
                }
            };

            if (body) {
                request.body = JSON.stringify(body);
            }

            const signedRequest = await signer.sign(request);

            const requestConfig = {
                apiName: 'gameApi',
                path: path.startsWith('/') ? path.slice(1) : path,
                options: {
                    headers: signedRequest.headers,
                    body: body ? JSON.stringify(body) : undefined
                }
            };

            console.log('Request Config:', requestConfig);
            const response = await (method === 'GET' ? get(requestConfig) : post(requestConfig));
            console.log('Response:', response);
            
            return response;
        } catch (error) {
            console.error('API Call Error:', {
                message: error.message,
                status: error.status,
                name: error.name,
                details: error
            });
            throw error;
        }
    }, []);

    const generateNewScene = useCallback(async () => {
        try {
            const response = await makeApiCall('POST', 'generate-story', {
                current_scene: 'start',
                player_choice: null,
            });

            console.log('Generate Scene Response:', response);
            if (response?.body) {
                const data = JSON.parse(response.body);
                setCurrentScene(data.scene);
                setChoices(data.choices || []);
            }
            setLoading(false);
        } catch (error) {
            console.error('Error generating new scene:', error);
            setLoading(false);
        }
    }, [makeApiCall]);

    const loadGameState = useCallback(async () => {
        try {
            const response = await makeApiCall('GET', 'game-state');
            console.log('Load Game State Response:', response);
            
            if (response?.body) {
                const data = JSON.parse(response.body);
                setCurrentScene(data.currentScene);
                setGameHistory(data.playerChoices || []);
                setGameStats(data.stats || {
                    health: 100,
                    experience: 0,
                    level: 1
                });
                
                if (!data.currentScene) {
                    generateNewScene();
                } else {
                    setLoading(false);
                }
            } else {
                generateNewScene();
            }
        } catch (error) {
            console.error('Error loading game state:', error);
            setLoading(false);
        }
    }, [makeApiCall, generateNewScene]);

    useEffect(() => {
        loadGameState();
    }, [loadGameState]);

    const makeChoice = async (choice) => {
        try {
            setLoading(true);
            
            const response = await makeApiCall('POST', 'generate-story', {
                current_scene: currentScene,
                player_choice: choice,
            });

            console.log('Make Choice Response:', response);
            if (response?.body) {
                const data = JSON.parse(response.body);
                setCurrentScene(data.scene);
                setChoices(data.choices || []);
                
                const newStats = {
                    ...gameStats,
                    experience: gameStats.experience + 10,
                    health: Math.max(0, Math.min(100, gameStats.health + (data.healthChange || 0)))
                };

                if (newStats.experience >= newStats.level * 100) {
                    newStats.level += 1;
                }

                setGameStats(newStats);
                
                await makeApiCall('POST', 'save-game', {
                    currentScene: data.scene,
                    playerChoices: [...gameHistory, choice],
                    stats: newStats
                });

                setGameHistory([...gameHistory, choice]);
            }
            setLoading(false);
        } catch (error) {
            console.error('Error processing choice:', error);
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="loading">Loading your adventure...</div>;
    }

    return (
        <div className="game-screen">
            <div className="game-stats">
                <div className="stat">❤️ Health: {gameStats.health}</div>
                <div className="stat">⭐ Level: {gameStats.level}</div>
                <div className="stat">📈 XP: {gameStats.experience}</div>
            </div>
            <div className="scene-container">
                <div className="scene-description">
                    <p>{currentScene}</p>
                </div>
                <div className="choices">
                    {choices.map((choice, index) => (
                        <button
                            key={index}
                            onClick={() => makeChoice(choice)}
                            className="choice-button"
                            disabled={loading}
                        >
                            {choice}
                        </button>
                    ))}
                </div>
            </div>
            <div className="game-history">
                <h3>Adventure Log</h3>
                <div className="history-list">
                    {gameHistory.map((choice, index) => (
                        <div key={index} className="history-item">
                            {choice}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default GameScreen;