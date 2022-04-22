import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';

function Registration() {
  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
      navigate('/user');
    }
  });

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [repeat, setRepeat] = useState('');
  const [usernameInfo, setUsernameInfo] = useState('');
  const [repeatInfo, setRepeatInfo] = useState('');

  const fieldOnChange = (setState) => (event) => {
    setState(event.target.value);
  };

  const register = () => {
    setUsernameInfo('');
    setRepeatInfo('');

    if (password !== repeat) {
      setRepeatInfo('Two passwords have to be the same');
      return;
    }

    axios.post('http://localhost:8000/user', {
      username,
      password,
    }).then(() => {
      navigate('/login');
    }).catch((err) => {
      setUsernameInfo(err.response.data.detail);
    });
  };

  return (
    <div className="column">
      <div className="section">
        <h2 className="block has-text-white is-size-2">
          Register
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
          <PasswordBox
            name="__Repeat"
            onChange={fieldOnChange(setRepeat)}
            helpInfo={repeatInfo}
          />
          <div className="field">
            <div className="field-body">
              <Button name="Register" onClick={register} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Registration;
