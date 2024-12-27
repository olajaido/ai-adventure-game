// import React from 'react';
// import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
// import { Amplify } from 'aws-amplify';
// import { withAuthenticator } from '@aws-amplify/ui-react';
// import '@aws-amplify/ui-react/styles.css';
// import awsExports from './aws-exports';
// import GameScreen from './components/GameScreen';
// import Inventory from './components/Inventory';
// import Profile from './components/Profile';
// import './styles/App.css';

// Amplify.configure(awsExports);

// function App() {
//     return (
//         <Router>
//             <div className="app">
//                 <nav className="nav-bar">
//                     <h1>AI Adventure Game</h1>
//                     <div className="nav-links">
//                         <Link to="/" className="nav-link">Game</Link>
//                         <Link to="/inventory" className="nav-link">Inventory</Link>
//                         <Link to="/profile" className="nav-link">Profile</Link>
//                     </div>
//                 </nav>
//                 <Routes>
//                     <Route path="/" element={<GameScreen />} />
//                     <Route path="/inventory" element={<Inventory />} />
//                     <Route path="/profile" element={<Profile />} />
//                 </Routes>
//             </div>
//         </Router>
//     );
// }

// export default withAuthenticator(App);

// import React from 'react';
// import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
// import { Amplify } from 'aws-amplify';
// import { Authenticator } from '@aws-amplify/ui-react';
// import '@aws-amplify/ui-react/styles.css';
// import awsExports from './aws-exports';
// import GameScreen from './components/GameScreen';
// import Inventory from './components/Inventory';
// import Profile from './components/Profile';
// import './styles/App.css';

// Amplify.configure(awsExports);

// function App() {
//   return (
//     <Authenticator.Provider>
//       <Authenticator>
//         {({ signOut, user }) => (
//           <Router>
//             <div className="app">
//               <nav className="nav-bar">
//                 <h1>AI Adventure Game</h1>
//                 <div className="nav-links">
//                   <Link to="/" className="nav-link">Game</Link>
//                   <Link to="/inventory" className="nav-link">Inventory</Link>
//                   <Link to="/profile" className="nav-link">Profile</Link>
//                 </div>
//               </nav>
//               <Routes>
//                 <Route path="/" element={<GameScreen />} />
//                 <Route path="/inventory" element={<Inventory />} />
//                 <Route path="/profile" element={<Profile signOut={signOut} />} />
//               </Routes>
//             </div>
//           </Router>
//         )}
//       </Authenticator>
//     </Authenticator.Provider>
//   );
// }

// export default App;

import React from 'react'; 
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom'; 
import { Amplify } from 'aws-amplify'; 
import { Authenticator } from '@aws-amplify/ui-react'; 
import '@aws-amplify/ui-react/styles.css'; 
import awsExports from './aws-exports'; 
import GameScreen from './components/GameScreen'; 
import Inventory from './components/Inventory'; 
import Profile from './components/Profile'; 
import './styles/App.css';  

// Configure Amplify with more explicit configuration
Amplify.configure({
    ...awsExports,
    Auth: awsExports.Auth,
    API: {
        REST: awsExports.API.endpoints.reduce((acc, endpoint) => {
            acc[endpoint.name] = {
                endpoint: endpoint.endpoint,
                region: endpoint.region
            };
            return acc;
        }, {})
    }
});

function App() {   
    return (     
        <Authenticator.Provider>       
            <Authenticator>         
                {({ signOut, user }) => (           
                    <Router>             
                        <div className="app">               
                            <nav className="nav-bar">                 
                                <h1>AI Adventure Game</h1>                 
                                <div className="nav-links">                   
                                    <Link to="/" className="nav-link">Game</Link>                   
                                    <Link to="/inventory" className="nav-link">Inventory</Link>                   
                                    <Link to="/profile" className="nav-link">Profile</Link>                 
                                </div>               
                            </nav>               
                            <Routes>                 
                                <Route path="/" element={<GameScreen />} />                 
                                <Route path="/inventory" element={<Inventory />} />                 
                                <Route path="/profile" element={<Profile signOut={signOut} />} />               
                            </Routes>             
                        </div>           
                    </Router>         
                )}       
            </Authenticator>     
        </Authenticator.Provider>   
    ); 
}  

export default App;