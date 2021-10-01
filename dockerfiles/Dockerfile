FROM debian
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get update && apt-get -y upgrade 
RUN apt-get install -y apt-utils software-properties-common python3-software-properties build-essential 			
# Set the locale
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 
RUN apt-get -y install locales
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
RUN export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8	
RUN apt-get install -y python3 python3-pymysql python3-openssl python3-dev python3-pip python3-mysqldb python3-rsa python3-psutil mutt wget iproute2 systemd git libarchive-dev  autoconf mc pkg-config vim git-core inetutils-ping mailutils at figlet libcurl4-openssl-dev libjson-c-dev ntpdate libsqlite3-dev sudo openssh-server mariadb-client percona-toolkit				
RUN mkdir -p /var/run/sshd
# authorize SSH connection with root account
#RUN sed -i '/^#/!s/PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN ssh-keygen -A 
RUN sudo service ssh restart
# change password root
RUN echo "root:docker"|chpasswd
RUN git config --global user.email "acasadoalonso@gmail.com" 
RUN git config --global user.name  "Angel Casado"     
RUN set -x \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 install ephem pytz geopy configparser pycountry pyopenssl uritemplate \
    && pip3 install mysqlclient requests mysql-connector-python beeprint ogn.client \
    && pip3 install tqdm psutil rsa python-dateutil  				

ENV TZ=Europe/Madrid
ENV USER=sarogn
RUN dpkg-reconfigure tzdata				
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone	
RUN apt-get -y dist-upgrade					
RUN apt-get -y autoremove	
WORKDIR /var/www/

RUN git clone https://github.com/acasadoalonso/RepoOGN-DataGatheringPart.git main
RUN git clone https://github.com/acasadoalonso/RepoOGN-WEB-files.git         html
RUN mkdir -p /var/www/data
RUN mkdir -p /var/www/local
RUN mkdir -p /var/www/html
RUN mkdir -p /var/www/html/cuc/
RUN mkdir -p /var/www/src
RUN mkdir -p /etc/local 
RUN mkdir -p /nfs/
RUN mkdir -p /nfs/OGN
RUN mkdir -p /nfs/OGN/DIRdata
RUN mkdir -p /nfs/OGN/DIRdata/fd
RUN mkdir -p /nfs/OGN/DIRdata/fd/Y21
RUN mkdir -p /nfs/OGN/DIRdata/log
RUN mkdir -p /nfs/OGN/DIRdata/data
RUN mkdir -p /nfs/OGN/DIRdata/tmp
RUN mkdir -p ~/src
RUN ln -s /var/www/main ~/src/SARsrc 
COPY config.docker /etc/local/SARconfig.ini
COPY DBschema.sql .
COPY SARpogn.docker.sh .
COPY SARboot.docker.sh .
VOLUME /var/www
VOLUME /etc/local
VOLUME /nfs
ARG USER=angel
ARG UID=1000
ARG GID=1000
# default password for user
ARG PW=docker
RUN useradd -m ${USER} --uid=${UID} --shell=/bin/bash && echo "${USER}:${PW}" | \
      chpasswd
RUN echo "Welcome to the SAR application container" > /etc/motd \
    && cp -a /root /root.orig
EXPOSE 80
EXPOSE 81
EXPOSE 22
RUN touch SARinstallation.done	
RUN service ssh restart
WORKDIR /var/www/main/
RUN git config pull.ff only 
RUN echo 'alias ll="ls -la"' >> ~/.bashrc
WORKDIR /nfs/OGN/DIRdata
STOPSIGNAL SIGTERM
#ENTRYPOINT /usr/bin/python3 /var/www/main/SARognES.py
CMD ["/usr/bin/python3", "/var/www/main/SARognES.py" ]
