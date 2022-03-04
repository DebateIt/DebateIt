import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import PropTypes from 'prop-types';

import InputBox from '../components/inputbox';
import Textarea from '../components/textarea';
import Button from '../components/button';

function TopicCreate({ accessToken }) {
    const navigate = useNavigate();

    useEffect(() => {
        if (accessToken === null) {
            navigate('/login');
        }
    });

    const [topicName, setTopicName] = useState('');
    const [topicNameInfo, setTopicNameInfo] = useState('');
    const [description, setDescription] = useState('');

    const fieldOnChange = (setState) => (event) => {
        setState(event.target.value);
    };

    const createTopic = () => {
        axios.post('http://localhost:8000/topic', {
            name: topicName,
            description,
        }, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        }).then((res) => {
            navigate('/');
        }).catch((err) => {
            setTopicNameInfo(err.response.data.detail);
        });
    };

    return (
        <div className="column is-flex is-flex-direction-column is-align-self-center">
            <div
                className=""
                style={{
                    margin: "0 10em 0 10em"
                }}
            >
                <InputBox
                    name="Name"
                    onChange={fieldOnChange(setTopicName)}
                    helpInfo={topicNameInfo}
                />
                <Textarea
                    name="Description"
                    onChange={fieldOnChange(setDescription)}
                />
                <div className="field">
                    <div className="field-body">
                        <Button name="Create" onClick={createTopic} />
                    </div>
                </div>
            </div>
        </div>
    );
}

TopicCreate.propTypes = {
    accessToken: PropTypes.string,
}

export default TopicCreate;