# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ , tools
from odoo.exceptions import ValidationError 
 
class CinemaPerson(models.Model):
    _name = 'cinema.person'
    _description = 'Cinema Person Management'
    _rec_name = 'full_name'
    _order = 'last_name, first_name, birthdate desc'

    first_name = fields.Char('First Name', size=25, required=True)
    last_name = fields.Char('Last Name', size=45, required=True)
    is_director = fields.Boolean('Is Director', required=True)
    is_actor = fields.Boolean('Is Actor', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other','Other')],'Gender', required=True)
    birthdate = fields.Date('Birthdate', required=True)
    date_of_death = fields.Date('Date of Death')

    directed_films_ids = fields.One2many('cinema.film', 'director_id', string='Directed Films', readonly=True)
    acted_films_ids = fields.Many2many('cinema.film', string='Acted Films' , readonly=True)
    country_id = fields.Many2one('res.country','Citizenship', required=True)

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
      

    def _auto_init(self):
        res = super(CinemaPerson, self)._auto_init()
        # Passem cada columna de manera independent dins de la llista
        tools.create_unique_index(
            self._cr, 
            'cinema_person_unique_name_lastname_birthdate',
            self._table, 
            ['first_name', 'last_name', 'birthdate']
        )
        return res


class CinemaFilm(models.Model):
    _name = 'cinema.film'
    _description = 'Cinema Film'

    title = fields.Char('Title', size=60, required=True)
    year = fields.Date('year', required=True)
    duration = fields.Integer(string='Duration', help='Duration in minutes', required=True)    
    
    director_id = fields.Many2one('cinema.person', string='director')
    type = fields.Char(compute='_compute_type', string='type')
    
    synopsis = fields.Text('synopsis')
    web_page = fields.Char('web page', size=60)
    poster = fields.Binary('poster')

    @api.depends('duration')
    def _compute_type(self):
        for obj in self:
            if obj.duration:
                if obj.duration < 30: obj.type='short film'
                elif obj.duration < 60: obj.type='medium-length film'
                else: obj.type = 'full-length film'
            else:
                obj.type='unknown'

    @api.constrains('year')
    def _constrains_year(self):
        for obj in self:
            if obj.duration:
                if obj.year<1895:
                    raise ValidationError(_('Year must be past 1895.'))

    def _auto_init(self):
        res = super(CinemaFilm, self)._auto_init()
        # Creem un índex únic parcial que ignora els valors buits (NULL)
        self._cr.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS cinema_film_webpage
            ON %s (web_page)
            WHERE web_page IS NOT NULL AND web_page != ''
        """ % self._table)
        return res

    @api.onchange('web_page')
    def _onchange_web_page(self):
        if(self.web_page):
            self.web_page = self.web_page.lower()

    #campo_id = fields.Many2one('modelo.relacionado', string='Etiqueta') 
    #campos_ids = fields.One2many('modelo.relacionado', 'campo_many2one_relacionado', string='Etiqueta') 
    #campos_ids = fields.Many2many('modelo.relacionado', string='Etiqueta') 
