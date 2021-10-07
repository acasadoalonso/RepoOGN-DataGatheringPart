docker run --net mynetsql --ip 172.18.0.6 --name sarogn --restart unless-stopped -d sarogn:latest
docker exec -it sarogn python3 /var/www/main/SARcalsunrisesunset.py
