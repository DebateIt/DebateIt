import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

function Intro() {
    const navigate = useNavigate();

    return (
        <div className="column is-flex is-flex-direction-column is-align-self-center">
            <div className="container">
                <h1 className="is-size-2 has-text-white">
                    Debate It, The New Way To Debate
                </h1>
                <button
                    type="button"
                    className="button TopicCreateButton is-large is-success has-text-info"
                    onClick={() => {navigate("/topic")}}
                >
                    <span className="icon is-medium">
                        <FontAwesomeIcon className="fa-lg" icon={faPlus} />
                    </span> 
                </button>
            </div>
        </div>
    );
}

export default Intro;