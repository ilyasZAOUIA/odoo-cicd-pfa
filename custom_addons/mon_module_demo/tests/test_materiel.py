from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestMateriel(TransactionCase):

    # --- Niveau 1 : tests unitaires ---

    def test_creation_materiel(self):
        """Vérifie qu'on peut créer un matériel correctement"""
        materiel = self.env['baam.materiel'].create({
            'name': 'Ciment CPA 45',
            'quantite': 100,
            'prix_unitaire': 55.0,
        })
        self.assertEqual(materiel.name, 'Ciment CPA 45')
        self.assertEqual(materiel.valeur_stock, 5500.0)

    def test_quantite_negative_interdite(self):
        """Vérifie que la contrainte anti-négatif fonctionne"""
        with self.assertRaises(ValueError):
            self.env['baam.materiel'].create({
                'name': 'Test',
                'quantite': -5,
            })

    # --- Niveau 2 : test d'intégration (simule un vrai processus métier) ---

    def test_processus_reception_et_sortie_stock(self):
        """Simule un vrai flux : réception de matériel, sortie de stock,
        et cohérence du calcul de valeur à chaque étape."""
        materiel = self.env['baam.materiel'].create({
            'name': 'Ciment CPA 45',
            'quantite': 0,
            'prix_unitaire': 55.0,
        })

        # Réception d'une livraison de 200 sacs
        materiel.write({'quantite': materiel.quantite + 200})
        self.assertEqual(materiel.valeur_stock, 11000.0)

        # Sortie de 50 sacs pour un chantier
        materiel.write({'quantite': materiel.quantite - 50})
        self.assertEqual(materiel.quantite, 150)
        self.assertEqual(materiel.valeur_stock, 8250.0)

    # --- Niveau 3 : test de sécurité / droits d'accès ---

    def test_utilisateur_sans_droits_ne_peut_pas_creer(self):
        """Un utilisateur du groupe 'portal' (accès restreint) ne doit pas
        pouvoir créer de matériel, faute de droits suffisants."""
        user_limite = self.env['res.users'].create({
            'name': 'Ouvrier Test',
            'login': 'ouvrier_test_pfa',
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
        })
        with self.assertRaises(Exception):
            self.env['baam.materiel'].with_user(user_limite).create({
                'name': 'Test non autorisé',
                'quantite': 10,
            })
