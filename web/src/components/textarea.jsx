import React from 'react';
import PropTypes from 'prop-types';

function Textarea({
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
            <textarea
              className="textarea is-family-secondary"
              placeholder={name}
              id={name}
              onChange={onChange}
              value={value}
            >

            </textarea>
          </p>
          <p className="help is-white">{ helpInfo }</p>
        </div>
      </div>
    </div>
  );
}

Textarea.propTypes = {
    name: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    helpInfo: PropTypes.string,
    value: PropTypes.string,
};

export default Textarea;
  