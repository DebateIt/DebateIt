import React from 'react';

function User() {
  return (
    <div className="column is-flex is-flex-direction-column is-align-self-center">
      <div className="container">
        <div className="field is-horizontal">
          <div className="field-label is-normal">
            <label className="label has-text-white is-size-5">Username:</label>
          </div>
          <div className="field-body">
            <div className="field">
              <p className="control is-expanded">
                <input
                  className="input is-family-secondary"
                  type="text"
                  placeholder="Username"
                />
              </p>
            </div>
          </div>
        </div>
        <div className="field is-horizontal">
          <div className="field-label is-normal">
            <label className="label has-text-white is-size-5">Password:</label>
          </div>
          <div className="field-body">
            <div className="field">
              <p className="control is-expanded">
                <input
                  className="input is-family-secondary"
                  type="password"
                  placeholder="Password"
                />
              </p>
            </div>
          </div>
        </div>
        <div className="field">
          <div className="field-body">
            <div className="field">
              <button className="button is-medium is-success has-text-info is-fullwidth">
                Login
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
