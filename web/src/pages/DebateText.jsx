import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import jwt_decode from 'jwt-decode';
import axios from 'axios';

import ChatInputBox from '../components/chatinputbox';
import Message from '../components/message';
import config from '../config';

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
      config.apiURL(`/room/history/${debateId}`)
    ).then((res) => {
      setHistory(res.data.history);
      setIsProTurn(res.data.pro_turn);
      setProOnHold(res.data.debate.pro_user_id === null);
      setConOnHold(res.data.debate.con_user_id === null);

      setProUserId(res.data.debate.pro_user_id);
      setConUserId(res.data.debate.con_user_id);

      setIsMePro(myUserId !== res.data.debate.con_user_id);

      if (res.data.debate.status === 4) {
        setMode(REVIEW);
      } else if (myUserId === res.data.debate.pro_user_id || myUserId === res.data.debate.con_user_id) {
        setMode(DEBATOR);
      } else {
        setMode(AUDIENCE);
      }
    }).catch((err) => {
      console.log(err);
    });
  }

  const send = () => {
    axios.post(config.apiURL('/room/message'), {
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
    axios.post(config.apiURL('/debate/exit'), {
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

  useEffect(() => {
    axios.get(
      config.apiURL(`/debate/${debateId}`)
    ).then((res) => {
      return Promise.resolve(res.data.topic_id);
    }).then((topicId) => {
      axios.get(
        config.apiURL(`/topic/${topicId}`)
      ).then((res) => {
        setTopicName(res.data.name);
      }).catch((err) => {
        console.log(err);
      });

      readHistory();
      setPeriodicPing(periodicPing ? periodicPing : setInterval(readHistory, 1000));
    }).catch((err) => {
      console.log(err);
      navigate("/404");
    });

  }, []);

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
              { (isMePro && conOnHold || !isMePro && proOnHold) ? " (Pending...)" : "" }
              { mode === REVIEW ? " (DONE)" : "" }
            </p>
          </div>
        </div>
        <div className="level-right">
          <div className="level-item has-text-right">
            <p className="is-size-2 has-text-white">
              { isMePro ? "Proposition" : "Opposition" }
              { (isMePro && proOnHold || !isMePro && conOnHold) ? " (Pending...)" : "" }
              { mode === REVIEW ? " (DONE)" : "" }
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
          >{
              proOnHold || conOnHold ? (
                <div className="column is-2">
                  <div className="control">
                    <input
                      className="input"
                      type="text"
                      value={ window.location.origin + `/debate/${debateId}/join` }
                      readOnly={true}
                    />
                  </div>
                </div>
              ) : (<div></div>)
            }
            <div
              className={ `column is-${proOnHold || conOnHold ? '8' : '10'}` }
            >
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
