#FROM debian
FROM ubuntu
RUN apt update -y && apt install mariadb-server -y
RUN sed -i 's/bind-address/bind-address = 0.0.0.0 #/i' /etc/mysql/mariadb.conf.d/50-server.cnf
RUN mkdir /mysql_scripts
COPY mySqlScript.sql /mysql_scripts/
EXPOSE 3306/tcp
#RUN /etc/init.d/mariadb start && mysql -uroot --password="" -e "source /mysql_scripts/mySqlScript.sql"
RUN service mysql start && mysql -uroot --password="" -e "source /mysql_scripts/mySqlScript.sql"
CMD service mysql start && tail -f /dev/null

