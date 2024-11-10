
## Any Cluster Command help
```
docker run  --rm obulka/mysql-cluster ndb_mgmd --help | less
docker run  --rm obulka/mysql-cluster ndb_mgmd --help | less
docker run  --rm obulka/mysql-cluster mysqld --help --verbose | less
docker run  --rm obulka/mysql-cluster mysqld --innodb-buffer-pool-size=256M --help --verbose | grep innodb-buffer-pool-size
```
## Build image
```
docker build -t obulka/mysql-cluster .
docker build -t obulka/mysql-cluster --progress=plain .
docker build -t obulka/mysql-cluster --no-cache --progress=plain .
```
## Up docker compose
```
[<cluster>=false] ./compose.sh [<num_nodes>=1]
```
Example:
```
cluster=true ./compose.sh 3
```
## Run tests
```
[<num_nodes>=0] [<empty_threads>=false] [<comments_per_thread>=1000] ./run.sh <num_threads>...
```
Example:
```
num_nodes=2 empty_threads=true comments_per_thread=1000 ./run.sh 1 5 10 50 100
```
