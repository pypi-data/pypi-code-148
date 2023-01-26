# Fundamental filters


filters = {
    "p/e": {
        "name": "fa_pe_",
        "values": [
            "low", "profitable", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "u35", "u40", "u45", "u50",
            "o5", "o10", "o15", "o20", "o25", "o30",
            "o35", "o40", "o45", "o50",
        ]
    },

    "price/cash": {
        "name": "fa_pc_",
        "values": [
            "low", "profitable", "high",
            "u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8", "u9", "u10",
            "o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10",
            "o20", "o30", "o40", "o50"
        ]
    },

    "eps growth next 5 years": {
        "name": "fa_estltgrowth_",
        "values": [
            "neg", "pos", "poslow", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "o20", "o25", "o30",
        ]
    },

    "return on equity": {
        "name": "fa_roe_",
        "values": [
            "pos", "neg", "verypos", "veryneg",
            "u-50", "u-45", "u-40", "u-35", "u-30", "u-25", "u-20", "u-15", "u-10", "u-5",
            "o50", "o45", "u-40", "o35", "o30", "o25", "o20", "o15", "o10", "o5",
        ]
    },

    "debt/equity": {
        "name": "fa_debteq_",
        "values": [
            "high", "low",
            "u1", "u0.9", "u0.8", "u0.7", "u0.6", "u0.5", "u0.4", "u0.3", "u0.2", "u0.1",
            "o1", "o0.9", "o0.8", "o0.7", "o0.6", "o0.5", "o0.4", "o0.3", "o0.2", "o0.1",
        ]
    },

    "insider ownership": {
        "name": "sh_insiderown_",
        "values": [
            "high", "low", "o10", "o20", "o30", "o40", "o50", "o60", "o70", "o80", "o90"
        ]
    },

    "forward p/e": {
        "name": "fa_fpe_",
        "values": [
            "low", "profitable", "high",
            "u5", "u10", "u15", "u20", "u25", "u30", "u35", "u40", "u45", "u50",
            "o5", "o10", "o15", "o20", "o25", "o30", "o35", "o40", "o45", "o50",
        ]
    },

    "price/free cash flow": {
        "name": "fa_pfcf_",
        "values": [
            "low", "high",
            "u5", "u10", "u15", "u20", "u25", "u30", "u35", "u40",
            "u45", "u50", "u60", "u70", "u80", "u90", "u100",
            "o5", "o10", "o15", "o20", "o25", "o30", "o35", "o40",
            "o45", "o50", "o60", "o70", "o80", "o90", "o100",
        ]
    },

    "sales growth past 5 years": {
        "name": "fa_sales5years_",
        "values": [
            "neg", "pos", "poslow", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "o20", "o25", "o30",
        ]
    },

    "roi": {
        "name": "fa_roi_",
        "values": [
            "pos", "neg", "verypos", "veryneg",
            "u-50", "u-45", "u-40", "u-35", "u-30", "u-25", "u-20", "u-15", "u-10", "u-5",
            "o50", "o45", "u-40", "o35", "o30", "o25", "o20", "o15", "o10", "o5",
        ]
    },

    "gross margin": {
        "name": "fa_grossmargin_",
        "values": [
            "pos", "neg", "high",
            "u90", "u80", "u70", "u60", "u50", "u45", "u40", "u35", "u30", "u25", "u20", "u15", "u10", "u5", "u0",
            "u-10", "u-20", "u-30", "u-50", "u-70", "u-100",
            "o50", "o45", "u-40", "o35", "o30", "o25", "o20", "o15", "o10", "o5",
            "o90", "o80", "o70", "o60", "o50", "o45", "o40", "o35", "o30", "o25", "o20", "o15", "o10", "o5", "o0",
        ]
    },

    "insider transactions": {
        "name": "sh_insidertrans_",
        "values": [
            "veryneg", "neg", "pos", "verypos",
            "u-90", "u-80", "u-70", "u-60", "u-50", "u-45", "u-40", "u-35", "u-30", "u-25", "u-20", "u-15", "u-10", "u-5",
            "o-90", "o-80", "o-70", "o-60", "o-50", "o-45", "o-40", "o-35", "o-30", "o-25", "o-20", "o-15", "o-10", "o-5",
        ]
    },

    "peg": {
        "name": "fa_peg_",
        "values": [
            "low", "high", "u1", "u2", "u3",
            "o1", "o2", "o3"
        ]
    },

    "eps growth this year": {
        "name": "fa_epsyoy_",
        "values": [
            "neg", "pos", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "o20", "o25", "o30"
        ]
    },

    "eps growth qtr over qtr": {
        "name": "fa_epsqoq_",
        "values": [
            "neg", "pos", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "o20", "o25", "o30"
        ]
    },

    "current ratio": {
        "name": "fa_curratio_",
        "values": [
            "high", "low", "u1", "u0.5",
            "o0.5", "o1", "o1.5", "o2", "o3",
            "o4", "o5", "o10"
        ]
    },

    "operating margin": {
        "name": "fa_opermargin_",
        "values": [
            "pos", "neg", "high",
            "u90", "u80", "u70", "u60", "u50", "u45", "u40", "u35", "u30", "u25", "u20", "u15", "u10", "u5", "u0",
            "u-10", "u-20", "u-30", "u-50", "u-70", "u-100",
            "o50", "o45", "u-40", "o35", "o30", "o25", "o20", "o15", "o10", "o5",
            "o90", "o80", "o70", "o60", "o50", "o45", "o40", "o35", "o30", "o25", "o20", "o15", "o10", "o5", "o0",
        ]
    },

    "institutional ownership": {
        "name": "sh_instown_",
        "values": [
            "high", "low",
            "u90", "u80", "u70", "u60", "u50", "u40", "u30", "u20", "u10",
            "o90", "o80", "o70", "o60", "o50", "o40", "o30", "o20", "o10",
        ]
    },

    "p/s": {
        "name": "fa_ps_",
        "values": [
            "high", "low",
            "u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8", "u9", "u10",
            "o1", "o2", "o3", "o4", "o5", "o6", "o7", "o8", "o9", "o10",
        ]
    },

    "eps growth next year": {
        "name": "fa_epsyoy1_",
        "values": [
            "neg", "pos", "poslow", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "o20", "o25", "o30",
        ]
    },

    "sales growth qtr over qtr": {
        "name": "fa_salesqoq_",
        "values": [
            "neg", "pos", "poslow", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "o20", "o25", "o30",
        ]
    },

    "quick ratio": {
        "name": "fa_quickratio_",
        "values": [
            "high", "low", "u1", "u0.5",
            "o0.5", "o1", "o1.5", "o2", "o2.5", "o3", "o4", "o5", "o10"
        ]
    },

    "net profit margin": {
        "name": "fa_netmargin_",
        "values": [
            "pos", "neg", "veryneg", "high",
            "u90", "u80", "u70", "u60", "u50", "u45",
            "u40", "u35", "u30", "u25", "u20", "u15", "u10", "u5", "u0",
            "u-10", "u-20", "u-30", "u-50", "u-70", "u-100",
            "o90", "o80", "o70", "o60", "o50", "o45",
            "o40", "o35", "o30", "o25", "o20", "o15", "o10", "o5", "o0",
        ]
    },

    "institutional ownership": {
        "name": "sh_insttrans_",
        "values": [
            "veryneg", "neg", "pos", "verypos",
            "u-50", "u-45", "u-40", "u-35", "u-30", "u-25", "u-20", "u-15", "u-10", "u-5",
            "o50", "o45", "o40", "o35", "o30", "o25", "o20", "o15", "o10", "o5",
        ]
    },

    "p/b": {
        "name": "pb",
        "values": [
            "low", "high",
            "u1", "u2", "u3", "u4", "u5",
            "u6", "u7", "u8", "u9", "u10",
            "o1", "o2", "o3", "o4", "o5",
            "o6", "o7", "o8", "o9", "o10",
        ]
    },

    "eps growth past 5 years": {
        "name": "fa_eps5years_",
        "values": [
            "neg", "pos", "poslow", "high",
            "u5", "u10", "u15", "u20", "u25", "u30",
            "o5", "o10", "o15", "o20", "o25", "o30",
        ]
    },

    "return on assets": {
        "name": "fa_roa_",
        "values": [
            "pos", "neg", "verypos", "veryneg",
            "u-50", "u-45", "u-40", "u-35", "u-30", "u-25", "u-20",
            "u-15", "u-10", "u-5",
            "o50", "o45", "o40", "o35", "o30", "o25", "o20",
            "o15", "o10", "o5",
        ]
    },

    "lt debt/equity": {
        "name": "",
        "values": [
            "high", "low",
            "u1", "u0.9", "u0.8", "u0.7", "u0.6",
            "u0.5", "u0.4", "u0.3", "u0.2", "u0.1",
            "o1", "o0.9", "o0.8", "o0.7", "o0.6",
            "o0.5", "o0.4", "o0.3", "o0.2", "o0.1"
        ]
    },

    "payout ratio": {
        "name": "fa_payout_ratio_",
        "values": [
            "none", "pos", "low", "high",
            "o10", "o20", "o30", "o40", "o50", 
            "o60", "o70", "o80", "o90", "o100",
            "u10", "u20", "u30", "u40", "u50", 
            "u60", "u70", "u80", "u90", "u100"
        ]
    }
}
