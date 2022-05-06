const SERVER_IP_ADDR = "http://localhost:8000";

function apiURL(pathToFile) {
    return SERVER_IP_ADDR + pathToFile;
}

const config = {
    SERVER_IP_ADDR,
    apiURL,
};

export default config;
