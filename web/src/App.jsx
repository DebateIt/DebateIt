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
import Intro from './pages/Intro';
import TopicCreate from './pages/TopicCreate';
import DebateText from './pages/DebateText';
import Main from './pages/Main';
import Topic from './pages/Topic';
import DebateJoin from './pages/DebateJoin';

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
            path="/"
            element={ accessToken ? (<Main accessToken={accessToken} />) : (<Intro />) }
          />
          <Route
            path="/topic"
            element={(<TopicCreate accessToken={accessToken} />)}
          />
          <Route path="/topic/:topicId" element={(<Topic accessToken={accessToken} />)} />
          <Route path="/debate/:debateId" element={(<DebateText accessToken={accessToken} />)} />
          <Route path="/debate/:debateId/join" element={(<DebateJoin accessToken={accessToken} />)} />
          <Route 
            path="/login"
            element={(
              <Login
                accessToken={accessToken}
                resetAccessToken={resetAccessToken}
              />
            )}
          />
          <Route
            path="/register"
            element={
              <Registration />
            }
          />
          <Route
            path="/user"
            element={(
              <User
                accessToken={accessToken}
                resetAccessToken={resetAccessToken}
              />
            )}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
