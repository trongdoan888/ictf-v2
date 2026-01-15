FROM ictf_base
COPY ./secrets /opt/ictf/secrets

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y python3-pip nginx uwsgi uwsgi-plugin-python3 mysql-server python3-pip python3-virtualenv python3-mysqldb python3-dev python3-setuptools python3-wheel cron daemon
RUN pip install --upgrade pip

COPY ./database /opt/ictf/database
COPY ./database/secrets /opt/ictf/secrets
COPY ./database/secrets /opt/ictf/secrets
COPY ./scoring_ictf /opt/ictf/scoring_ictf

WORKDIR /opt/ictf/database
COPY ./database/secrets /opt/ictf/secrets
COPY ./secrets /opt/ictf/secrets
COPY ./secrets /opt/ictf/secrets
COPY ./secrets ./secrets

RUN chmod +x ./start.sh && ansible-playbook ./provisioning/hephaestus_provisioning/ansible-provisioning.yml

ENTRYPOINT ./start.sh
