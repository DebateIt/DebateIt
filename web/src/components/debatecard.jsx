import React from 'react';
import PropTypes from 'prop-types';

function DebateCard({ debateId, topicName, nthDebate }) {
    return (
        <div className="column is-2">
            <a href={ `/debate/${debateId}` } className="box has-background-success">
                <div className="content has-text-primary">
                    { topicName }
                </div>
                <span className="is-size-5 has-text-primary">#{ nthDebate }</span>
            </a>
        </div>
    );
}

DebateCard.propTypes = {
    debateId: PropTypes.number.isRequired,
    topicName: PropTypes.string.isRequired,
    nthDebate: PropTypes.number.isRequired,
};

export default DebateCard;