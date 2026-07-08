def migrate(cr, version):
    """Exécuté APRES le chargement du nouveau module.
    On assigne une catégorie par défaut à tous les matériels existants
    qui n'en ont pas encore, pour éviter des lignes 'orphelines'."""
    cr.execute("""
        UPDATE baam_materiel
        SET categorie = 'gros_oeuvre'
        WHERE categorie IS NULL
    """)
