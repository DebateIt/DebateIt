import React, { useState } from 'react';
import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';

function User() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [repeat, setRepeat] = useState('');
  const [helpInfo, setHelpInfo] = useState('');

  const fieldOnChange = (setState) => (event) => {
    setState(event.target.value);
  };

  const register = () => {
    if (password !== repeat) {
      setHelpInfo('Two password have to be the same!');
    }
    console.log(username, password, repeat);
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
