import React from 'react';
import PropTypes from 'prop-types';

function InputBox({ name }) {
  return (
    <div className="field is-horizontal">
      <div className="field-label is-normal">
        <label htmlFor={name} className="label has-text-white is-size-5">
          { name }
          :
          {/* <input type="text" /> */}
        </label>
      </div>
      <div className="field-body">
        <div className="field">
          <p className="control is-expanded">
            <input
              className="input is-family-secondary"
              type="text"
              placeholder={name}
              id={name}
            />
          </p>
        </div>
      </div>
    </div>
  );
}

InputBox.propTypes = {
  name: PropTypes.string.isRequired,
};

export default InputBox;
