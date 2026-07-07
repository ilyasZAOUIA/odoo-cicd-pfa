from odoo import models, fields, api


class MaterielConstruction(models.Model):
    _name = 'baam.materiel'
    _description = 'Matériel de Construction'

    name = fields.Char(string='Nom du matériel', required=True)
    reference = fields.Char(string='Référence')
    quantite = fields.Integer(default=0)
    prix_unitaire = fields.Float(string='Prix unitaire (DH)')
    fournisseur = fields.Char()
    date_reception = fields.Date(string='Date de réception')

    @api.constrains('quantite')
    def _check_quantite(self):
        for rec in self:
            if rec.quantite < 0:
                raise ValueError("La quantité ne peut pas être négative")

    valeur_stock = fields.Float(string='Valeur totale stock', compute='_compute_valeur_stock', store=True)

    @api.depends('quantite', 'prix_unitaire')
    def _compute_valeur_stock(self):
        for rec in self:
            rec.valeur_stock = rec.quantite * rec.prix_unitaire
