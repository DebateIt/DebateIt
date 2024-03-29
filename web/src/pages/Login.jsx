import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import PropTypes from 'prop-types';

import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';
import config from '../config';

function Login({ accessToken, resetAccessToken }) {
  const navigate = useNavigate();

  useEffect(() => {
    if (accessToken !== null) {
      navigate('/user');
    }
  });

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [usernameInfo, setUsernameInfo] = useState('');

  const fieldOnChange = (setState) => (event) => {
    setState(event.target.value);
  };

  const login = () => {
    axios.post(config.apiURL('/login'), {
      username,
      password,
    }).then((res) => {
      localStorage.setItem('access_token', res.data.token_content);
      resetAccessToken();
      navigate('/');
    }).catch((err) => {
      setUsernameInfo(err.response.data.detail);
    });
  };

  return (
    <div className="column">
      <div className="section">
        <h2 className="block has-text-white is-size-2">
          Login
        </h2>
      </div>
      <div className="is-flex is-flex-direction-column is-align-self-center my-6">
        <div className="container">
          <InputBox
            name="Username"
            onChange={fieldOnChange(setUsername)}
            helpInfo={usernameInfo}
          />
          <PasswordBox
            name="Password"
            onChange={fieldOnChange(setPassword)}
          />
          <div className="field">
            <div className="field-body">
              <Button name="Login" onClick={login} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

Login.propTypes = {
  accessToken: PropTypes.string,
  resetAccessToken: PropTypes.func.isRequired,
};

export default Login;
