import React from 'react';
import PropTypes from 'prop-types';

function Message({ content, isYourTurn }) {
    return (
        <div className="columns">
            <div className={`column is-half ${
                isYourTurn ? "is-offset-half" : ""
            }`}>
                <div className={`box ${
                    isYourTurn
                    ? "has-background-success" : "has-background-primary"
                }`}>
                    <p className={
                        isYourTurn ? "has-text-primary" : "has-text-white"
                    }>
                        { content }
                    </p>
                </div>
            </div>
        </div>
    );
}

Message.propTypes = {
    content: PropTypes.string.isRequired,
    isYourTurn: PropTypes.bool.isRequired,
};

export default Message;
