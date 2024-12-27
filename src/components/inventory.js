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

import React, { useState, useEffect } from 'react'; 
import { generateClient } from 'aws-amplify/api'; 
import '../styles/Inventory.css';  

function Inventory() {     
    const client = generateClient();
    const [inventory, setInventory] = useState([]);     
    const [loading, setLoading] = useState(true);      

    useEffect(() => {         
        loadInventory();     
    }, []);      

    const loadInventory = async () => {         
        try {             
            const response = await client.get({
                apiName: 'gameApi', 
                path: '/inventory'
            });
            
            setInventory(response.data?.items || []);             
            setLoading(false);         
        } catch (error) {             
            console.error('Error loading inventory:', error);             
            setLoading(false);         
        }     
    };      

    if (loading) {         
        return <div className="loading">Loading inventory...</div>;     
    }      

    return (         
        <div className="inventory">             
            <h2>Your Inventory</h2>             
            <div className="inventory-grid">                 
                {inventory.map((item, index) => (                     
                    <div key={index} className="inventory-item">                         
                        <div className="item-icon">{item.icon}</div>                         
                        <div className="item-name">{item.name}</div>                         
                        <div className="item-description">{item.description}</div>                     
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