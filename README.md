
## Any Cluster Command help
```
docker run  --rm obulka/mysql-cluster ndb_mgmd --help | less
docker run  --rm obulka/mysql-cluster ndb_mgmd --help | less
```
## Build image
```
docker build -t obulka/mysql-cluster .
docker build -t obulka/mysql-cluster --progress=plain .
docker build -t obulka/mysql-cluster --no-cache --progress=plain .
```
## Up docker compose
```
./compose.sh [<num_nodes>=1]
```
Example:
```
./compose.sh 3
```
## Run tests
```
[<empty_threads>] [<comments_per_thread>=1000] ./run.sh <num_threads>...
```
Example:
```
empty_threads=1 comments_per_thread=1000 ./run.sh 1 5 10 50 100
```
