# API de coleta de dados de clima

## Os dados são coletados no openweather com periodicidade de 5 dias com 3h

### Comandos
python -c "from app.models import create_table create_table()"
docker-compose down  
docker-compose up --build 