import React from 'react';

function User() {
  return (
    <div className="column is-flex is-flex-direction-column is-align-self-center">
      <div className="container">
        <div className="field is-horizontal">
          <div className="field-label is-normal">
            <label htmlFor="Username" className="label has-text-white is-size-5">
              Username:
              {/* <input type="text" /> */}
            </label>
          </div>
          <div className="field-body">
            <div className="field">
              <p className="control is-expanded">
                <input
                  className="input is-family-secondary"
                  type="text"
                  placeholder="Username"
                  id="Username"
                />
              </p>
            </div>
          </div>
        </div>
        <div className="field is-horizontal">
          <div className="field-label is-normal">
            <label htmlFor="Password" className="label has-text-white is-size-5">
              Password:
              {/* <input type="text" /> */}
            </label>
          </div>
          <div className="field-body">
            <div className="field">
              <p className="control is-expanded">
                <input
                  className="input is-family-secondary"
                  type="password"
                  placeholder="Password"
                  id="Password"
                />
              </p>
            </div>
          </div>
        </div>
        <div className="field is-horizontal">
          <div className="field-label is-normal">
            <label htmlFor="New-Password" className="label has-text-white is-size-5">
              New Password:
              {/* <input type="text" /> */}
            </label>
          </div>
          <div className="field-body">
            <div className="field">
              <p className="control is-expanded">
                <input
                  className="input is-family-secondary"
                  type="password"
                  placeholder="New Password"
                  id="New-Password"
                />
              </p>
            </div>
          </div>
        </div>
        <div className="field is-horizontal">
          <div className="field-body">
            <div className="field">
              <button type="button" className="button is-medium is-success has-text-info is-fullwidth">
                Save
              </button>
            </div>
            <div className="field">
              <button type="button" className="button is-medium is-primary is-fullwidth">
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
