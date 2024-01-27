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
# Copy the entrypoint script and make it executable
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh
# Create a non-root user
RUN adduser --disabled-password --gecos '' devops
# Set ownership of the application directory to the non-root user
RUN chown -R devops /usr/src/app/
# Set permissions to read and execute only for the devops user
RUN find /usr/src/app/ -type f -exec chmod 500 {} +
RUN find /usr/src/app/ -type d -exec chmod 500 {} +
# Switch to the non-root user
USER devops
# Expose port 8080
EXPOSE 8080
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
