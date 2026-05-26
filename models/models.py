# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 
 
 
class cinema_maig2025Type(models.Model): 
    _name = 'cinema_maig2025.type' 
    _description = 'Type Management' 
 
    name = fields.Char('Name', size=60, required=True) 


#TODO: Persona, Film, Pais



class CinemaPerson(models.Model):
    _name = 'cinema.person'
    _description = 'Cinema Person Management'
    _rec_name = 'full_name'

    first_name = fields.Char('First Name', size=25, required=True)
    last_name = fields.Char('Last Name', size=45, required=True)
    is_director = fields.Boolean('Is Director')
    is_actor = fields.Boolean('Is Actor')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other','Other')],'Gender')
    birthdate = fields.Date('Birthdate', required=True)
    date_of_death = fields.Date('Date of Death')


    full_name = fields.Char(compute='_compute_full_name', string='Full name')
    
    @api.depends('first_name, last_name')
    def _compute_full_name(self):
        for obj in self:
            if obj.first_name and obj.last_name:
                obj.full_name = obj.last_name + ", " + obj.first_name
            else:
                obj.full_name = ''

    

class CinemaFilm(models.Model):
    _name = 'cinema.film'
    _description = 'Cinema Film'



    #campo_id = fields.Many2one('modelo.relacionado', string='Etiqueta') 
    #campos_ids = fields.One2many('modelo.relacionado', 'campo_many2one_relacionado', string='Etiqueta') 
    #campos_ids = fields.Many2many('modelo.relacionado', string='Etiqueta') 
