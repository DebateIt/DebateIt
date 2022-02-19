import React from 'react';
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
  return (
    <div className="App columns m-0">
      <NavBar />
      <BrowserRouter>
        <Routes>
          <Route path="login" element={<Login />} />
          <Route path="register" element={<Registration />} />
          <Route path="user" element={<User />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
