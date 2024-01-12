ARG PYTHON_VERSION=3.10.0
ARG APP_FOLDER=/app

FROM python:${PYTHON_VERSION}-slim-buster AS builder

ARG APP_FOLDER

FROM builder AS deps_install

WORKDIR /app

COPY pyproject.toml /app/

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==1.3.2 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --with dev \
    && echo yes | poetry cache clear . --all

FROM python:${PYTHON_VERSION}-slim-buster AS release

ARG APP_FOLDER
ARG APP_USER=otp_user
ARG APP_GROUP=otp_group
ARG APP_USER_UID=999
ARG LOG_FOLDER=${APP_FOLDER}/logs


ENV PYTHONPATH="${APP_FOLDER}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Europe/Moscow

RUN groupadd --gid ${APP_USER_UID} --system ${APP_GROUP} && \
    useradd --uid ${APP_USER_UID} \
            --gid ${APP_GROUP} \
            --no-create-home \
            --system \
            --shell /bin/false \
            ${APP_USER}

WORKDIR ${APP_FOLDER}

COPY --from=deps_install /usr/local /usr/local

RUN mkdir -p ${LOG_FOLDER} && chown ${APP_USER}:${APP_GROUP} ${LOG_FOLDER}

COPY --chown=${APP_USER}:${APP_GROUP} . .
