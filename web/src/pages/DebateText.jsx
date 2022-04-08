import React, { useEffect, useState } from 'react';
import axios from 'axios';

import ChatInputBox from '../components/chatinputbox';
import Message from '../components/message';

function DebateText() {
  const myUserId = 28;
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get(
      'http://localhost:8000/history'
    ).then((res) => {
      setHistory(res.data);
    }).catch((err) => {
      console.log(err);
    })
  }, []);

  const messages = history.map(mes => {
    return (
      <Message content={mes.content} isYourTurn={mes.user_id===myUserId} />
    );
  });

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
        {messages}
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
