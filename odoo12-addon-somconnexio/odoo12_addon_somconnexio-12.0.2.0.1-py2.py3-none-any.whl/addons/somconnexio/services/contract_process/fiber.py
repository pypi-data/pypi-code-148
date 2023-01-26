import logging
from datetime import date, timedelta

from odoo.exceptions import UserError
from otrs_somconnexio.services.unblock_mobile_pack_ticket import UnblockMobilePackTicket

from .ba import BAContractProcess

_logger = logging.getLogger(__name__)


class FiberContractProcess(BAContractProcess):
    _description = """
        Fiber Contract creation
    """

    @staticmethod
    def validate_service_technology_deps(params):
        errors = []
        if "service_address" not in params:
            errors.append('Fiber needs "service_address"')
        if params["service_supplier"] not in ("Vodafone", "Orange", "MásMóvil", "XOLN"):
            errors.append(
                'Fiber needs "Vodafone", "Orange", "MásMóvil" or "XOLN" suppliers'
            )
        else:
            if params["service_supplier"] == "Vodafone":
                if "vodafone_fiber_contract_service_info" not in params:
                    errors.append(
                        "Vodafone Fiber needs vodafone_fiber_contract_service_info"
                    )
                if params.get("fiber_signal_type") == "fibraIndirecta":
                    errors.append(
                        'Fiber signal "Fibra Indirecta" needs MásMóvil supplier'
                    )
            elif params["service_supplier"] == "MásMóvil":
                if "mm_fiber_contract_service_info" not in params:
                    errors.append("MásMóvil Fiber needs mm_fiber_contract_service_info")
                if params.get("fiber_signal_type") in ("fibraCoaxial", "NEBAFTTH"):
                    errors.append(
                        'Fiber signal "{}" needs Vodafone supplier'.format(
                            params["fiber_signal_type"]
                        )
                    )
            elif params["service_supplier"] == "XOLN":
                if "xoln_fiber_contract_service_info" not in params:
                    errors.append("XOLN Fiber needs mm_fiber_contract_service_info")
            elif params["service_supplier"] == "Orange":
                if "orange_fiber_contract_service_info" not in params:
                    errors.append(
                        "Orange Fiber needs orange_fiber_contract_service_info"
                    )
        if errors:
            raise UserError("\n".join(errors))

    def _create_vodafone_fiber_contract_service_info(self, params):
        if not params:
            return False
        return (
            self.env["vodafone.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "phone_number": params["phone_number"],
                    "vodafone_id": params["vodafone_id"],
                    "vodafone_offer_code": params["vodafone_offer_code"],
                }
            )
        )

    def _create_mm_fiber_contract_service_info(self, params):
        if not params:
            return False
        return (
            self.env["mm.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "phone_number": params["phone_number"],
                    "mm_id": params["mm_id"],
                }
            )
        )

    def _create_orange_fiber_contract_service_info(self, params):
        if not params:
            return False
        return (
            self.env["orange.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "suma_id": params["suma_id"],
                }
            )
        )

    def _create_xoln_fiber_contract_service_info(self, params):
        if not params:
            return False
        if "router_mac_address" in params and params["router_mac_address"] != "-":
            router_mac_address = params["router_mac_address"]
        else:
            router_mac_address = False
        router_product = self._get_router_product_id(params["router_product_id"])
        router_lot_id = self._create_router_lot_id(
            params["router_serial_number"],
            router_mac_address,
            router_product,
        )
        project_options = dict(
            self.env["xoln.fiber.service.contract.info"]._fields["project"].selection
        ).keys()
        if params["project"] not in project_options:
            raise UserError("Project %s not found" % (params["project"],))
        return (
            self.env["xoln.fiber.service.contract.info"]
            .sudo()
            .create(
                {
                    "phone_number": params["phone_number"],
                    "external_id": params["external_id"],
                    "id_order": params["id_order"],
                    "project": params["project"],
                    "router_product_id": router_product.id,
                    "router_lot_id": router_lot_id.id,
                }
            )
        )

    def create(self, **params):
        contract_dict = super(FiberContractProcess, self).create(**params)
        # Update mobile tiquets
        self._update_pack_mobile_tickets(contract_dict)

        self._relate_with_mobile_pack(params.get("mobile_pack_contracts"))
        return contract_dict

    def _relate_with_mobile_pack(self, mobile_pack_contracts):
        """
        When we create a contract from address change order,
        we need to relate the parent contract
        """
        if mobile_pack_contracts:
            mobile_contracts = (
                self.env["contract.contract"]
                .sudo()
                .search([("code", "in", set(mobile_pack_contracts.split(",")))])
            )
            for contract in mobile_contracts:
                contract.parent_pack_contract_id = self.id

    def _update_pack_mobile_tickets(self, contract_dict):
        crm_lead_line = self.env["crm.lead.line"].sudo().search(
            [("ticket_number", "=", contract_dict["ticket_number"])]
        )
        mobile_lines = crm_lead_line.lead_id.lead_line_ids.filtered("is_mobile")
        if not mobile_lines:
            return True

        activation_date = self._get_activation_date()
        introduced_date = self._get_introduced_date(activation_date)

        for line in mobile_lines:
            UnblockMobilePackTicket(
                line.ticket_number,
                activation_date=activation_date.strftime("%Y-%m-%d"),
                introduced_date=introduced_date.strftime("%Y-%m-%d")
            ).run()

    def _get_activation_date(self):
        """
        First working day after the 8th day from fiber contract creation
        """
        create_date = date.today()
        activaton_date = create_date + timedelta(days=8)
        holidays = self.env["hr.holidays.public.line"].sudo().search([]).mapped("date")
        while (
            activaton_date in holidays
            or not activaton_date.weekday() < 5  # 5 Sat, 6 Sun
        ):
            activaton_date = activaton_date + timedelta(days=1)
        return activaton_date

    def _get_introduced_date(self, activaton_date):
        """
        Two working days before the incoming activation date
        """
        introduced_date = activaton_date - timedelta(days=2)

        holidays = self.env["hr.holidays.public.line"].sudo().search([]).mapped("date")
        while (
            introduced_date in holidays
            or not introduced_date.weekday() < 5  # 5 Sat, 6 Sun
        ):
            introduced_date = introduced_date - timedelta(days=1)
        return introduced_date
