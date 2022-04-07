import React from 'react';

import ChatInputBox from '../components/chatinputbox';
import Message from '../components/message';

function DebateText() {
  return (
    <div className="column is-flex is-flex-direction-column">
      <div className="level">
        <div className="level-left">
          <div className="level-item">
            <p className="is-size-2 has-text-white">For</p>
          </div>
        </div>
        <div className="level-right">
          <div className="level-item has-text-right">
            <p className="is-size-2 has-text-white">Against</p>
          </div>
        </div>
      </div>
      <div
        className="is-flex-grow-1 is-family-secondary scrollable"
        style={{
          overflow: 'scroll',
        }}
      >
        <Message 
          content="Traditionally speaking, science expo is a thing dads will do"
          isYourTurn={true}
        />
        <Message
          content="Scientifically speaking, tradition is a thing idiots will do"
          isYourTurn={false}
        />
      </div>
      <div className="columns is-variable is-1 has-background-info">
        <div className="column is-11">
          <ChatInputBox
            name="Send Your Argument and Rebuttal"
          />
        </div>
        <div className="column">
          <div className="control">
            <button
              type="button"
              className="button is-success has-text-info is-fullwidth"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DebateText;
