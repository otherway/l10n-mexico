# -*- coding: utf-8 -*-
# © 2012-2015 Otherway Creatives S.L. <info@otherway.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def unlink(self):
        self.filtered(lambda x: x.internal_number).write(
            {'internal_number': False})
        return super(AccountInvoice, self).unlink()
