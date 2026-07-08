from odoo import models, fields, api


class MaterielConstruction(models.Model):
    _name = 'baam.materiel'
    _description = 'Matériel de Construction'

    name = fields.Char(required=True)
    reference = fields.Char()
    quantite = fields.Integer(default=0)
    prix_unitaire = fields.Float()
    fournisseur = fields.Char()
    date_reception = fields.Date()
    valeur_stock = fields.Float(compute='_compute_valeur_stock', store=True)
    categorie = fields.Selection(
        [
            ('gros_oeuvre', 'Gros œuvre'),
            ('second_oeuvre', 'Second œuvre'),
            ('finition', 'Finition'),
        ],
        string='Catégorie',
        default='gros_oeuvre',
    )

    @api.depends('quantite', 'prix_unitaire')
    def _compute_valeur_stock(self):
        for rec in self:
            rec.valeur_stock = rec.quantite * rec.prix_unitaire

    @api.constrains('quantite')
    def _check_quantite(self):
        for rec in self:
            if rec.quantite < 0:
                raise ValueError("La quantité ne peut pas être négative")
