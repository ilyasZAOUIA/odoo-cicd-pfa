from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestMateriel(TransactionCase):

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
