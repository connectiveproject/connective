FROM gitpod/workspace-full:latest

# increment by one to re-run dockerfile commands without cache
ENV INVALIDATE_CACHE=4

# Install PostgreSQL
RUN sudo install-packages postgresql-12 postgresql-contrib-12

# Setup PostgreSQL server for user gitpod
ENV PATH="$PATH:/usr/lib/postgresql/12/bin"
ENV PGDATA="/workspace/.pgsql/data"
RUN mkdir -p ~/.pg_ctl/bin ~/.pg_ctl/sockets \
 && printf '#!/bin/bash\n[ ! -d $PGDATA ] && mkdir -p $PGDATA && initdb -D $PGDATA\npg_ctl -D $PGDATA -l ~/.pg_ctl/log -o "-k ~/.pg_ctl/sockets" start\n' > ~/.pg_ctl/bin/pg_start \
 && printf '#!/bin/bash\npg_ctl -D $PGDATA -l ~/.pg_ctl/log -o "-k ~/.pg_ctl/sockets" stop\n' > ~/.pg_ctl/bin/pg_stop \
 && chmod +x ~/.pg_ctl/bin/*
ENV PATH="$PATH:$HOME/.pg_ctl/bin"
ENV DATABASE_URL="postgresql://gitpod@localhost"
ENV PGHOSTADDR="127.0.0.1"
ENV PGDATABASE="postgres"

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/
RUN sudo apt-get update  && sudo apt-get install -y   redis-server  && sudo rm -rf /var/lib/apt/lists/* && brew update && brew install mailhog

RUN echo "export PIP_USER=false" >> /home/gitpod/.bashrc
RUN echo "export CELERY_BROKER_URL=redis://localhost:6379/0" >> /home/gitpod/.bashrc
RUN sudo apt-get update  && sudo apt-get install -y   redis-server  && sudo rm -rf /var/lib/apt/lists/* && brew update && brew install mailhog

COPY server/requirements temp_requirements

RUN pip install -r temp_requirements/local.txt

COPY . .

RUN echo "export PIP_USER=false" >> /home/gitpod/.bashrc
RUN echo "export CELERY_BROKER_URL=redis://localhost:6379/0" >> /home/gitpod/.bashrc
