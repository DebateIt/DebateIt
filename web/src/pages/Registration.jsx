import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';

function User() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [repeat, setRepeat] = useState('');
  const [helpInfo, setHelpInfo] = useState('');
  const navigate = useNavigate();

  const fieldOnChange = (setState) => (event) => {
    setState(event.target.value);
  };

  const register = () => {
    setHelpInfo(password !== repeat ? 'Two passwords have to be the same!' : '');
    if (!helpInfo) {
      return;
    }

    axios.post('http://localhost:8000/user', {
      username,
      password,
    }).then(() => {
      navigate('/login');
    }).catch((err) => {
      console.log(err.response.data.detail);
    });
  };

  return (
    <div className="column is-flex is-flex-direction-column is-align-self-center">
      <div className="container">
        <InputBox
          name="Username"
          onChange={fieldOnChange(setUsername)}
        />
        <PasswordBox
          name="Password"
          onChange={fieldOnChange(setPassword)}
        />
        <PasswordBox
          name="__Repeat"
          onChange={fieldOnChange(setRepeat)}
          helpInfo={helpInfo}
        />
        <div className="field">
          <div className="field-body">
            <Button name="Register" onClick={register} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
