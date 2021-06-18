# Copyright 2021 ACSONE SA/NV
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _


class RecurrenceMixin(models.AbstractModel):

    _name = 'recurrence.mixin'
    _description = 'Recurrence Mixin'
    _field_last_recurrency_date = None
    _field_next_recurrency_date = None

    # Scheduling
    recurrence_type = fields.Selection([
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("monthlylastday", "Monthly Last Day"),
        ("quarterly", "Quarterly"),
        ("semesterly", "Semesterly"),
        ("yearly", "Yearly"),
    ])

    @api.model
    def get_relative_delta(self, recurring_rule_type, interval):
        """Return a relativedelta for one period.

        When added to the first day of the period,
        it gives the first day of the next period.
        """
        if recurring_rule_type == "daily":
            return relativedelta(days=interval)
        elif recurring_rule_type == "weekly":
            return relativedelta(weeks=interval)
        elif recurring_rule_type == "monthly":
            return relativedelta(months=interval)
        elif recurring_rule_type == "monthlylastday":
            return relativedelta(months=interval, day=1)
        elif recurring_rule_type == "quarterly":
            return relativedelta(months=3 * interval)
        elif recurring_rule_type == "semesterly":
            return relativedelta(months=6 * interval)
        elif recurring_rule_type == "yearly":
            return relativedelta(years=interval)
        else:
            raise NotImplementedError()

    def _get_next_recurrency_date(self):
        self.ensure_one()
        return self[self._field_last_recurrency_date] + \
            self.get_relative_delta(self.recurrence_type, 1)

    def _set_next_recurrency_date(self):
        self[self._field_last_recurrency_date] = fields.Datetime.now()
        self[self._field_next_recurrency_date] = self._get_next_recurrency_date()
