import React from 'react';

function NavBar() {
  return (
    <div
      className="column p-0 is-1 is-flex is-flex-direction-column is-align-items-center has-background-primary has-text-light"
    >
      <div className="is-size-3 mt-5">
        Debate It
      </div>
      <div className="is-size-5 my-6">
        ALPACAMAX
      </div>
      <a href="/login" className="py-4 button is-primary is-fullwidth is-family-secondary">
        Login
      </a>
      <a href="/register" className="py-4 button is-primary is-fullwidth is-family-secondary">
        Register
      </a>
      <a href="/user" className="py-4 button is-primary is-fullwidth is-family-secondary">
        User
      </a>
    </div>
  );
}

export default NavBar;
