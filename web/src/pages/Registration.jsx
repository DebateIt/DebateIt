import React from 'react';
import InputBox from '../components/inputbox';
import PasswordBox from '../components/passwordbox';
import Button from '../components/button';

function User() {
  return (
    <div className="column is-flex is-flex-direction-column is-align-self-center">
      <div className="container">
        <InputBox name="Username" />
        <PasswordBox name="Password" />
        <PasswordBox name="__Repeat" />
        <div className="field">
          <div className="field-body">
            <Button name="Register" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
