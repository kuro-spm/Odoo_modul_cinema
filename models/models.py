# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 
 
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

    directed_films_ids = fields.One2many('cinema.film', 'director_id', string='Directed Films')
    acted_films_ids = fields.Many2many('cinema.film', string='Acted Films')

    full_name = fields.Char(compute='_compute_full_name', string='Full name')
    
    @api.depends('first_name, last_name')
    def _compute_full_name(self):
        for obj in self:
            if obj.first_name and obj.last_name:
                obj.full_name = obj.last_name + ", " + obj.first_name
            else:
                obj.full_name = ''

    @api.constrains('birthdate, date_of_death')
    def _check_birthdate_date_of_death(self):
        for obj in self:
            if obj.date_of_death and obj.birthdate:
              if obj.date_of_death < obj.birthdate:
                    raise ValidationError(_("Date of death cannot be earlier than the birth date."))
      

class CinemaFilm(models.Model):
    _name = 'cinema.film'
    _description = 'Cinema Film'

    title = fields.Char('Title', size=60, required=True)
    year = fields.Date('year')
    duration = fields.Integer(string='Duration', help='Duration in minutes', required=True)    
    
    director_id = fields.Many2one('cinema.person', string='director')
    type = fields.Char(compute='_compute_type', string='type')
    
    @api.depends('duration')
    def _compute_type(self):
        for obj in self:
            if obj.duration:
                if obj.duration < 30: obj.type='short film'
                elif obj.duration < 60: obj.type='medium-length film'
                else: obj.type = 'full-length film'
            else:
                obj.type='unknown'

    synopsis = fields.Text('synopsis')
    web_page = fields.Char('web page', size=60)
    poster = fields.Binary('poster')




    #campo_id = fields.Many2one('modelo.relacionado', string='Etiqueta') 
    #campos_ids = fields.One2many('modelo.relacionado', 'campo_many2one_relacionado', string='Etiqueta') 
    #campos_ids = fields.Many2many('modelo.relacionado', string='Etiqueta') 
