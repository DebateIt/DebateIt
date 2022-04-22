import React, { useEffect, useState } from 'react';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';
import config from '../config';

function User({ accessToken, resetAccessToken }) {
  const navigate = useNavigate();

  useEffect(() => {
    if (accessToken === null) {
      navigate('/login');
    }
  });

  const [username, setUsername] = useState(
    accessToken !== null ? jwt_decode(accessToken).username : '',
  );
  const [password, setPassword] = useState('');
  const [repeat, setRepeat] = useState('');
  const [usernameInfo, setUsernameInfo] = useState('');
  const [repeatInfo, setRepeatInfo] = useState('');

  const fieldOnChange = (setState) => (event) => {
    setState(event.target.value);
  };

  const save = () => {
    setUsernameInfo('');
    setRepeatInfo('');

    if (password !== repeat) {
      setRepeatInfo('Two passwords have to be the same');
      return;
    }

    const params = {};

    if (jwt_decode(accessToken).username !== username) {
      params.new_username = username;
    }

    if (password !== '') {
      params.new_password = password;
    }

    axios.put(config.apiURL('/user'), params, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }).then((res) => {
      localStorage.setItem('access_token', res.data.token_content);
      resetAccessToken();
      setPassword('');
      setRepeat('');
    }).catch((err) => {
      if (err.response.status === 401) { // If the access_token expires
        localStorage.removeItem('access_token');
        resetAccessToken();
        navigate('/login');
      }
      setUsernameInfo(err.response.data.detail);
    });
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    resetAccessToken();
  };

  return (
    <div className="column">
      <div className="section">
        <h2 className="block has-text-white is-size-2">
          Profile
        </h2>
      </div>
      <div className="is-flex is-flex-direction-column is-align-self-center my-6">
        <div className="container">
          <InputBox
            name="Username"
            onChange={fieldOnChange(setUsername)}
            helpInfo={usernameInfo}
            value={username}
          />
          <PasswordBox
            name="Password"
            onChange={fieldOnChange(setPassword)}
            value={password}
          />
          <PasswordBox
            name="__Repeat"
            onChange={fieldOnChange(setRepeat)}
            helpInfo={repeatInfo}
            value={repeat}
          />
          <div className="field is-horizontal">
            <div className="field-body">
              <Button name="Save" onClick={save} />
              <Button name="Logout" onClick={logout} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

User.propTypes = {
  accessToken: PropTypes.string,
  resetAccessToken: PropTypes.func.isRequired,
};

export default User;
