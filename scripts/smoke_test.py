import xmlrpc.client
import sys

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8069"
DB = sys.argv[2] if len(sys.argv) > 2 else "demo"
USER = "staging@gmail.com"
PASSWORD = "staging"

try:
    common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
    uid = common.authenticate(DB, USER, PASSWORD, {})
    if not uid:
        print("ÉCHEC: authentification refusée")
        sys.exit(1)

    models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

    count = models.execute_kw(DB, uid, PASSWORD, 'baam.materiel', 'search_count', [[]])
    print(f"OK: {count} enregistrements dans baam.materiel")

    test_id = models.execute_kw(DB, uid, PASSWORD, 'baam.materiel', 'create', [{
        'name': 'SMOKE_TEST_TEMPORAIRE',
        'quantite': 1,
        'prix_unitaire': 1.0,
        'categorie': 'gros_oeuvre',
    }])
    models.execute_kw(DB, uid, PASSWORD, 'baam.materiel', 'unlink', [[test_id]])
    print("OK: création et suppression réussies (champ categorie fonctionnel)")
    sys.exit(0)

except Exception as e:
    print(f"ÉCHEC: {e}")
    sys.exit(1)
