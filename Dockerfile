FROM odoo:17.0

USER root

# Dépendances système supplémentaires si besoin
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier nos modules custom dans l'image
COPY ./custom_addons /mnt/extra-addons

USER odoo
