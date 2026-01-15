FROM ictf_base
COPY ./secrets /opt/ictf/secrets

RUN DEBIAN_FRONTEND=noninteractive apt-get clean && apt-get update && apt-get install -y python3-pip --no-install-recommends python3-pip python3-wheel

COPY ./gamebot /opt/ictf/gamebot

WORKDIR /opt/ictf/gamebot
COPY ./secrets /opt/ictf/secrets
COPY ./secrets /opt/ictf/secrets

RUN pip install -r requirements.txt

RUN chmod +x ./start.sh 

RUN ansible-playbook ./provisioning/hephaestus_provisioning/ansible-provisioning.yml --extra-vars ICTF_API_ADDRESS="database.ictf" 

ENTRYPOINT ./start.sh
