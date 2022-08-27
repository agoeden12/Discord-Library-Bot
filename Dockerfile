FROM continuumio/miniconda3:4.6.14
WORKDIR /library_bot
COPY . /library_bot/

RUN ["conda", "env", "update", "-f", "/library_bot/env.yaml"]