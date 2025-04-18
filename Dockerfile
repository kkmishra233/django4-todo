FROM python:3.13-slim AS origin
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/root/.local/bin/:$PATH"

FROM origin AS pre-build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

FROM origin AS runtime
WORKDIR /app
COPY --from=pre-build /app /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8080"]

FROM origin AS pre-test
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --group tests
COPY . .

FROM origin AS unittest
WORKDIR /app
COPY --from=pre-test /app /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uv", "run", "coverage", "run", "-m", "pytest"]