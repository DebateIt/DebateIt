from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PRO_USER_ID = None
CON_USER_ID = None
curr_turn = None


@app.get("/history")
def get_debate_history():
    return None


@app.post("/message")
def send_message():
    return None
