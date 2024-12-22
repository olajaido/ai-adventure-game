// import React, { useState, useEffect } from 'react';
// import { generateClient } from 'aws-amplify/api';
// import '../styles/GameScreen.css';

// const api = generateClient();

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

//     useEffect(() => {
//         loadGameState();
//     }, []);

//     const loadGameState = async () => {
//         try {
//             const response = await api.get('gameApi', '/game-state');
//             setCurrentScene(response.currentScene);
//             setGameHistory(response.playerChoices);
//             setGameStats(response.stats || {
//                 health: 100,
//                 experience: 0,
//                 level: 1
//             });
            
//             if (!response.currentScene) {
//                 generateNewScene();
//             } else {
//                 setLoading(false);
//             }
//         } catch (error) {
//             console.error('Error loading game state:', error);
//             setLoading(false);
//         }
//     };

//     const generateNewScene = async () => {
//         try {
//             const response = await api.post('gameApi', '/generate-story', {
//                 body: {
//                     current_scene: 'start',
//                     player_choice: null,
//                 },
//             });

//             setCurrentScene(response.scene);
//             setChoices(response.choices);
//             setLoading(false);
//         } catch (error) {
//             console.error('Error generating new scene:', error);
//             setLoading(false);
//         }
//     };

//     const makeChoice = async (choice) => {
//         try {
//             setLoading(true);
//             const response = await api.post('gameApi', '/generate-story', {
//                 body: {
//                     current_scene: currentScene,
//                     player_choice: choice,
//                 },
//             });

//             setCurrentScene(response.scene);
//             setChoices(response.choices);
            
//             const newStats = {
//                 ...gameStats,
//                 experience: gameStats.experience + 10,
//                 health: Math.max(0, Math.min(100, gameStats.health + (response.healthChange || 0)))
//             };

//             if (newStats.experience >= newStats.level * 100) {
//                 newStats.level += 1;
//             }

//             setGameStats(newStats);
            
//             await api.post('gameApi', '/save-game', {
//                 body: {
//                     currentScene: response.scene,
//                     playerChoices: [...gameHistory, choice],
//                     stats: newStats
//                 },
//             });

//             setGameHistory([...gameHistory, choice]);
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
import '../styles/GameScreen.css';

const api = generateClient();

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

    const loadGameState = useCallback(async () => {
        try {
            const response = await api.get('gameApi', '/game-state');
            setCurrentScene(response.currentScene);
            setGameHistory(response.playerChoices);
            setGameStats(response.stats || {
                health: 100,
                experience: 0,
                level: 1
            });
            
            if (!response.currentScene) {
                generateNewScene();
            } else {
                setLoading(false);
            }
        } catch (error) {
            console.error('Error loading game state:', error);
            setLoading(false);
        }
    }, []);

    const generateNewScene = useCallback(async () => {
        try {
            const response = await api.post('gameApi', '/generate-story', {
                body: {
                    current_scene: 'start',
                    player_choice: null,
                },
            });

            setCurrentScene(response.scene);
            setChoices(response.choices);
            setLoading(false);
        } catch (error) {
            console.error('Error generating new scene:', error);
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadGameState();
    }, [loadGameState]);

    const makeChoice = async (choice) => {
        try {
            setLoading(true);
            const response = await api.post('gameApi', '/generate-story', {
                body: {
                    current_scene: currentScene,
                    player_choice: choice,
                },
            });

            setCurrentScene(response.scene);
            setChoices(response.choices);
            
            const newStats = {
                ...gameStats,
                experience: gameStats.experience + 10,
                health: Math.max(0, Math.min(100, gameStats.health + (response.healthChange || 0)))
            };

            if (newStats.experience >= newStats.level * 100) {
                newStats.level += 1;
            }

            setGameStats(newStats);
            
            await api.post('gameApi', '/save-game', {
                body: {
                    currentScene: response.scene,
                    playerChoices: [...gameHistory, choice],
                    stats: newStats
                },
            });

            setGameHistory([...gameHistory, choice]);
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