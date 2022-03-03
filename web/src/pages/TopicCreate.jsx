import React from 'react';

import InputBox from '../components/inputbox';
import Textarea from '../components/textarea';
import Button from '../components/button';

function TopicCreate() {
    return (
        <div className="column is-flex is-flex-direction-column is-align-self-center">
            <div
                className=""
                style={{
                    margin: "0 30em 0 30em"
                }}
            >
                <InputBox name="Name" />
                <Textarea name="Description" />
                <div className="field">
                    <div className="field-body">
                        <Button name="Create" />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default TopicCreate;