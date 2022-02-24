import React, { useState } from 'react';
import axios from 'axios';
import jwt_decode from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';

function User() {
  const navigate = useNavigate();
  const token_data = localStorage.getItem('access_token');
  if (token_data === null) {
    navigate('/login');
  }

  const [username, setUsername] = useState(jwt_decode(token_data).username);
  const [password, setPassword] = useState('');
  const [repeat, setRepeat] = useState('');
  const [usernameInfo, setUsernameInfo] = useState('');
  const [repeatInfo, setRepeatInfo] = useState('');

  const fieldOnChange = (setState) => (event) => {
    setState(event.target.value);
  };

  const save = () => {
    if (password !== repeat) {
      setRepeatInfo('Two passwords have to be the same');
      return;
    } else {
      setRepeatInfo('');
    }

    if (!localStorage.getItem('access_token')) {
      navigate('/login');
    }

    const params = {
      new_username: username
    };

    if (password !== '') {
      params.new_password = password;
    }

    axios.put('http://localhost:8000/user', {
      params
    }, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
      },
    }).then((res) => {
      localStorage.setItem('access_token', res.data.token_content);
      setPassword('');
      setRepeat('');
    }).catch((err) => {
      setUsernameInfo(err.response.data.detail);
    });
  };

  return (
    <div className="column is-flex is-flex-direction-column is-align-self-center">
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
            <Button name="Logout" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
