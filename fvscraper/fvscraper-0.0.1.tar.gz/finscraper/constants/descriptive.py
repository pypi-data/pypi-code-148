filters = {
    "exchange": {
        "short": "exch_",
        "values": ["amex", "nasd", "nyse"]
    },

    "market cap": {
        "short": "cap_",
        "values": [
            "mega", "large", "mid", "small", "micro", "nano",
            "largeover", "midover", "smallover", "microover"
            "largeunder", "midunder", "smallunder", "microunder"

        ]
    },

    "earnings date": {
        "short": "earningsdate_",
        "values": [
            "today", "todaybefore", "todayafter",
            "tomorrow", "tomorrowbefore", "tomorrowafter",
            "yesterday", "yesterdaybefore", "yesterdayafter",
            "nextdays5", "prevdays5", "thisweek",
            "nextweek", "prevweek", "thismonth"
        ]

    },

    "target price": {
        "short": "targetprice_",
        "values": [
            "a50", "a40", "a30", "a20", "a10", "a5", "above", "below",
            "b5", "b10", "b20", "b30", "b40", "b50"
        ]
    },

    "index": {
        "short": "idx_",
        "values": [
            "sp500", "dji"
        ]
    },

    "dividend yield": {
        "short": "fa_div_",
        "values": [
            "none", "pos", "high", "veryhigh",
            "o1", "o2", "o3", "o4", "o5",
            "o6", "o7", "o8", "o9", "o10"
        ]
    },

    "average volume": {
        "short": "sh_avgvol_u500_",
        "values": [
            "u50", "u100", "u500", "u750", "u1000",
            "o50", "o100", "o500", "o750", "o1000", "o2000",
            "100to500", "100to1000", "500to1000", "500to10000"
        ]
    },

    "ipo date": {
        "short": "ipodate_",
        "values": [
            "today", "yesterday", "prevweek", "prevmonth", "prevquarter",
            "prevyear", "prev2years", "prev3years", "prev5years",
            "more1", "more5", "more10", "more15", "more20", "more25"
        ]
    },

    "sector": {
        "short": "sec_",
        "values": [
            "basicmaterials", "communicationservices", "consumercyclical", "consumerdefensive",
            "energy", "financial", "healthcare", "industrials", "realestate", "technology",
            "utilities",
        ]
    },

    "float short": {
        "short": "sh_short_",
        "values": [
            "low", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "020", "025", "030",
        ]
    },

    "relative volume": {
        "short": "sh_relvol_",
        "values": [
            "o10", "o5", "o3", "o3", "o2", "o1.5", "o1", "o0.75", "o0.5", "o0.25",
            "u2", "u1.5", "u1", "u0.75", "u0.5", "u0.25", "u0.1"
        ]
    },

    "shares outstanding": {
        "short": "sh_outstanding",
        "values": [
            "u1", "u5", "u10", "u20", "u50", "u100",
            "o1", "o2", "o5", "o10", "o20", "o50", "o100", "o200", "o500", "o1000"
        ]
    },

    "industry": {
        "short": "ind_",
        "values": [
            "stocksonly", "exchangetradedfund", "advertisingagencies", "aerospacedefense",
            "agriculturalinputs", "airlines", "airportsairservices", "aluminum", "apparelmanufacturing",
            "apparelretail", "assetmanagement", "automanufacturers", "autoparts", "autotruckdealerships",
            "banksdiversified", "banksregional", "beveragesbrewers", "beveragesnonalcoholic", "beverageswineriesdistilleries",
            "biotechnology", "broadcasting", "buildingmaterials", "buildingproductsequipment", "businessequipmentsupplies",
            "capitalmarkets", "chemicals", "closedendfunddebt", "closedendfundequity", "closedendfundforeign", "cokingcoal",
            "communicationequipment", "computerhardware", "confectioners", "conglomerates", "consultingservices", "consumerelectronics",
            "copper", "creditservices", "departmentstores", "diagnosticsresearch", "discountstores", "drugmanufacturersgeneral",
            "drugmanufacturersspecialtygeneric", "educationtrainingservices", "electricalequipmentparts", "electroniccomponents",
            "electronicgamingmultimedia", "electronicscomputerdistribution", "engineeringconstruction", "entertainment",
            "exchangetradedfund", "farmheavyconstructionmachinery", "farmproducts", "financialconglomerates",
            "financialdatastockexchanges", "fooddistribution", "footwearaccessories", "furnishingsfixturesappliances",
            "gambling", "gold", "grocerystores", "healthcareplans", "healthinformationservices", "homeimprovementretail",
            "householdpersonalproducts", "industrialdistribution"
        ]
    },

    "analyst recommendation": {
        "short": "an_recom_",
        "values": [
            "buybetter", "buy",
            "holdbetter", "hold", "holdworse",
            "sell", "sellworse", "strongsell",
        ]},

    "current volume": {
        "short": "sh_curvol_",
        "values": [
            "u50", "u100", "u500", "u750", "u1000",
            "o0", "o50", "o100", "o200", "o300", "o400", "o500", "o750",
            "o1000", "o2000", "o5000", "o10000", "o20000"
        ],
    },

    "float": {
        "short": "sh_float_",
        "values": [
            "u1", "u5", "u10", "u20", "u50", "u100",
            "o1", "o2", "o5", "o10", "o20", "o50", "o100", "o200", "o500", "o1000"
        ]
    },

    "country": {
        "short": "geo_",
        "values": [
            "usa", "not_usa", "asia", "europe", "latinamerica", "bric"
        ]
    },

    "option/short": {
        "short": "sh_opt_",
        "values": ["option", "short", "optionshort"],
    },

    "price": {
        "short": "sh_price",
        "values": [
            "u1", "u2", "u3", "u4", "u5", "u7", "u10", "u15", "u20", "u30", "u40", "u50",
            "o1", "o2", "o3", "o4", "o5", "o7", "o10", "o15", "o20", "o30", "o40", "o50",
            "o60", "o70", "o80", "o90", "o100",
            "1to5", "1to10", "1to20",
            "5to10", "5to20", "5to50", "10to20", "10to50", "20to50", "50to100"
        ]
    },

}
