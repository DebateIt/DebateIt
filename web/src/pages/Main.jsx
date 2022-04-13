import React from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

function Main({ accessToken }) {
    const navigate = useNavigate();

    return (
        <div className="column">
            <div className="section">
                <h2 className="block has-text-white is-size-2">
                    Your Debates
                </h2>
                <div className="columns">
                    <div className="column is-2">
                        <div className="box has-background-success">
                            <div className="content has-text-primary">
                                Are US and China destined to have a war?
                            </div>
                            <span className="is-size-5 has-text-primary">#1</span>
                        </div>
                    </div>
                </div>
                {/* <span className="has-text-white is-family-secondary">
                    You don't have any debates
                </span> */}
            </div>
            <div className="section">
                <h2 className="block has-text-white is-size-2">
                    Your Topics
                </h2>
                <span className="has-text-white is-family-secondary">
                    You don't have any topics. Click the bottom right button to create your first topic!
                </span>
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