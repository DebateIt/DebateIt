import React, { useEffect, useState } from 'react';
import jwt_decode from 'jwt-decode';
import PropTypes from 'prop-types';

function NavBar({ accessToken }) {

  return (
    <div
      className="column p-0 is-1 is-flex is-flex-direction-column is-align-items-center has-background-primary has-text-light"
    >
      <div className="is-size-3 mt-5">
        Debate It
      </div>
      <div className="is-size-5 my-6">
        <a href="/user" className="has-text-white">
          { accessToken !== null ? jwt_decode(accessToken).username : 'Anonymous' }
        </a>
      </div>
      <a href="/login" className="py-4 button is-primary is-fullwidth is-family-secondary">
        Login
      </a>
      <a href="/register" className="py-4 button is-primary is-fullwidth is-family-secondary">
        Register
      </a>
    </div>
  );
}

NavBar.propTypes = {
  accessToken: PropTypes.string,
};

export default NavBar;
