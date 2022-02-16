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
        <PasswordBox name="New Pasword" />
        <div className="field is-horizontal">
          <div className="field-body">
            <Button name="Save" />
            <Button name="Logout" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
