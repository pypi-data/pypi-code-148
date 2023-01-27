class Operations(object):

    # These are the ERP integrations
    # Each with a unique ID
    AUTHENTICATE = -1
    GLOBAL = AUTHENTICATE + 1

    # These are the ids of each type client/erp
    QBO = GLOBAL + 1
    ZOHO = QBO + 1
    SAP = ZOHO + 1
    XERO = SAP + 1
    ODOO = XERO + 1
    MS_DYNAMICS = ODOO + 1
    NETSUITE = MS_DYNAMICS + 1
    ERP_NEXT = NETSUITE + 1

    ERP_TYPES = {
        QBO: ("QBO", 1),
        ZOHO: ("ZOHO", 2),
        SAP: ("SAP", 3),
        XERO: ("XERO", 4),
        MS_DYNAMICS: ("MS_DYNAMICS", 5),
        ERP_NEXT: ("ERP_NEXT", 6)
    }

    # These are the operations to be performed in Banking Identity
    # Each with a unique incremental ID

    # Returns Sample Data
    OPERATIONS = -2
    AUTH_GET_TOKEN = OPERATIONS + 1
    AUTH_AUTHORIZE = AUTH_GET_TOKEN + 1

    # All end points are placed in the BANKS_CONF
    # This is to allow easy standardization of the base url, endpoint and operations
    # When calling the APIs, in this case this is done in the resource class read function
    ERP_CONF = {
        AUTHENTICATE: {
            "url": "https://authserver.purplecliff-03d4fbdd.westeurope.azurecontainerapps.io",
            "read": {
                "operations": {
                    AUTH_GET_TOKEN: ("connect/token", "POST"),
                    AUTH_AUTHORIZE: ("connect/authorize", "POST"),
                }
            }

        }
    }
