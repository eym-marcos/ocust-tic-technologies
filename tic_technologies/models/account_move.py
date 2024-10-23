from odoo import api, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('journal_id', 'partner_id', 'company_id', 'move_type', 'debit_origin_id', 'l10n_pe_edi_operation_type')
    def _compute_l10n_latam_available_document_types(self):
        super(AccountMove, self)._compute_l10n_latam_available_document_types()
        # EXTENDS 'l10n_latam_invoice_document'
        pe02_moves = self.filtered(
            lambda move: (
                    move.state == 'draft'
                    and move.country_code == 'PE'
                    and move.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code != '6'
                    and move.l10n_pe_edi_operation_type in (
                        '0200', '0201', '0202', '0203', '0204', '0205', '0206', '0207', '0208')
                    and move.journal_id.type == 'sale'
            )
        )
        for rec in pe02_moves.filtered(lambda move: move.move_type == 'out_invoice'):
            rec.l10n_latam_available_document_type_ids = self.env.ref('l10n_pe.document_type01') | self.env.ref('l10n_pe.document_type08') | self.env.ref('l10n_pe.document_type02')
        for rec in pe02_moves.filtered(lambda move: move.move_type == 'out_refund'):
            rec.l10n_latam_available_document_type_ids = self.env.ref('l10n_pe.document_type02')
        # return super(AccountMove, self - pe02_moves)._compute_l10n_latam_available_document_types()
