import React from 'react';
import PropTypes from 'prop-types';

function PasswordBox({
  name, onChange, helpInfo, value,
}) {
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
              type="password"
              placeholder={name}
              id={name}
              onChange={onChange}
              value={value}
            />
          </p>
          <p className="help is-white">{ helpInfo }</p>
        </div>
      </div>
    </div>
  );
}

PasswordBox.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  helpInfo: PropTypes.string,
  value: PropTypes.string,
};

export default PasswordBox;
