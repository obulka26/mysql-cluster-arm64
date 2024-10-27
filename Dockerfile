

# https://hub.docker.com/layers/mysql/mysql-cluster/7.5/images/sha256-f5a8c1b74eb63f22dd3cc65b7fb3eb504cce7318c158d9ef9f7a9c0afc94bda9
#ARG MYSQL_SERVER_PACKAGE=mysql-cluster-9.1.0
#ARG MYSQL_SHELL_PACKAGE=mysql-shell-9.1.0

#FROM container-registry.oracle.com/mysql/community-cluster AS cluster
#COPY --from=cluster /entrypoint.sh /entrypoint.sh
#COPY --from=cluster /healthcheck.sh /healthcheck.sh

# https://dev.mysql.com/downloads/cluster/
# https://dev.mysql.com/doc/refman/9.1/en/mysql-cluster-install-linux-binary.html

FROM container-registry.oracle.com/os/oraclelinux:9-slim

ARG MYSQL_SERVER_PACKAGE=mysql-cluster-9.1.0-linux-glibc2.28-aarch64

COPY entrypoint.sh /entrypoint.sh
COPY healthcheck.sh /healthcheck.sh

RUN groupadd mysql
RUN useradd -g mysql -s /bin/false mysql

# tar -C /usr/local -xzvf mysql-cluster-gpl-9.1.0-linux-glibc2.28-aarch64
ADD ${MYSQL_SERVER_PACKAGE}.tar.xz /usr/local

RUN ln -s /usr/local/${MYSQL_SERVER_PACKAGE} /usr/local/mysql

RUN chown -R root /usr/local/mysql
RUN chmod +x /usr/local/mysql/bin/ndb*

RUN rpm -i https://rpmfind.net/linux/centos-stream/9-stream/BaseOS/aarch64/os/Packages/libaio-0.3.111-13.el9.aarch64.rpm
#RUN rpm -i https://rpmfind.net/linux/centos-stream/9-stream/BaseOS/aarch64/os/Packages/numactl-libs-2.0.14-7.el9.aarch64.rpm
RUN rpm -i https://rpmfind.net/linux/centos-stream/9-stream/BaseOS/aarch64/os/Packages/numactl-libs-2.0.16-3.el9.aarch64.rpm 

RUN mkdir -p /var/lib/mysql
RUN chown -R mysql:mysql /var/lib/mysql

RUN mkdir -p /usr/local/mysql/data

RUN mkdir -p /var/lib/mysql-files
RUN chown -R mysql:mysql /var/lib/mysql-files
RUN chmod 750 /var/lib/mysql-files

ENV PATH="$PATH:/usr/local/mysql/bin"
#ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/mysql/lib"


ENTRYPOINT ["/entrypoint.sh"]
HEALTHCHECK CMD /healthcheck.sh


ENV MYSQL_UNIX_PORT=/var/lib/mysql/mysql.sock
EXPOSE 3306 33060-33061 2202 1186
CMD ["mysqld"]




