import React from 'react';
import PropTypes from 'prop-types';

function ChatInputBox({
  name, onChange, value,
}) {
  return (
    <div className="field is-horizontal">
      <div className="field-body">
        <div className="field">
          <p className="control is-expanded">
            <input
              className="input is-family-secondary"
              type="text"
              placeholder={name}
              id={name}
              onChange={onChange}
              value={value}
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
  helpInfo: PropTypes.string,
  value: PropTypes.string,
};

export default ChatInputBox;
