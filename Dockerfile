FROM python:3.12-slim
WORKDIR /usr/src/app/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY src/ .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
EXPOSE 8080
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]