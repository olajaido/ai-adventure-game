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
import React, { useState, useEffect, useCallback } from 'react';
import { get } from 'aws-amplify/api';
import { fetchAuthSession } from '@aws-amplify/auth';
import '../styles/Inventory.css';

function Inventory() {
    const [inventory, setInventory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const loadInventory = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            
            const session = await fetchAuthSession();
            const idToken = session.tokens?.idToken?.toString();
            
            if (!idToken) {
                throw new Error('Authentication required');
            }

            const response = await get({
                apiName: 'gameApi',
                path: '/inventory',
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

            console.log('Inventory Response:', jsonData);

            // Process inventory data
            const inventoryItems = Array.isArray(jsonData?.inventory) ? 
                jsonData.inventory : [];

            // Transform and validate each item
            const validatedItems = inventoryItems.map(item => ({
                id: item.id || Math.random().toString(36).substr(2, 9),
                name: item.name || 'Unknown Item',
                description: item.description || 'No description available',
                quantity: item.quantity || 1,
                icon: item.icon || '📦',
                type: item.type || 'misc'
            }));

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
                <p>{error.message || 'Unable to load inventory. Please try again.'}</p>
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
                    {inventory.map((item) => (
                        <div key={item.id} className="inventory-item">
                            <div className="item-header">
                                <span className="item-icon">{item.icon}</span>
                                <span className="item-name">{item.name}</span>
                                {item.quantity > 1 && (
                                    <span className="item-quantity">x{item.quantity}</span>
                                )}
                            </div>
                            <p className="item-description">{item.description}</p>
                            <div className="item-type">{item.type}</div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default Inventory;