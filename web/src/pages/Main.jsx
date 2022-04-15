import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import jwt_decode from 'jwt-decode';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

import DebateCard from '../components/debatecard';
import axios from 'axios';

function Main({ accessToken }) {
    const user_id = jwt_decode(accessToken).id;
    const navigate = useNavigate();
    const [debates, setDebates] = useState([]);
    const [topics, setTopics] = useState([]);

    useEffect(() => {
        // Remeber to change it back to using user_id
        axios.get(
            `http://localhost:8000/debate/debator/2`
        ).then((res) => {
            setDebates(res.data);
        }).catch((err) => {
            console.log(err.response.data.detail);
        });
    }, []);
    console.log(debates);

    useEffect(() => {
        axios.get(
            `http://localhost:8000/topic/ownedby/2`
        ).then((res) => {
            setTopics(res.data);
        }).catch((err) => {
            console.log(err.response.data.detail);
        });
    }, []);

    const debateCards = debates.map(d => (
        <DebateCard
            key={d.id}
            topicName={d.name}
            nthDebate={d.nth_time_of_debate}
        />
    ));

    const topicRows = topics.map(t => (
        <div key={t.id} className="columns has-text-white is-family-secondary">
            <div className="column is-three-thirds">
                <span>
                    { t.name }
                </span>
            </div>
            <div className="column">
                <span>
                    { t.num_of_debates }
                </span>
            </div>
        </div>
    ))

    return (
        <div className="column">
            <div className="section">
                <h2 className="block has-text-white is-size-2">
                    Your Debates
                </h2>
                <div>
                    <div className="columns">{ debateCards }</div>
                </div>
                {/* <span className="has-text-white is-family-secondary">
                    You don't have any debates
                </span> */}
            </div>
            <div className="section">
                <h2 className="block has-text-white is-size-2">
                    Your Topics
                </h2>
                <div>
                    <div className="columns has-text-white is-size-4">
                        <div className="column is-three-thirds">
                            <span>
                                Topic
                            </span>
                        </div>
                        <div className="column">
                            <span>
                                Number of Debates
                            </span>
                        </div>
                    </div>
                    { topicRows }
                </div>
                {/* <span className="has-text-white is-family-secondary">
                    You don't have any topics. Click the bottom right button to create your first topic!
                </span> */}
            </div>
            <button
                type="button"
                className="button TopicCreateButton is-large is-success has-text-info"
                onClick={() => { navigate('/topic'); }}
            >
                <span className="icon is-medium">
                    <FontAwesomeIcon className="fa-lg" icon={faPlus} />
                </span>
            </button>
        </div>
    )
}

Main.propTypes = {
    accessToken: PropTypes.string,
};

export default Main;