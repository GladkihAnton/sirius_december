FROM ubuntu:latest
LABEL authors="kenny"

ENTRYPOINT ["top", "-b"]