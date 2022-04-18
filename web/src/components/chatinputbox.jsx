import React from 'react';
import PropTypes from 'prop-types';

function ChatInputBox({
  name, onChange, value, disabled
}) {
  return (
    <div className="field is-horizontal">
      <div className="field-body">
        <div className="field">
          <p className="control is-expanded">
            <input
              className="input is-family-secondary has-background-primary"
              type="text"
              placeholder={name}
              id={name}
              onChange={onChange}
              value={value}
              disabled={disabled}
            />
          </p>
        </div>
      </div>
    </div>
  );
}

ChatInputBox.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  value: PropTypes.string,
  disabled: PropTypes.bool
};

export default ChatInputBox;
