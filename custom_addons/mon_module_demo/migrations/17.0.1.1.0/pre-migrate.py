def migrate(cr, version):
    """Exécuté AVANT le chargement du nouveau module.
    Ici on pourrait par exemple sauvegarder une colonne qui va être renommée."""
    cr.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name='baam_materiel' AND column_name='categorie'
    """)
    if not cr.fetchone():
        # La colonne n'existe pas encore, rien à préparer — Odoo la créera lui-même
        pass
