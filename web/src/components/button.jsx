import React from 'react';
import PropTypes from 'prop-types';

function Button({ name }) {
  return (
    <div className="field">
      <button type="button" className="button is-medium is-success has-text-info is-fullwidth">
        { name }
      </button>
    </div>
  );
}

Button.propTypes = {
  name: PropTypes.string.isRequired,
};

export default Button;
