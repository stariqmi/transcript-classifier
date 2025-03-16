### Setup
docker-compose build
docker-compose up


### Migrations

# Connect to your app container
docker-compose exec app bash

# Create a new migration
alembic revision --autogenerate -m "create catalogue table"

# Upgrade the database
alembic upgrade head

### Accessing the database

docker exec -it $(docker ps -q -f name=db) psql -U postgres -d db

### Running the app

echo "Machine learning and artificial intelligence concepts" | python app.py

