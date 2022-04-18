import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from "react-router-dom";

function Topic({ accessToken }) {
    const navigate = useNavigate();
    const params = useParams();
    const topicId = params.topicId;
    const [topic, setTopic] = useState({});

    const initiateDebate = (asPro) => () => {
        let params = {
            topic_id: topicId,
            start_time: Date.now(),
        }
        if (asPro) params.as_pro = true;
        else params.as_con = true;

        axios.post('http://localhost:8000/debate', params, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            }
        }).then((res) => {
            navigate(`/debate/${res.data.id}`);
        }).catch((err) => {
            console.log(err);
        });
    }

    useEffect(() => {
        axios.get(
            `http://localhost:8000/topic/${topicId}`
        ).then((res) => {
            setTopic(res.data);
        }).catch((err) => {
            console.log(err);
        });
    }, []);

    return (
        <div className="column">
            <div className="section">
                <div className="content">
                    <h2 className="has-text-white is-size-2">
                        { topic.name }
                    </h2>
                    <h4 className="has-text-white">
                        Number of Debates: { topic.num_of_debates }
                    </h4>
                    <p className="has-text-white is-family-secondary">
                        { topic.description }
                    </p>
                </div>
                <div className="buttons">
                    <button 
                        className="button is-medium is-success has-text-info"
                        onClick={initiateDebate(true)}
                    >
                        Debate It for proposition!
                    </button>
                    <button 
                        className="button is-medium is-success has-text-info"
                        onClick={initiateDebate(false)}
                    >
                        Debate It for opposition!
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Topic;