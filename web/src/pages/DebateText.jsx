import React from 'react';

import InputBox from '../components/inputbox';

function DebateText() {
    return (
        <div className="column is-flex-direction-column">
            <div className="level">
                <div className="level-item has-text-left">
                    <p className="title has-text-white">For</p>
                </div>
                <div className="level-item has-text-right">
                    <p className="title has-text-white">Against</p>
                </div>
            </div>
            <nav class="navbar is-fixed-bottom">
                <InputBox
                    className="is-flex-grow-1"
                    name="Message"
                />
            </nav>
        </div>
    );
}

export default DebateText;