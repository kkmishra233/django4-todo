FROM python:3.13-slim AS origin
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/root/.local/bin/:$PATH"

FROM origin AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .

FROM origin AS runtime
WORKDIR /app
COPY --from=builder /app /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8080
ENTRYPOINT ["/entrypoint.sh"]