### Setup
`docker-compose build`

#### Connect to your app container
`docker-compose exec app bash`
    
### Accessing the database
`docker exec -it $(docker ps -q -f name=db) psql -U postgres -d db`

### Running the app
`docker-compose up`
`docker exec edvisorly-app-1 python app.py path/to/transcript.pdf`

