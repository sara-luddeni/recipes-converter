ARG UV_VERSION=0.9.26
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-source
FROM ubuntu:24.04 AS base

ENV UV_NO_SYNC=1
COPY --from=uv-source /uv /uvx /bin/

WORKDIR /app
COPY . /app/

RUN uv sync
CMD ["bash"]
