import React, { useState } from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';

import NavBar from './components/navbar';
import Registration from './pages/Registration';
import Login from './pages/Login';
import User from './pages/User';

function App() {
  const [accessToken, setAccessToken] = useState(localStorage.getItem('access_token'));
  const resetAccessToken = () => {
    setAccessToken(localStorage.getItem('access_token'));
  };
  
  return (
    <div className="App columns m-0">
      <NavBar accessToken={accessToken} />
      <BrowserRouter>
        <Routes>
          <Route
            path="login"
            element={
              <Login
                accessToken={accessToken}
                resetAccessToken={resetAccessToken}
              />
            }
          />
          <Route
            path="register"
            element={
              <Registration />
            }
          />
          <Route
            path="user"
            element={
              <User
                accessToken={accessToken}
                resetAccessToken={resetAccessToken}
              />
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
