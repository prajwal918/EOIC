FROM nginx:1.25-alpine

# Set metadata for maintainability and tracking (Kaizen)
LABEL org.opencontainers.image.source="https://github.com/eoic/eoic"
LABEL org.opencontainers.image.description="EOIC Presentation Web Container"
LABEL maintainer="EOIC Core Team"

# Clear out default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy strictly the src directory containing our code and assets (Wabi-Sabi)
COPY ./src /usr/share/nginx/html

# Establish a robust healthcheck to verify application resilience (Jidoka)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]