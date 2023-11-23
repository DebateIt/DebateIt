# Debate It
This is a 1 vs 1 open debate app designed and implemented by
- [Tian(Maxwell) Yang](https://github.com/AlpacaMax)(Leader, Scrum Master, Frontend Dev)
- [Jingyang(Simon) Men](https://github.com/SimonMen65)(Backend Dev)
- [Hao Wu](https://github.com/flyhawk86)(Backend Dev)
- [Yi Lu](https://github.com/Leobrook121)(Initial Brainstorming and Designing)

It is a design project for CS-UY 4513 Software Engineering and CS-UY 4523 Design Project at NYU Tandon taught by Professor Fred Strauss.

## Repo Structure

`.github` - Github Actions

`design` - Stores some design graphs

`web` - Frontend code, written in `Javascript` and `React.js`

`api` - Backend code, written in `Python3` and `Fastapi`

`.gitignore` - Ignore generated files

`CONTRIBUTING.md` - Some git usage guidelines for this project

`README.md` - You're reading it right now

## Install Dependencies
```
cd api
pip install -r requirements.txt
cd ../web
npm install
```

## Run

Open one terminal and type:
```
uvicorn api.main:app --host:0.0.0.0 --reload
```

Open another one and type:
```
cd web
npm start
```

And visit the provided link 
