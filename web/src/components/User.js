function User() {
    return (
        <div className="column is-flex is-flex-direction-column is-align-self-center">
            <div className="container is-max-desktop">
                <div className="field is-horizontal">
                    <div className="field-label is-normal">
                        <label className="label">Username:</label>
                    </div>
                    <div className="field-body">
                        <div className="field">
                            <p class="control is-expanded">
                                <input class="input" type="text" placeholder="Username" />
                            </p>
                        </div>
                    </div>
                </div>
                <div className="field is-horizontal">
                    <div className="field-label is-normal">
                        <label className="label">Password:</label>
                    </div>
                    <div className="field-body">
                        <div className="field">
                            <p class="control is-expanded">
                                <input class="input" type="text" placeholder="Password" />
                            </p>
                        </div>
                    </div>
                </div>
                <div className="field is-horizontal">
                    <div className="field-label"></div>
                    <div className="field-body">
                        <div className="field">
                            <button className="button">
                                Save
                            </button>
                        </div>
                        <div className="field">
                            <button className="button">
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default User;