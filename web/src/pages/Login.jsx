import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';

function Login() {
  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
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
    axios.post('http://localhost:8000/login', {
      username,
      password,
    }).then((res) => {
      localStorage.setItem('access_token', res.data.token_content);
      navigate('/user');
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
  );
}

export default Login;
