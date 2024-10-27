
## Any Cluster Command help
```
```
docker run  --rm obulka/mysql-cluster ndb_mgmd --help | less
docker run  --rm obulka/mysql-cluster ndb_mgmd --help | less
```
```
## Build image

docker build -t obulka/mysql-cluster .
docker build -t obulka/mysql-cluster --progress=plain .
docker build -t obulka/mysql-cluster --no-cache --progress=plain .


## Up docker compose

(docker compose -f docker-compose.yml up; docker compose -f docker-compose.yml rm -f)

### As daemon
  docker compose -f docker-compose.yml up -d;

#### Stop daemon

  docker compose -f docker-compose.yml stop

##### Remove compose containers  

  docker compose -f docker-compose.yml rm -f
