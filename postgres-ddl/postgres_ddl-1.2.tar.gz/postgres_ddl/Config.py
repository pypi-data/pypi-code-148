#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config():
    Indent = " " * 2
    NL = chr(10)
    IsSeqGrantsInTable = False

    @staticmethod
    def Parse(json):
        Config.Indent = " " * (json.get("indent") or 2)
        Config.NL = json.get("new_line") or chr(10)

        style = json.get("style") or []
        Config.IsSeqGrantsInTable = "seq_grants_in_table" in style
