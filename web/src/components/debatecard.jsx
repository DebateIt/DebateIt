import React from 'react';
import PropTypes from 'prop-types';

function DebateCard({ debateId, topicName, nthDebate, isActive }) {
    return (
        <div className="column is-2">
            <a
                href={ `/debate/${debateId}` }
                className={
                    `box ${isActive ? "has-background-success" : "has-background-primary"} `
                }
            >
                <div
                    className={ `content ${isActive ? "has-text-primary" : "has-text-white"}` }
                >
                    { topicName }
                </div>
                <span
                    className={ `is-size-5 ${isActive ? "has-text-primary" : "has-text-white"}` }
                >
                    #{ nthDebate }
                </span>
            </a>
        </div>
    );
}

DebateCard.propTypes = {
    debateId: PropTypes.number.isRequired,
    topicName: PropTypes.string.isRequired,
    nthDebate: PropTypes.number.isRequired,
    isActive: PropTypes.bool.isRequired
};

export default DebateCard;