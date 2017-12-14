# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    info@vauxoo.com
############################################################################
#    Coded by: moylop260 (moylop260@vauxoo.com)
#    Coded by: isaac (isaac@vauxoo.com)
############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _

class account_invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        
        res =  super(account_invoice, self).onchange_partner_id(type, partner_id,
            date_invoice=date_invoice, payment_term=payment_term, 
            partner_bank_id=partner_bank_id, company_id=company_id)
        pay_method_id = False
        p = self.env['res.partner'].browse(partner_id or False)
        if partner_id:
            pay_method_id = partner_id and p.pay_method_id and \
                p.pay_method_id.id or False
        res['value']['pay_method_ids'] = [pay_method_id]
        return res

    @api.multi
    def onchange_payment_term_date_invoice(self, payment_term_id, date_invoice):

        res =  super(account_invoice, self).onchange_payment_term_date_invoice(
            payment_term_id, date_invoice)
        forma_pago = 'PAGO EN UNA SOLA EXHIBICION'
        p = self.env['account.payment.term'].browse(payment_term_id or False)
        if payment_term_id and p.line_ids and len(p.line_ids) > 1:
            forma_pago = 'PAGOS EN PARCIALIDADES'
        res['value']['forma_pago'] = forma_pago
        return res
    
    forma_pago = fields.Char('Forma de Pago', required=False)
    pay_method_ids = fields.Many2many('pay.method', 
        'account_invoice_pay_method_rel', 
        'invoice_id', 'pay_method_id', 'Métodos de Pago')
    pay_method_id = fields.Many2one('pay.method', 'Payment Method',
        readonly=True, states={'draft': [('readonly', False)]},
            help='Indicates the way it was paid or will be paid the invoice,\
            where the options could be: check, bank transfer, reservoir in \
            account bank, credit card, cash etc. If not know as will be \
            paid the invoice, leave empty and the XML show “Unidentified”.')
    acc_payment = fields.Many2one('res.partner.bank', 'Account Number',
        readonly=True, states={'draft': [('readonly', False)]},
            help='Is the account with which the client pays the invoice, \
            if not know which account will used for pay leave empty and \
            the XML will show "“Unidentified”".')


            