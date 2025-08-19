FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN addgroup --syste django-group && \
    adduser --system --ingroup django-group --no-create-home --disabled-password django-user

#RUN mkdir -p /code && chown django-user:django-group /code

WORKDIR /code

COPY ./requirements.txt /tmp/requirements.txt

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

COPY ./code /code/
RUN chown -R django-user:django-group /code

USER django-user

ENV PATH="/py/bin:$PATH"

EXPOSE 8000