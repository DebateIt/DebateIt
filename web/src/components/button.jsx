import React from 'react';
import PropTypes from 'prop-types';

function Button({ name, onClick }) {
  return (
    <div className="field">
      <button
        type="button"
        className="button is-medium is-success has-text-info is-fullwidth"
        onClick={onClick}
      >
        { name }
      </button>
    </div>
  );
}

Button.propTypes = {
  name: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

export default Button;
