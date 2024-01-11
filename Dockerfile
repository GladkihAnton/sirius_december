FROM python:3.11 as base

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

# RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir poetry==1.3.2

# COPY pyproject.toml /code/

# RUN poetry config virtualenvs.create false \
#     && poetry install --no-interaction --no-ansi --without dev \
#     && echo yes | poetry cache clear . --all
# #
# ## stand image
# #FROM base AS prod
#
#COPY . .
#
#RUN mkdir -p /var/log && chmod -R 1777 /var/log
#
#USER 1001
