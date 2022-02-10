# Structure
`/routers` - All the endpoints of the API\
`crud.py` - All the crud operations used by the endpoints\
`database.py` - Database initialization and configuration\
`dependencies.py` - All dependencies used by the endpoints\
`main.py` - The api server\
`models.py` - All database models\
`README.md` - You're reading it right now\
`requirements.in` - Dependencies of the application\
`requirements.txt` - Dependencies with versions fixed\
`schemas.py` - All Pydantic schemas

# Instructions
1. Download PostgreSQL
   - MacOS: `brew install postgresql`
2. Create `debateit` database
   - `createdb debateit`
3. Login PostgreSQL
   - `psql`
4. Create user `debate` with password `helloworld`
   - `create user debate with password 'helloworld'`
5. Logout
6. Install dependencies
   - `pip3 install -r api/requirements.txt`
7. Run the server
   - `uvicorn api.main:app --reload`