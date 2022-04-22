import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

function DebateJoin({ accessToken }) {
    const params = useParams();
    const navigate = useNavigate();
    const debateId = params.debateId;

    useEffect(() => {
        let params = {
            id: debateId,
            as_pro: false,
            as_con: false
        };

        axios.get(
            `http://localhost:8000/debate/${debateId}`
        ).then((res) => {
            if (res.data.pro_user_id === null) {
                params.as_pro = true;
            } else if (res.data.con_user_id === null) {
                params.as_con = true;
            } else {
                console.log("The debate is in progress!");
            }

            return Promise.resolve(params);
        }).then((params) => {
            axios.post('http://localhost:8000/debate/join', params, {
                headers: {
                    Authorization: `Bearer ${accessToken}`,
                },
            }).catch((err) => {
                console.log(err);
            }).then(() => {
                navigate(`/debate/${debateId}`);
            });
        }).catch((err) => {
            console.log(err);
        });
    });

    return (
        <div className="column is-flex is-flex-direction-column is-align-self-center">
            <div className="container">
                <h1 className="is-size-3 has-text-white">
                    Redirecting...
                </h1>
            </div>
        </div>
    );
}

export default DebateJoin;