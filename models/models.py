# -*- coding: utf-8 -*-
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError


class CinemaPerson(models.Model):
    _name = 'cinema.person'
    _description = 'Cinema Person Management'
    _rec_name = 'full_name'
    _order = 'last_name asc, first_name asc, birthdate desc'

    first_name = fields.Char('First Name', size=25, required=True)
    last_name = fields.Char('Last Name', size=45, required=True)
    is_director = fields.Boolean('Is Director?', required=True)
    is_actor = fields.Boolean('Is Actor?', required=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        'Gender', required=True
    )
    birthdate = fields.Date('Birthdate', required=True)
    date_of_death = fields.Date('Date of Death')

    directed_films_ids = fields.One2many('cinema.film', 'director_id', string='Directed Films', readonly=True)
    acted_films_ids = fields.Many2many('cinema.film', string='Acted Films', readonly=True)
    country_id = fields.Many2one('res.country', 'Citizenship', required=True)

    full_name = fields.Char(compute='_compute_full_name', string='Full name', store=True)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for obj in self:
            if obj.first_name and obj.last_name:
                obj.full_name = obj.last_name + ", " + obj.first_name
            else:
                obj.full_name = ''

    @api.constrains('birthdate', 'date_of_death')
    def _check_birthdate_date_of_death(self):
        for obj in self:
            if obj.date_of_death and obj.birthdate:
                if obj.date_of_death < obj.birthdate:
                    raise ValidationError(_("Date of death cannot be earlier than the birth date."))

    def _auto_init(self):
        res = super(CinemaPerson, self)._auto_init()
        tools.create_unique_index(
            self._cr,
            'cinema_person_unique_name_lastname_birthdate',
            self._table,
            ['lower(first_name)', 'lower(last_name)', 'birthdate']
        )
        return res

    def unlink(self):
        for obj in self:
            num_directed = len(obj.directed_films_ids)
            num_acted = len(obj.acted_films_ids)
            total_films = num_directed + num_acted

            if total_films > 0:
                raise ValidationError(_(
                    "Cannot delete %s because they are linked to %s directed film(s) and %s acted film(s)."
                ) % (obj.full_name, num_directed, num_acted))

        return super(CinemaPerson, self).unlink()


class CinemaFilm(models.Model):
    _name = 'cinema.film'
    _description = 'Cinema Film'
    _order = 'title asc, year desc'

    title = fields.Char('Title', size=60, required=True, translate=True)
    year = fields.Date('Year', required=True)
    duration = fields.Integer(string='Duration', help='Duration in minutes', required=True)

    actors_ids = fields.Many2many('cinema.person', string='Actors')
    director_id = fields.Many2one('cinema.person', string='Director')
    director_citizenship = fields.Many2one(
        comodel_name='res.country',
        related='director_id.country_id',
        string='Director Citizenship',
        readonly=True
    )
    type = fields.Char(compute='_compute_type', string='Type', translate=True)

    synopsis = fields.Text('Synopsis', translate=True)
    web_page = fields.Char('Web Page', size=60)
    poster = fields.Image('Poster')

    @api.depends('duration')
    def _compute_type(self):
        for obj in self:
            if obj.duration:
                if obj.duration < 30:
                    obj.type = 'Curtmetratge'
                elif obj.duration < 60:
                    obj.type = 'Migmetratge'
                else:
                    obj.type = 'Llargmetratge'
            else:
                obj.type = 'Desconegut'

    @api.constrains('year')
    def _constrains_year(self):
        for obj in self:
            if obj.year:
                if obj.year.year < 1895:
                    raise ValidationError(_('Year must be 1895 or later (first film ever recorded).'))

    def _auto_init(self):
        res = super(CinemaFilm, self)._auto_init()
        self._cr.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS cinema_film_webpage
            ON %s (lower(web_page))
            WHERE web_page IS NOT NULL AND web_page != ''
        """ % self._table)
        return res

    @api.onchange('web_page')
    def _onchange_web_page(self):
        if self.web_page:
            self.web_page = self.web_page.lower()


class ResCountry(models.Model):
    _inherit = 'res.country'

    director_ids = fields.One2many('cinema.person', 'country_id', string='Directors')
    qt_directors = fields.Integer(compute='_compute_qt_directors', string='Qt Directors')

    @api.depends('director_ids')
    def _compute_qt_directors(self):
        for obj in self:
            obj.qt_directors = len(obj.director_ids)
