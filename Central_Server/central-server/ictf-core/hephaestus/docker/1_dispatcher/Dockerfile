FROM rabbitmq:management

ENV RABBITMQ_PID_FILE /var/lib/rabbitmq/mnesia/rabbitmq

COPY ./dispatcher /opt/ictf/dispatcher

WORKDIR /opt/ictf/dispatcher
COPY ./secrets /opt/ictf/secrets

RUN chmod +x ./start.sh

ENTRYPOINT ./start.sh
