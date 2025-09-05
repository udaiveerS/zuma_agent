FROM postgres:16-alpine

# Install additional extensions if needed
RUN apk add --no-cache \
    postgresql-contrib

# Set environment variables
ENV POSTGRES_DB=chatdb
ENV POSTGRES_USER=chatuser
ENV POSTGRES_PASSWORD=chatpass
ENV PGDATA=/var/lib/postgresql/data/pgdata

# Create custom directory for initialization scripts
COPY scripts/init/ /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB} || exit 1
