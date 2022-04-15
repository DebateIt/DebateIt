import React from 'react';
import PropTypes from 'prop-types';

function DebateCard({ topicName, nthDebate}) {
    return (
        <div className="column is-2">
            <div className="box has-background-success">
                <div className="content has-text-primary">
                    { topicName }
                </div>
                <span className="is-size-5 has-text-primary">#{ nthDebate }</span>
            </div>
        </div>
    );
}

DebateCard.propTypes = {
    topicName: PropTypes.string.isRequired,
    nthDebate: PropTypes.number.isRequired,
};

export default DebateCard;