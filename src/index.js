// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import './styles/index.css';
// import App from './App';

// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );

// src/index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import { Amplify } from 'aws-amplify';
import { cognitoUserPoolsTokenProvider } from 'aws-amplify/auth/cognito';
import awsExports from './aws-exports';
import './styles/index.css';
import App from './App';

// Configure Amplify
Amplify.configure(awsExports);
cognitoUserPoolsTokenProvider.setKeyValueStorage(window.localStorage);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);