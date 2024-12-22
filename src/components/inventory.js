// // // import React, { useState, useEffect } from 'react';
// // // import { API } from 'aws-amplify';
// // // import '../styles/Inventory.css';
// // import React, { useState, useEffect } from 'react'; 
// // import { generateClient } from 'aws-amplify/api';
// // import '../styles/Inventory.css'; 

// // const client = generateClient();


// // function Inventory() {
// //   const [inventory, setInventory] = useState([]);
// //   const [loading, setLoading] = useState(true);

// //   useEffect(() => {
// //     loadInventory();
// //   }, []);

// //   const loadInventory = async () => {
// //     try {
// //       const response = await API.get('gameApi', '/inventory');
// //       setInventory(response.items || []);
// //       setLoading(false);
// //     } catch (error) {
// //       console.error('Error loading inventory:', error);
// //       setLoading(false);
// //     }
// //   };

// //   if (loading) {
// //     return <div className="loading">Loading inventory...</div>;
// //   }

// //   return (
// //     <div className="inventory">
// //       <h2>Your Inventory</h2>
// //       <div className="inventory-grid">
// //         {inventory.map((item, index) => (
// //           <div key={index} className="inventory-item">
// //             <div className="item-icon">{item.icon}</div>
// //             <div className="item-name">{item.name}</div>
// //             <div className="item-description">{item.description}</div>
// //           </div>
// //         ))}
// //         {inventory.length === 0 && (
// //           <div className="empty-inventory">
// //             Your inventory is empty. Explore the world to find items!
// //           </div>
// //         )}
// //       </div>
// //     </div>
// //   );
// // }

// // export default Inventory;
// import React, { useState, useEffect } from 'react'; 
// import { generateClient } from 'aws-amplify/api';
// import '../styles/Inventory.css';  

// // Create the API client
// const client = generateClient();

// function Inventory() {
//  const [inventory, setInventory] = useState([]);
//  const [loading, setLoading] = useState(true);

//  useEffect(() => {
//    loadInventory();
//  }, []);

//  const loadInventory = async () => {
//    try {
//      // Use the client to make API calls
//      const response = await client.get('gameApi', '/inventory');
//      setInventory(response.data?.items || []);
//      setLoading(false);
//    } catch (error) {
//      console.error('Error loading inventory:', error);
//      setLoading(false);
//    }
//  };

//  if (loading) {
//    return <div className="loading">Loading inventory...</div>;
//  }

//  return (
//    <div className="inventory">
//      <h2>Your Inventory</h2>
//      <div className="inventory-grid">
//        {inventory.map((item, index) => (
//          <div key={index} className="inventory-item">
//            <div className="item-icon">{item.icon}</div>
//            <div className="item-name">{item.name}</div>
//            <div className="item-description">{item.description}</div>
//          </div>
//        ))}
//        {inventory.length === 0 && (
//          <div className="empty-inventory">
//            Your inventory is empty. Explore the world to find items!
//          </div>
//        )}
//      </div>
//    </div>
//  );
// }

// export default Inventory;

import React, { useState, useEffect } from 'react';
import { API } from 'aws-amplify';
import '../styles/Inventory.css';

function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadInventory();
  }, []);

  const loadInventory = async () => {
    try {
      const response = await API.get('gameApi', '/inventory');
      setInventory(response.items || []);
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
          </div>
        ))}
        {inventory.length === 0 && (
          <div className="empty-inventory">
            Your inventory is empty. Explore the world to find items!
          </div>
        )}
      </div>
    </div>
  );
}

export default Inventory;