FROM golang:1.20.0-bullseye AS build

USER root
WORKDIR /code
COPY . ./

RUN make build

FROM debian:bullseye

USER root
WORKDIR /app

COPY --from=build /code/output/ ./
COPY --from=build /code/docker/docker_entry.sh ./

RUN chmod +x /app/*.sh

ENTRYPOINT ["/app/docker_entry.sh"]

CMD ["primary"]
