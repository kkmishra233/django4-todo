# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /usr/src/app/
# Prevent Python from writing bytecode and enable unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Copy only the requirements file to optimize caching
COPY src/requirements.txt .
# Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


# Stage 2: Create the final image
FROM python:3.12-slim
WORKDIR /usr/src/app/
# Prevent Python from writing bytecode and enable unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Copy only the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
# Copy the source code
COPY src/ .
# setup supervisored
RUN apt-get update && \
    apt-get install -y \
    supervisor \
    bc
COPY supervisord.conf /etc/supervisor/supervisord.conf
# Copy uptime script
COPY uptime-check.sh /usr/local/bin/uptime-check.sh
RUN chmod +x /usr/local/bin/uptime-check.sh
# Copy the entrypoint script and make it executable
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
# Expose port 8080
EXPOSE 8080
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]