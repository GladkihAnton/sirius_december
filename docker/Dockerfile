FROM python:3.11 as base

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

WORKDIR /code

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==1.3.2

COPY pyproject.toml /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev \
    && echo yes | poetry cache clear . --all


# FROM base AS prod

# COPY . .

# RUN mkdir -p /var/log && chmod -R 1777 /var/log

FROM base AS test

RUN poetry install --no-interaction --no-ansi --with dev

COPY scripts/web/startup.sh /scripts/web/startup.sh

RUN chmod u+x /scripts/web/startup.sh

CMD ["/scripts/web/startup.sh", "-m", "-l"]

