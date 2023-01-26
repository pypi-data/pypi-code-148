from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, MissingError
from odoo.addons.queue_job.job import job
from odoo.addons.base_iban.models.res_partner_bank import \
    normalize_iban, pretty_iban, _map_iban_template
from otrs_somconnexio.client import OTRSClient

import re


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    subscription_request_id = fields.Many2one(
        'subscription.request', 'Subscription Request'
    )
    iban = fields.Char(string="IBAN")

    skip_duplicated_phone_validation = fields.Boolean(
        string="Skip duplicated phone validation",
    )

    partner_category_id = fields.Many2many(
        'res.partner.category',
        string='Tags',
        related='partner_id.category_id',
    )
    create_date = fields.Datetime('Creation Date')

    mobile_lead_line_ids = fields.One2many(
        'crm.lead.line', string='Mobile lead lines',
        compute='_compute_mobile_lead_line_ids')

    broadband_lead_line_ids = fields.One2many(
        'crm.lead.line', string='BA lead lines',
        compute='_compute_broadband_lead_line_ids')

    has_mobile_lead_lines = fields.Boolean(
        compute='_compute_has_mobile_lead_lines',
        store=True
    )
    has_broadband_lead_lines = fields.Boolean(
        compute='_compute_has_broadband_lead_lines',
        store=True
    )
    broadband_wo_fix_lead_line_ids = fields.One2many(
        'crm.lead.line', string='BA without fix lead lines',
        compute='_compute_broadband_wo_fix_lead_line_ids'
    )
    broadband_w_fix_lead_line_ids = fields.One2many(
        'crm.lead.line', string='BA with fix lead lines',
        compute='_compute_broadband_w_fix_lead_line_ids'
    )
    phones_from_lead = fields.Char(
        compute='_compute_phones_from_lead',
        store=True
    )

    def _ensure_crm_lead_iban_belongs_to_partner(self, crm_lead):
        partner_bank_ids = crm_lead.partner_id.bank_ids
        partner_iban_list = [bank.sanitized_acc_number for bank in partner_bank_ids]

        if crm_lead.iban and crm_lead.iban not in partner_iban_list:
            self.env['res.partner.bank'].create({
                'acc_type': 'iban',
                'acc_number': crm_lead.iban,
                'partner_id': crm_lead.partner_id.id
            })

    def action_set_won(self):
        for crm_lead in self:
            crm_lead.validate_won()
            crm_lead.validate_icc()
            crm_lead.lead_line_ids.add_activation_notes()
            if crm_lead.iban:
                self._ensure_crm_lead_iban_belongs_to_partner(crm_lead)
        super(CrmLead, self).action_set_won()

    def validate_won(self):
        if self.stage_id != self.env.ref("crm.stage_lead3"):
            raise ValidationError(
                _("The crm lead must be in remesa stage.")
            )

    def validate_icc(self):
        for line in self.lead_line_ids.filtered("is_mobile"):
            if not line.mobile_isp_info.icc:
                raise ValidationError(
                    _('The ICC value of all mobile lines is not filled')
                )
            icc_prefix = self.env['ir.config_parameter'].get_param(
                'somconnexio.icc_start_sequence'
            )
            if (
                not line.mobile_isp_info.icc.startswith(icc_prefix) or
                len(line.mobile_isp_info.icc) != 19
            ):
                raise ValidationError(
                    _('The value of ICC is not right: it must contain '
                      '19 digits and starts with {}').format(icc_prefix)
                )

    @api.depends('lead_line_ids')
    def _compute_mobile_lead_line_ids(self):
        for crm in self:
            crm.mobile_lead_line_ids = (
                crm.lead_line_ids.filtered(lambda p: p.is_mobile)
            )

    @api.depends('mobile_lead_line_ids')
    def _compute_has_mobile_lead_lines(self):
        for crm in self:
            crm.has_mobile_lead_lines = bool(
                crm.mobile_lead_line_ids)

    @api.depends('lead_line_ids')
    def _compute_broadband_lead_line_ids(self):
        for crm in self:
            crm.broadband_lead_line_ids = (
                crm.lead_line_ids.filtered(lambda p: not p.is_mobile)
            )

    @api.depends('broadband_lead_line_ids')
    def _compute_has_broadband_lead_lines(self):
        for crm in self:
            crm.has_broadband_lead_lines = bool(
                crm.broadband_lead_line_ids)

    @api.depends('lead_line_ids')
    def _compute_broadband_wo_fix_lead_line_ids(self):
        for record in self:
            record.broadband_wo_fix_lead_line_ids = (
                record.lead_line_ids.filtered(
                    lambda l: (
                        l.product_id.without_fix
                    )
                )
            )

    @api.depends('lead_line_ids')
    def _compute_broadband_w_fix_lead_line_ids(self):
        for record in self:
            record.broadband_w_fix_lead_line_ids = (
                record.lead_line_ids.filtered(
                    lambda l: (
                        not l.is_mobile and
                        not l.product_id.without_fix
                    )
                )
            )

    @api.depends('lead_line_ids')
    def _compute_phones_from_lead(self):
        for crm in self:
            mbl_phones = crm.lead_line_ids.filtered(
                lambda l: l.mobile_isp_info_phone_number
            ).mapped('mobile_isp_info_phone_number')
            ba_phones = crm.lead_line_ids.filtered(
                lambda l: (
                    l.broadband_isp_info_phone_number and
                    l.broadband_isp_info_phone_number != "-"
                )
            ).mapped('broadband_isp_info_phone_number')
            crm.phones_from_lead = mbl_phones + ba_phones

    def _get_email_from_partner_or_SR(self, vals):
        if vals.get('partner_id'):
            contact_id = vals.get('partner_id')
            model = self.env['res.partner']
        else:
            contact_id = vals.get('subscription_request_id')
            model = self.env['subscription.request']
        return model.browse(contact_id).email

    @api.model
    def create(self, vals):
        if not vals.get("email_from"):
            vals["email_from"] = self._get_email_from_partner_or_SR(vals)
        leads = super(CrmLead, self).create(vals)
        return leads

    def action_set_paused(self):
        paused_stage_id = self.env.ref('crm.stage_lead2').id
        for crm_lead in self:
            crm_lead.write({'stage_id': paused_stage_id})

    def action_set_remesa(self):
        remesa_stage_id = self.env.ref('crm.stage_lead3').id
        for crm_lead in self:
            crm_lead.validate_remesa()
            crm_lead.write({'stage_id': remesa_stage_id})

    def action_set_cancelled(self):
        cancelled_stage_id = self.env.ref('somconnexio.stage_lead5').id
        for crm_lead in self:
            crm_lead.write({
                'stage_id': cancelled_stage_id,
                'probability': 0
            })

    def validate_remesa(self):
        self.ensure_one()
        # Check if related SR is validated
        if not self.partner_id:
            raise ValidationError(
                _("Error in {}: The subscription request related must be validated.").format(self.id)  # noqa
            )
        # Validate IBAN
        if not self._get_bank_from_iban():
            raise ValidationError(
                _("Error in {}: Invalid bank.").format(self.id)
            )
        # Validate phone number
        self._validate_phone_number()

        if self.stage_id != self.env.ref("crm.stage_lead1"):
            raise ValidationError(
                _("The crm lead must be in new stage.")
            )

    def _get_bank_from_iban(self):
        self.ensure_one()
        # Code copied from base_bank_from_iban module:
        # https://github.com/OCA/community-data-files/blob/12.0/base_bank_from_iban/models/res_partner_bank.py#L13  # noqa
        acc_number = pretty_iban(normalize_iban(self.iban)).upper()
        country_code = acc_number[:2].lower()
        iban_template = _map_iban_template[country_code]
        first_match = iban_template[2:].find('B') + 2
        last_match = iban_template.rfind('B') + 1
        bank_code = acc_number[first_match:last_match].replace(' ', '')
        bank = self.env['res.bank'].search([
            ('code', '=', bank_code),
            ('country.code', '=', country_code.upper()),
        ], limit=1)
        return bank

    def _phones_already_used(self, line):
        # Avoid phone duplicity validation with address change leads
        if line.create_reason == 'location_change':
            self.skip_duplicated_phone_validation = True

        if self.skip_duplicated_phone_validation:
            return False

        phone = False
        if line.mobile_isp_info:
            phone = line.mobile_isp_info.phone_number
        else:
            phone = line.broadband_isp_info.phone_number
        if not phone or phone == "-":
            return False
        contracts = self.env["contract.contract"].search([
            ("is_terminated", "=", False),
            "|",
            "|",
            "|",
            ("mobile_contract_service_info_id.phone_number", "=", phone),
            ("vodafone_fiber_service_contract_info_id.phone_number", "=", phone),
            ("mm_fiber_service_contract_info_id.phone_number", "=", phone),
            ("adsl_service_contract_info_id.phone_number", "=", phone),
        ])
        won_stage_id = self.env.ref("crm.stage_lead4").id
        remesa_stage_id = self.env.ref("crm.stage_lead3").id
        new_stage_id = self.env.ref("crm.stage_lead1").id
        order_lines = self.env["crm.lead.line"].search([
            "|",
            ("lead_id.stage_id", "=", won_stage_id),
            ("lead_id.stage_id", "=", remesa_stage_id),
            "|",
            ("mobile_isp_info.phone_number", "=", phone),
            ("broadband_isp_info.phone_number", "=", phone),
        ])
        if contracts or order_lines:
            raise ValidationError(
                _("Error in {}: Contract or validated CRMLead with the same phone already exists.").format(self.id)  # noqa
            )
        new_lines = self.env["crm.lead.line"].search([
            ("lead_id.stage_id", "=", new_stage_id),
            "|",
            ("mobile_isp_info.phone_number", "=", phone),
            ("broadband_isp_info.phone_number", "=", phone),
        ])
        if len(new_lines) > 1:
            raise ValidationError(
                _("Error in {}: Duplicated phone number in CRMLead petitions.").format(self.id)  # noqa
            )

    def _phone_number_portability_format_validation(self, line):
        if line.mobile_isp_info_type == 'portability' or line.broadband_isp_info_type == 'portability':  # noqa
            phone = line.mobile_isp_info_phone_number or line.broadband_isp_info_phone_number  # noqa
            if not phone:
                raise ValidationError(
                    _('Phone number is required in a portability')
                )
            pattern = None
            if line.mobile_isp_info:
                pattern = re.compile(r"^(6|7)?[0-9]{8}$")
                message = _('Mobile phone number has to be a 9 digit number starting with 6 or 7') # noqa
            elif not line.check_phone_number:
                pattern = re.compile(r"^(8|9)?[0-9]{8}$|^-$")
                message = _('Landline phone number has to be a dash "-" or a 9 digit number starting with 8 or 9') # noqa

            isValid = pattern.match(phone) if pattern else True
            if not isValid:
                raise ValidationError(message)

    def _validate_phone_number(self):
        self.ensure_one()
        for line in self.lead_line_ids:
            self._phone_number_portability_format_validation(line)
            self._phones_already_used(line)

    @api.multi
    def action_set_new(self):
        for lead in self:
            new_stage_id = self.env.ref('crm.stage_lead1')
            lead.write({'stage_id': new_stage_id.id})

    @api.multi
    def action_restore(self):
        for lead in self:
            lead.toggle_active()
            new_stage_id = self.env.ref('crm.stage_lead1')
            lead.write({'stage_id': new_stage_id.id})

    @job
    def link_pack_tickets(self):
        fiber_ticket = None
        fiber_ticket_number = ""
        OTRS_client = OTRSClient()
        mobile_ticket_numbers = {
            line.id: line.ticket_number
            for line in self.lead_line_ids
            if line.is_mobile
        }
        mobile_tickets = {
            mobile_ticket_number : OTRS_client.get_ticket_by_number(
                mobile_ticket_number
            )
            for mobile_ticket_number in mobile_ticket_numbers.values()
            if mobile_ticket_number
        }
        for line in [line for line in self.lead_line_ids if line.ticket_number]:
            if line.is_fiber:
                fiber_ticket_number = line.ticket_number
                fiber_ticket = OTRS_client.get_ticket_by_number(fiber_ticket_number)

        if not all(mobile_ticket_numbers.values()) or not fiber_ticket_number:
            raise MissingError(
                "Either mobile or fiber ticket numbers where not found among "
                "the lines of this pack CRMLead")
        if not all(mobile_tickets.values()):
            raise MissingError(
                "Mobile tickets not found in OTRS with ticket_numbers {}".format(
                    ",".join(number
                             for number in mobile_tickets
                             if not mobile_tickets[number]
                             )
                )
            )
        elif not fiber_ticket:
            raise MissingError(
                "Fiber ticket not found in OTRS with ticket_number {}".format(
                    fiber_ticket_number))
        for mobile_ticket in mobile_tickets.values():
            OTRS_client.link_tickets(
                fiber_ticket.tid, mobile_ticket.tid, link_type="ParentChild")
