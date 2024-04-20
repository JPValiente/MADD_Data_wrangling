# Use the official PostgreSQL image from Docker Hub
FROM postgres:latest

# Set environment variables
ENV POSTGRES_DB=european-soccer
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password

# Copy the SQL script into the Docker container
COPY pg_european_soccer.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
# Change permissions of the SQL script to make it executable
RUN chmod +r /docker-entrypoint-initdb.d/pg_european_soccer.sql
