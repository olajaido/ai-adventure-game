// import React from 'react';
// import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
// import { Amplify } from 'aws-amplify';
// import { withAuthenticator } from '@aws-amplify/ui-react';
// import '@aws-amplify/ui-react/styles.css';
// import awsExports from './aws-exports';  // Import AWS exports
// import GameScreen from './components/GameScreen';  
// import Inventory from './components/inventory';    
// import Profile from './components/profile';        
// import './styles/App.css';                        
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import awsExports from './aws-exports';
import GameScreen from './components/GameScreen';  
import Inventory from './components/inventory';    
import Profile from './components/profile';        
import './styles/App.css'; 

// Configure Amplify with imported config
Amplify.configure(awsExports);

function App() {
  return (
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
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </div>
    </Router>
  );
}

export default withAuthenticator(App);