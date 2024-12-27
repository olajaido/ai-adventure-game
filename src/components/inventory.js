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

import React, { useState, useEffect, useCallback } from 'react'; 
import { get } from 'aws-amplify/api'; 
import { fetchAuthSession } from '@aws-amplify/auth';
import '../styles/Inventory.css';  

function Inventory() {     
    const [inventory, setInventory] = useState([]);     
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

    const loadInventory = useCallback(async () => {         
        try {             
            const session = await fetchAuthSession();
            
            const requestConfig = {
                apiName: 'gameApi', 
                path: '/inventory',
                options: {
                    headers: {
                        'Authorization': `Bearer ${session.tokens.idToken?.toString()}`,
                        'Content-Type': 'application/json'
                    }
                }
            };

            const response = await get(requestConfig);
            
            const data = parseResponse(response);
            
            setInventory(data.items || data.inventory || []);             
            setLoading(false);         
        } catch (error) {             
            console.error('Error loading inventory:', error);             
            setLoading(false);         
        }     
    }, []);

    useEffect(() => {         
        loadInventory();     
    }, [loadInventory]);      

    if (loading) {         
        return <div className="loading">Loading inventory...</div>;     
    }      

    return (         
        <div className="inventory">             
            <h2>Your Inventory</h2>             
            <div className="inventory-grid">                 
                {inventory.map((item, index) => (                     
                    <div key={index} className="inventory-item">                         
                        <div className="item-icon">{item.icon || '📦'}</div>                         
                        <div className="item-name">{item.name || 'Unnamed Item'}</div>                         
                        <div className="item-description">{item.description || 'No description available'}</div>                     
                    </div>                 ))}                 
                {inventory.length === 0 && (                     
                    <div className="empty-inventory">                         
                        Your inventory is empty. Explore the world to find items!                     
                    </div>                 )}             
            </div>         
        </div>     
    ); 
}  

export default Inventory;