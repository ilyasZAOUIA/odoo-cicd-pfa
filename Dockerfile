FROM odoo:17.0

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY ./custom_addons /mnt/extra-addons

USER odoo
