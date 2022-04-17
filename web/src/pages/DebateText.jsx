import React, { useEffect, useState } from 'react';
import axios from 'axios';

import ChatInputBox from '../components/chatinputbox';
import Message from '../components/message';

function DebateText() {
  const myUserId = 28;
  const [messageContent, setMessageContent] = useState("");
  const [history, setHistory] = useState([]);

  
  const messages = history.map(mes => {
    return (
      <Message content={mes.content} isYourTurn={mes.user_id===myUserId} />
    );
  });

  const readHistory = () => {
    axios.get(
      'http://localhost:8000/history'
    ).then((res) => {
      setHistory(res.data);
    }).catch((err) => {
      console.log(err);
    });
  }
  
  const send = () => {
    axios.post('http://localhost:8000/message', {
      "content": messageContent,
      "user_id": myUserId,
    }).then((res) => {
      setMessageContent("");
      readHistory();
    }).catch((err) => {
      console.log(err);
    })
  }
  
  const fieldOnChange = (setState) => (event) => {
    setState(event.target.value);
  };

  // This is a really bad practice here but I'll do it for simplicity's sake
  // In the future we need to set an endpoint in the backend just to check
  // if the other user has already sent a message or not. Or we can setup
  // a websocket server to let the backend update the history data on the
  // frontend
  useEffect(() => {
    setTimeout(readHistory, 1000);
  });

  return (
    <div className="column is-flex is-flex-direction-column">
      <div className="level">
        <div className="level-left">
          <div className="level-item">
            <p className="is-size-2 has-text-white">Opposition</p>
          </div>
        </div>
        <div className="level-right">
          <div className="level-item has-text-right">
            <p className="is-size-2 has-text-white">Proposition</p>
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
            onChange={fieldOnChange(setMessageContent)}
            value={messageContent}
          />
        </div>
        <div className="column">
          <div className="control">
            <button
              type="button"
              className="button is-success has-text-info is-fullwidth"
              onClick={send}
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
