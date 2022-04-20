import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode';
import axios from 'axios';

import ChatInputBox from '../components/chatinputbox';
import Message from '../components/message';

function DebateText({ accessToken }) {
  const DEBATOR = 0;
  const AUDIENCE = 1;
  const REVIEW = 2;

  const navigate = useNavigate();
  const params = useParams();
  const debateId = params.debateId;
  const myUserId = jwt_decode(accessToken).id;
  const [isProTurn, setIsProTurn] = useState(false);
  const [isMePro, setIsMePro] = useState(true);
  const [messageContent, setMessageContent] = useState("");
  const [history, setHistory] = useState([]);
  const [proOnHold, setProOnHold] = useState(true);
  const [conOnHold, setConOnHold] = useState(true);
  const [proUserId, setProUserId] = useState();
  const [conUserId, setConUserId] = useState();
  const [periodicPing, setPeriodicPing] = useState();
  const [topicName, setTopicName] = useState("");
  const [mode, setMode] = useState(AUDIENCE);

  const readHistory = () => {
    axios.get(
      `http://localhost:8000/room/history/${debateId}`
    ).then((res) => {
      setHistory(res.data.history);
      setIsProTurn(res.data.pro_turn);
      setProOnHold(res.data.debate.pro_user_id === null);
      setConOnHold(res.data.debate.con_user_id === null);
    }).catch((err) => {
      console.log(err);
    });
  }

  const send = () => {
    axios.post('http://localhost:8000/room/message', {
      "content": messageContent,
      "debate_id": debateId,
      "pro_turn": isProTurn,
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }).then((res) => {
      setMessageContent("");
      readHistory();
      setIsProTurn(res.data.pro_turn);
    }).catch((err) => {
      console.log(err);
    });
  }

  const exit = () => {
    axios.post('http://localhost:8000/debate/exit', {
      id: debateId,
      as_pro: isMePro,
      as_con: !isMePro,
    }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }).then((res) => {
      navigate('/');
    }).catch((err) => {
      console.log(err);
    });
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
    axios.get(
      `http://localhost:8000/debate/${debateId}`
    ).then((res) => {
      setProUserId(res.data.pro_user_id);
      setConUserId(res.data.con_user_id);

      if (res.data.status === 4) {
        setMode(REVIEW);
        return Promise.resolve(res.data.topic_id);
      }

      if (res.data.pro_user_id === myUserId) {
        setIsMePro(true);
        setMode(DEBATOR);
      } else if (res.data.con_user_id === myUserId) {
        setIsMePro(false);
        setMode(DEBATOR);
      }

      return Promise.resolve(res.data.topic_id);
    }).then((topicId) => {
      axios.get(
        `http://localhost:8000/topic/${topicId}`
      ).then((res) => {
        setTopicName(res.data.name);
      }).catch((err) => {
        console.log(err);
      });
    }).catch((err) => {
      console.log(err);
    });

    readHistory();
    setPeriodicPing(periodicPing ? periodicPing : setInterval(readHistory, 1000));
  }, []);

  console.log(mode);

  return (
    <div className="column is-flex is-flex-direction-column">
      <h1 className="has-text-white is-size-4 is-flex is-align-self-center">
        { topicName }
      </h1>
      <div className="level">
        <div className="level-left">
          <div className="level-item">
            <p className="is-size-2 has-text-white">
              { isMePro ? "Opposition" : "Proposition" }
              {
                (isMePro && conOnHold || !isMePro && proOnHold) ? 
                (mode === REVIEW ? " (Done)" : " (Pending...)") :
                ""
              }
            </p>
          </div>
        </div>
        <div className="level-right">
          <div className="level-item has-text-right">
            <p className="is-size-2 has-text-white">
              { isMePro ? "Proposition" : "Opposition" }
              {
                (isMePro && proOnHold || !isMePro && conOnHold) ?
                (mode === REVIEW ? " (Done)" : " (Pending...)") :
                ""
              }
            </p>
          </div>
        </div>
      </div>
      <div
        className="is-flex-grow-1 is-family-secondary scrollable"
        style={{
          overflow: 'scroll',
        }}
      >
        {
          history.map(mes => {
            return (
              <Message
                content={mes.content}
                isYourTurn={mes.user_id===(isMePro ? proUserId : conUserId)}
              />
            );
          })
        }
      </div>
      {
        mode !== DEBATOR ?
        "" :
        (
          <div
            className="columns is-variable is-1 has-background-info"
            hidden={ mode !== DEBATOR }
          >
            <div className="column is-10">
              <ChatInputBox
                name="Send Your Argument and Rebuttal"
                onChange={fieldOnChange(setMessageContent)}
                value={messageContent}
                disabled={isMePro !== isProTurn}
              />
            </div>
            <div className="column">
              <div className="control">
                <button
                  type="button"
                  className="button is-success has-text-info is-fullwidth"
                  onClick={send}
                  disabled={isMePro !== isProTurn}
                >
                  Send
                </button>
              </div>
            </div>
            <div className="column">
              <div className="control">
                <button
                  type="button"
                  className="button is-primary has-text-white is-fullwidth"
                  onClick={exit}
                >
                  Exit
                </button>
              </div>
            </div>
          </div>
        )
      }
    </div>
  );
}

export default DebateText;
