import React from 'react';

import Button from '../components/button';

function Topic({ accessToken }) {
    return (
        <div className="column">
            <div className="section">
                <div className="content">
                    <h2 className="has-text-white is-size-2">
                        Should we ban racial slurs on internet?
                    </h2>
                    <h4 className="has-text-white">
                        Number of Debates: 3
                    </h4>
                    <p className="has-text-white is-family-secondary">
                        asdl;fkjasl;dfjaslk;dfj
                    </p>
                </div>
                <div className="buttons">
                    <button className="button is-medium is-success has-text-info">
                        Debate It for proposition!
                    </button>
                    <button className="button is-medium is-success has-text-info">
                        Debate It for opposition!
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Topic;