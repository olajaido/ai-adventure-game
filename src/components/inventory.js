// import React, { useState, useEffect } from 'react';
// import { generateClient } from 'aws-amplify/api';
// import '../styles/Inventory.css';

// const api = generateClient();

// function Inventory() {
//     const [inventory, setInventory] = useState([]);
//     const [loading, setLoading] = useState(true);

//     useEffect(() => {
//         loadInventory();
//     }, []);

//     const loadInventory = async () => {
//         try {
//             const response = await api.get('gameApi', '/inventory');
//             setInventory(response.data?.items || []);
//             setLoading(false);
//         } catch (error) {
//             console.error('Error loading inventory:', error);
//             setLoading(false);
//         }
//     };

//     if (loading) {
//         return <div className="loading">Loading inventory...</div>;
//     }

//     return (
//         <div className="inventory">
//             <h2>Your Inventory</h2>
//             <div className="inventory-grid">
//                 {inventory.map((item, index) => (
//                     <div key={index} className="inventory-item">
//                         <div className="item-icon">{item.icon}</div>
//                         <div className="item-name">{item.name}</div>
//                         <div className="item-description">{item.description}</div>
//                     </div>
//                 ))}
//                 {inventory.length === 0 && (
//                     <div className="empty-inventory">
//                         Your inventory is empty. Explore the world to find items!
//                     </div>
//                 )}
//             </div>
//         </div>
//     );
// }

// export default Inventory;

// import React, { useState, useEffect, useCallback } from 'react'; 
// import { get } from 'aws-amplify/api'; 
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/Inventory.css';  

// function Inventory() {     
//     const [inventory, setInventory] = useState([]);     
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

//     const loadInventory = useCallback(async () => {         
//         try {             
//             const session = await fetchAuthSession();
            
//             const requestConfig = {
//                 apiName: 'gameApi', 
//                 path: '/inventory',
//                 options: {
//                     headers: {
//                         'Authorization': `Bearer ${session.tokens.idToken?.toString()}`,
//                         'Content-Type': 'application/json'
//                     }
//                 }
//             };

//             console.log('Detailed Request Config:', JSON.stringify(requestConfig, null, 2));

//             try {
//                 const response = await get(requestConfig);

//                 console.log('Detailed API Response:', JSON.stringify(response, null, 2));
                
//                 const data = parseResponse(response);
                
//                 console.log('Parsed Inventory Data:', data);
                
//                 setInventory(data.items || data.inventory || []);             
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
//             console.error('Authentication or Inventory Load Error:', {
//                 message: error.message,
//                 name: error.name,
//                 stack: error.stack
//             });
//             setError(error);
//             setLoading(false);
//         }     
//     }, [parseResponse]);

//     useEffect(() => {         
//         loadInventory();     
//     }, [loadInventory]);      

//     const retryLoadInventory = () => {
//         setError(null);
//         loadInventory();
//     };

//     if (loading) {         
//         return <div className="loading">Loading inventory...</div>;     
//     }      

//     if (error) {
//         return (
//             <div className="error-container">
//                 <h2>An Error Occurred</h2>
//                 <p>Unable to load inventory. Please try again.</p>
//                 <pre>{JSON.stringify(error, null, 2)}</pre>
//                 <button onClick={retryLoadInventory}>Retry</button>
//             </div>
//         );
//     }

//     return (         
//         <div className="inventory">             
//             <h2>Your Inventory</h2>             
//             <div className="inventory-grid">                 
//                 {inventory.map((item, index) => (                     
//                     <div key={index} className="inventory-item">                         
//                         <div className="item-icon">{item.icon || '📦'}</div>                         
//                         <div className="item-name">{item.name || 'Unnamed Item'}</div>                         
//                         <div className="item-description">{item.description || 'No description available'}</div>                     
//                     </div>                 ))}                 
//                 {inventory.length === 0 && (                     
//                     <div className="empty-inventory">                         
//                         Your inventory is empty. Explore the world to find items!                     
//                     </div>                 )}             
//             </div>         
//         </div>     
//     ); 
// }  

// export default Inventory;
// import React, { useState, useEffect, useCallback } from 'react';
// import { get } from 'aws-amplify/api';
// import { fetchAuthSession } from '@aws-amplify/auth';
// import '../styles/Inventory.css';

// function Inventory() {
//     const [inventory, setInventory] = useState([]);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);

//     const loadInventory = useCallback(async () => {
//         try {
//             setLoading(true);
//             setError(null);
            
//             const session = await fetchAuthSession();
//             const idToken = session.tokens?.idToken?.toString();
            
//             if (!idToken) {
//                 throw new Error('No authentication token available');
//             }

//             const requestConfig = {
//                 apiName: 'gameApi',
//                 path: '/inventory',
//                 options: {}
//             };

//             const { body } = await get(requestConfig);
            
//             let data = body;
//             if (typeof body === 'string') {
//                 data = JSON.parse(body);
//             }

//             // Handle different response formats
//             const items = Array.isArray(data.items) ? data.items :
//                          Array.isArray(data.inventory) ? data.inventory :
//                          Array.isArray(data) ? data : [];

//             // Validate and transform items
//             const validatedItems = items.map(item => {
//                 if (typeof item === 'string') {
//                     return {
//                         name: item,
//                         description: 'No description available',
//                         icon: '📦'
//                     };
//                 }
//                 return {
//                     name: item.name || 'Unnamed Item',
//                     description: item.description || 'No description available',
//                     icon: item.icon || '📦',
//                     quantity: item.quantity || 1,
//                     type: item.type || 'misc',
//                     properties: item.properties || {}
//                 };
//             });

//             setInventory(validatedItems);
//         } catch (error) {
//             console.error('Inventory Load Error:', {
//                 message: error.message,
//                 name: error.name,
//                 code: error.code
//             });
//             setError(error);
//         } finally {
//             setLoading(false);
//         }
//     }, []);

//     useEffect(() => {
//         loadInventory();
//     }, [loadInventory]);

//     if (loading) {
//         return <div className="loading">Loading inventory...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <h2>An Error Occurred</h2>
//                 <p>Unable to load inventory. Please try again.</p>
//                 <button onClick={loadInventory} className="retry-button">
//                     Retry
//                 </button>
//             </div>
//         );
//     }

//     return (
//         <div className="inventory">
//             <h2>Your Inventory</h2>
            
//             {inventory.length === 0 ? (
//                 <div className="empty-inventory">
//                     Your inventory is empty. Explore the world to find items!
//                 </div>
//             ) : (
//                 <div className="inventory-grid">
//                     {inventory.map((item, index) => (
//                         <div key={index} className="inventory-item">
//                             <div className="item-header">
//                                 <div className="item-icon">{item.icon}</div>
//                                 <div className="item-name">{item.name}</div>
//                                 {item.quantity > 1 && (
//                                     <div className="item-quantity">x{item.quantity}</div>
//                                 )}
//                             </div>
//                             <div className="item-description">{item.description}</div>
//                             {item.type && (
//                                 <div className="item-type">Type: {item.type}</div>
//                             )}
//                             {Object.keys(item.properties || {}).length > 0 && (
//                                 <div className="item-properties">
//                                     {Object.entries(item.properties).map(([key, value]) => (
//                                         <div key={key} className="item-property">
//                                             {key}: {value}
//                                         </div>
//                                     ))}
//                                 </div>
//                             )}
//                         </div>
//                     ))}
//                 </div>
//             )}
//         </div>
//     );
// }

// export default Inventory;

import React, { useState, useEffect, useCallback } from 'react';
import { API, Auth } from 'aws-amplify';
import '../styles/Inventory.css';

function Inventory() {
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const loadInventory = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            
            const session = await Auth.currentSession();
            const idToken = session.getIdToken().getJwtToken();
            
            if (!idToken) {
                throw new Error('No authentication token available');
            }

            const requestConfig = {
                headers: {
                    Authorization: `Bearer ${idToken}`
                }
            };

            const response = await API.get('gameApi', '/inventory', requestConfig);
            
            let data = response;
            if (typeof response === 'string') {
                data = JSON.parse(response);
            }

            // Handle different response formats
            const items = Array.isArray(data.items) ? data.items :
                         Array.isArray(data.inventory) ? data.inventory :
                         Array.isArray(data) ? data : [];

            // Validate and transform items
            const validatedItems = items.map(item => {
                if (typeof item === 'string') {
                    return {
                        name: item,
                        description: 'No description available',
                        icon: '📦'
                    };
                }
                return {
                    name: item.name || 'Unnamed Item',
                    description: item.description || 'No description available',
                    icon: item.icon || '📦',
                    quantity: item.quantity || 1,
                    type: item.type || 'misc',
                    properties: item.properties || {}
                };
            });

            setInventory(validatedItems);
        } catch (error) {
            console.error('Inventory Load Error:', {
                message: error.message,
                name: error.name,
                code: error.code
            });
            setError(error);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadInventory();
    }, [loadInventory]);

    if (loading) {
        return <div className="loading">Loading inventory...</div>;
    }

    if (error) {
        return (
            <div className="error-container">
                <h2>An Error Occurred</h2>
                <p>Unable to load inventory. Please try again.</p>
                <button onClick={loadInventory} className="retry-button">
                    Retry
                </button>
            </div>
        );
    }

    return (
        <div className="inventory">
            <h2>Your Inventory</h2>
            
            {inventory.length === 0 ? (
                <div className="empty-inventory">
                    Your inventory is empty. Explore the world to find items!
                </div>
            ) : (
                <div className="inventory-grid">
                    {inventory.map((item, index) => (
                        <div key={index} className="inventory-item">
                            <div className="item-header">
                                <div className="item-icon">{item.icon}</div>
                                <div className="item-name">{item.name}</div>
                                {item.quantity > 1 && (
                                    <div className="item-quantity">x{item.quantity}</div>
                                )}
                            </div>
                            <div className="item-description">{item.description}</div>
                            {item.type && (
                                <div className="item-type">Type: {item.type}</div>
                            )}
                            {Object.keys(item.properties || {}).length > 0 && (
                                <div className="item-properties">
                                    {Object.entries(item.properties).map(([key, value]) => (
                                        <div key={key} className="item-property">
                                            {key}: {value}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Inventory;