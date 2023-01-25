# coding: UTF-8
import sys
bstack11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1_opy_ (bstack1l1l_opy_):
    global bstack1ll1_opy_
    stringNr = ord (bstack1l1l_opy_ [-1])
    bstackl_opy_ = bstack1l1l_opy_ [:-1]
    bstack1ll_opy_ = stringNr % len (bstackl_opy_)
    bstack1l_opy_ = bstackl_opy_ [:bstack1ll_opy_] + bstackl_opy_ [bstack1ll_opy_:]
    if bstack11_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack111_opy_ + stringNr) % bstack11l_opy_) for bstack111_opy_, char in enumerate (bstack1l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack111_opy_ + stringNr) % bstack11l_opy_) for bstack111_opy_, char in enumerate (bstack1l_opy_)])
    return eval (bstack1_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
bstack1ll1l_opy_ = {
	bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫৌ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸ্ࠧ"),
  bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧৎ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨ৏"),
  bstack1l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ৐"): bstack1l1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ৑"),
  bstack1l1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ৒"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩ৓"),
  bstack1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ৔"): bstack1l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࠬ৕"),
  bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ৖"): bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬৗ"),
  bstack1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ৘"): bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭৙"),
  bstack1l1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ৚"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧࠨ৛"),
  bstack1l1_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩড়"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡴࡱ࡯ࡩࠬঢ়"),
  bstack1l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ৞"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫয়"),
  bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬৠ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬৡ"),
  bstack1l1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩৢ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡺ࡮ࡪࡥࡰࠩৣ"),
  bstack1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ৤"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ৥"),
  bstack1l1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧ০"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧ১"),
  bstack1l1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ২"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ৩"),
  bstack1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭৪"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭৫"),
  bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৬"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ৭"),
  bstack1l1_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ৮"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ৯"),
  bstack1l1_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨৰ"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨৱ"),
  bstack1l1_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ৲"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ৳"),
  bstack1l1_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ৴"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ৵"),
  bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫ৶"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵࡗࡢ࡫ࡷࠫ৷"),
  bstack1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪ৸"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡵࠪ৹"),
  bstack1l1_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧ৺"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡧࡥࡤࡧ࡭࡫ࠧ৻"),
  bstack1l1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩৼ"): bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩ৽"),
  bstack1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭৾"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭৿"),
  bstack1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩ਀"): bstack1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ਁ"),
  bstack1l1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫਂ"): bstack1l1_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ਃ"),
  bstack1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ਄"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪਅ"),
  bstack1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫਆ"): bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫਇ"),
  bstack1l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧਈ"): bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧਉ"),
  bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧਊ"): bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪ਋"),
  bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ਌"): bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ਍"),
  bstack1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ਎"): bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬਏ"),
  bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩਐ"): bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ਑"),
  bstack1l1_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫ਒"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫਓ"),
}
bstack1111_opy_ = [
  bstack1l1_opy_ (u"ࠫࡴࡹࠧਔ"),
  bstack1l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨਕ"),
  bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨਖ"),
  bstack1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬਗ"),
  bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬਘ"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡦࡲࡍࡰࡤ࡬ࡰࡪ࠭ਙ"),
  bstack1l1_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯࡙ࡩࡷࡹࡩࡰࡰࠪਚ"),
]
bstack11ll1_opy_ = {
  bstack1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧਛ"): bstack1l1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩਜ"),
  bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨਝ"): [bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩਞ"), bstack1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫਟ")],
  bstack1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਠ"): bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨਡ"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨਢ"): bstack1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬਣ"),
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫਤ"): [bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨਥ"), bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧਦ")],
  bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪਧ"): bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬਨ"),
  bstack1l1_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨ਩"): bstack1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪਪ"),
  bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ਫ"): [bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧਬ"), bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩਭ")],
  bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨਮ"): [bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫਯ"), bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫਰ")]
}
bstack1ll11_opy_ = [
  bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫ਱"),
  bstack1l1_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩਲ"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ਲ਼"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨ਴"),
  bstack1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫਵ"),
  bstack1l1_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨਸ਼"),
  bstack1l1_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧ਷"),
  bstack1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪਸ"),
  bstack1l1_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫਹ"),
  bstack1l1_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ਺"),
  bstack1l1_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ਻"),
  bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵ਼ࠪ"),
]
bstack1l1l1_opy_ = [
  bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ਽"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨਾ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫਿ"),
  bstack1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ੀ"),
  bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪੁ"),
  bstack1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪੂ"),
  bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬ੃"),
  bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ੄"),
  bstack1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ੅"),
]
bstack11l1l_opy_ = [
  bstack1l1_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪ੆"),
  bstack1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨੇ"),
  bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪੈ"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੉"),
  bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࡐࡳ࡫ࡲࡶ࡮ࡺࡹࠨ੊"),
  bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ੋ"),
  bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡥ࡬࠭ੌ"),
  bstack1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧ੍ࠪ"),
  bstack1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ੎"),
  bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ੏"),
  bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ੐"),
  bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨੑ"),
  bstack1l1_opy_ (u"ࠪࡳࡸ࠭੒"),
  bstack1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ੓"),
  bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫ੔"),
  bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨ੕"),
  bstack1l1_opy_ (u"ࠧࡳࡧࡪ࡭ࡴࡴࠧ੖"),
  bstack1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪ੗"),
  bstack1l1_opy_ (u"ࠩࡰࡥࡨ࡮ࡩ࡯ࡧࠪ੘"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧਖ਼"),
  bstack1l1_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩਗ਼"),
  bstack1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩਜ਼"),
  bstack1l1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬੜ"),
  bstack1l1_opy_ (u"ࠧ࡯ࡱࡓࡥ࡬࡫ࡌࡰࡣࡧࡘ࡮ࡳࡥࡰࡷࡷࠫ੝"),
  bstack1l1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩਫ਼"),
  bstack1l1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ੟"),
  bstack1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ੠"),
  bstack1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡪࡴࡤࡌࡧࡼࡷࠬ੡"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩ੢"),
  bstack1l1_opy_ (u"࠭࡮ࡰࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠪ੣"),
  bstack1l1_opy_ (u"ࠧࡤࡪࡨࡧࡰ࡛ࡒࡍࠩ੤"),
  bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ੥"),
  bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡅࡲࡳࡰ࡯ࡥࡴࠩ੦"),
  bstack1l1_opy_ (u"ࠪࡧࡦࡶࡴࡶࡴࡨࡇࡷࡧࡳࡩࠩ੧"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ੨"),
  bstack1l1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ੩"),
  bstack1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࡙ࡩࡷࡹࡩࡰࡰࠪ੪"),
  bstack1l1_opy_ (u"ࠧ࡯ࡱࡅࡰࡦࡴ࡫ࡑࡱ࡯ࡰ࡮ࡴࡧࠨ੫"),
  bstack1l1_opy_ (u"ࠨ࡯ࡤࡷࡰ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧ੬"),
  bstack1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡎࡲ࡫ࡸ࠭੭"),
  bstack1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡌࡨࠬ੮"),
  bstack1l1_opy_ (u"ࠫࡩ࡫ࡤࡪࡥࡤࡸࡪࡪࡄࡦࡸ࡬ࡧࡪ࠭੯"),
  bstack1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡕࡧࡲࡢ࡯ࡶࠫੰ"),
  bstack1l1_opy_ (u"࠭ࡰࡩࡱࡱࡩࡓࡻ࡭ࡣࡧࡵࠫੱ"),
  bstack1l1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬੲ"),
  bstack1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡕࡰࡵ࡫ࡲࡲࡸ࠭ੳ"),
  bstack1l1_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧੴ"),
  bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪੵ"),
  bstack1l1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨ੶"),
  bstack1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡇ࡯࡯࡮ࡧࡷࡶ࡮ࡩࠧ੷"),
  bstack1l1_opy_ (u"࠭ࡶࡪࡦࡨࡳ࡛࠸ࠧ੸"),
  bstack1l1_opy_ (u"ࠧ࡮࡫ࡧࡗࡪࡹࡳࡪࡱࡱࡍࡳࡹࡴࡢ࡮࡯ࡅࡵࡶࡳࠨ੹"),
  bstack1l1_opy_ (u"ࠨࡧࡶࡴࡷ࡫ࡳࡴࡱࡖࡩࡷࡼࡥࡳࠩ੺"),
  bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨ੻"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡈࡪࡰࠨ੼"),
  bstack1l1_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫ੽"),
  bstack1l1_opy_ (u"ࠬࡹࡹ࡯ࡥࡗ࡭ࡲ࡫ࡗࡪࡶ࡫ࡒ࡙ࡖࠧ੾"),
  bstack1l1_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫ੿"),
  bstack1l1_opy_ (u"ࠧࡨࡲࡶࡐࡴࡩࡡࡵ࡫ࡲࡲࠬ઀"),
  bstack1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩઁ"),
  bstack1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩં"),
  bstack1l1_opy_ (u"ࠪࡪࡴࡸࡣࡦࡅ࡫ࡥࡳ࡭ࡥࡋࡣࡵࠫઃ"),
  bstack1l1_opy_ (u"ࠫࡽࡳࡳࡋࡣࡵࠫ઄"),
  bstack1l1_opy_ (u"ࠬࡾ࡭ࡹࡌࡤࡶࠬઅ"),
  bstack1l1_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬઆ"),
  bstack1l1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧઇ"),
  bstack1l1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩઈ"),
  bstack1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬઉ"),
  bstack1l1_opy_ (u"ࠪࡥࡵࡶࡖࡦࡴࡶ࡭ࡴࡴࠧઊ"),
  bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪઋ"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡴ࡫ࡪࡲࡆࡶࡰࠨઌ"),
  bstack1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࡵࠪઍ"),
  bstack1l1_opy_ (u"ࠧࡤࡣࡱࡥࡷࡿࠧ઎"),
  bstack1l1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩએ"),
  bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩઐ"),
  bstack1l1_opy_ (u"ࠪ࡭ࡪ࠭ઑ"),
  bstack1l1_opy_ (u"ࠫࡪࡪࡧࡦࠩ઒"),
  bstack1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬઓ"),
  bstack1l1_opy_ (u"࠭ࡱࡶࡧࡸࡩࠬઔ"),
  bstack1l1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡴࡡ࡭ࠩક"),
  bstack1l1_opy_ (u"ࠨࡣࡳࡴࡘࡺ࡯ࡳࡧࡆࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠩખ"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡅࡤࡱࡪࡸࡡࡊ࡯ࡤ࡫ࡪࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨગ"),
  bstack1l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡆࡺࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭ઘ"),
  bstack1l1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡋࡱࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧઙ"),
  bstack1l1_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࠩચ"),
  bstack1l1_opy_ (u"࠭ࡲࡦࡵࡨࡶࡻ࡫ࡄࡦࡸ࡬ࡧࡪ࠭છ"),
  bstack1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧજ"),
  bstack1l1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪઝ"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡤࡷࡸࡩ࡯ࡥࡧࠪઞ"),
  bstack1l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡹࡩ࡯࡯ࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪટ"),
  bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬઠ"),
  bstack1l1_opy_ (u"ࠬࡽࡤࡪࡱࡖࡩࡷࡼࡩࡤࡧࠪડ"),
  bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨઢ"),
  bstack1l1_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡄࡴࡲࡷࡸ࡙ࡩࡵࡧࡗࡶࡦࡩ࡫ࡪࡰࡪࠫણ"),
  bstack1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡑࡴࡨࡪࡪࡸࡥ࡯ࡥࡨࡷࠬત"),
  bstack1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡕ࡬ࡱࠬથ"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡳ࡯ࡷࡧࡌࡓࡘࡇࡰࡱࡕࡨࡸࡹ࡯࡮ࡨࡵࡏࡳࡨࡧ࡬ࡪࡼࡤࡸ࡮ࡵ࡮ࠨદ"),
  bstack1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ધ"),
  bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧન")
]
bstack11111_opy_ = {
  bstack1l1_opy_ (u"࠭ࡶࠨ઩"): bstack1l1_opy_ (u"ࠧࡷࠩપ"),
  bstack1l1_opy_ (u"ࠨࡨࠪફ"): bstack1l1_opy_ (u"ࠩࡩࠫબ"),
  bstack1l1_opy_ (u"ࠪࡪࡴࡸࡣࡦࠩભ"): bstack1l1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧࠪમ"),
  bstack1l1_opy_ (u"ࠬࡵ࡮࡭ࡻࡤࡹࡹࡵ࡭ࡢࡶࡨࠫય"): bstack1l1_opy_ (u"࠭࡯࡯࡮ࡼࡅࡺࡺ࡯࡮ࡣࡷࡩࠬર"),
  bstack1l1_opy_ (u"ࠧࡧࡱࡵࡧࡪࡲ࡯ࡤࡣ࡯ࠫ઱"): bstack1l1_opy_ (u"ࠨࡨࡲࡶࡨ࡫࡬ࡰࡥࡤࡰࠬલ"),
  bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡩࡱࡶࡸࠬળ"): bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭઴"),
  bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡳࡷࡺࠧવ"): bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨશ"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡺࡹࡥࡳࠩષ"): bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪસ"),
  bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫહ"): bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡣࡶࡷࠬ઺"),
  bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡨࡰࡵࡷࠫ઻"): bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡉࡱࡶࡸ઼ࠬ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡴࡷࡵࡸࡺࡲࡲࡶࡹ࠭ઽ"): bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧા"),
  bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨિ"): bstack1l1_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪી"),
  bstack1l1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫુ"): bstack1l1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡖࡵࡨࡶࠬૂ"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬૃ"): bstack1l1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡓࡥࡸࡹࠧૄ"),
  bstack1l1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨૅ"): bstack1l1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡕࡧࡳࡴࠩ૆"),
  bstack1l1_opy_ (u"ࠨࡤ࡬ࡲࡦࡸࡹࡱࡣࡷ࡬ࠬે"): bstack1l1_opy_ (u"ࠩࡥ࡭ࡳࡧࡲࡺࡲࡤࡸ࡭࠭ૈ"),
  bstack1l1_opy_ (u"ࠪࡴࡦࡩࡦࡪ࡮ࡨࠫૉ"): bstack1l1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧ૊"),
  bstack1l1_opy_ (u"ࠬࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧો"): bstack1l1_opy_ (u"࠭࠭ࡱࡣࡦ࠱࡫࡯࡬ࡦࠩૌ"),
  bstack1l1_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧ્ࠪ"): bstack1l1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫ૎"),
  bstack1l1_opy_ (u"ࠩ࡯ࡳ࡬࡬ࡩ࡭ࡧࠪ૏"): bstack1l1_opy_ (u"ࠪࡰࡴ࡭ࡦࡪ࡮ࡨࠫૐ"),
  bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭૑"): bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ૒"),
}
bstack111l1_opy_ = bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡸࡦ࠲࡬ࡺࡨࠧ૓")
bstack11l11_opy_ = bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠪ૔")
bstack11lll_opy_ = {
  bstack1l1_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪ૕"): 50,
  bstack1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ૖"): 40,
  bstack1l1_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫ૗"): 30,
  bstack1l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩ૘"): 20,
  bstack1l1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫ૙"): 10
}
DEFAULT_LOG_LEVEL = bstack11lll_opy_[bstack1l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ૚")]
bstack1l111_opy_ = bstack1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭૛")
bstack1l11l_opy_ = bstack1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭૜")
bstack1lll1l_opy_ = bstack1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨ૝")
bstack1l1ll_opy_ = bstack1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩ૞")
bstack1llll_opy_ = [bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬ૟"), bstack1l1_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬૠ")]
bstack1lll11_opy_ = [bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩૡ"), bstack1l1_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩૢ")]
bstack111l_opy_ = [
  bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡓࡧ࡭ࡦࠩૣ"),
  bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫ૤"),
  bstack1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ૥"),
  bstack1l1_opy_ (u"ࠫࡳ࡫ࡷࡄࡱࡰࡱࡦࡴࡤࡕ࡫ࡰࡩࡴࡻࡴࠨ૦"),
  bstack1l1_opy_ (u"ࠬࡧࡰࡱࠩ૧"),
  bstack1l1_opy_ (u"࠭ࡵࡥ࡫ࡧࠫ૨"),
  bstack1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ૩"),
  bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡥࠨ૪"),
  bstack1l1_opy_ (u"ࠩࡲࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧ૫"),
  bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡘࡧࡥࡺ࡮࡫ࡷࠨ૬"),
  bstack1l1_opy_ (u"ࠫࡳࡵࡒࡦࡵࡨࡸࠬ૭"), bstack1l1_opy_ (u"ࠬ࡬ࡵ࡭࡮ࡕࡩࡸ࡫ࡴࠨ૮"),
  bstack1l1_opy_ (u"࠭ࡣ࡭ࡧࡤࡶࡘࡿࡳࡵࡧࡰࡊ࡮ࡲࡥࡴࠩ૯"),
  bstack1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹ࡚ࡩ࡮࡫ࡱ࡫ࡸ࠭૰"),
  bstack1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡧࡵࡪࡴࡸ࡭ࡢࡰࡦࡩࡑࡵࡧࡨ࡫ࡱ࡫ࠬ૱"),
  bstack1l1_opy_ (u"ࠩࡲࡸ࡭࡫ࡲࡂࡲࡳࡷࠬ૲"),
  bstack1l1_opy_ (u"ࠪࡴࡷ࡯࡮ࡵࡒࡤ࡫ࡪ࡙࡯ࡶࡴࡦࡩࡔࡴࡆࡪࡰࡧࡊࡦ࡯࡬ࡶࡴࡨࠫ૳"),
  bstack1l1_opy_ (u"ࠫࡦࡶࡰࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩ૴"), bstack1l1_opy_ (u"ࠬࡧࡰࡱࡒࡤࡧࡰࡧࡧࡦࠩ૵"), bstack1l1_opy_ (u"࠭ࡡࡱࡲ࡚ࡥ࡮ࡺࡁࡤࡶ࡬ࡺ࡮ࡺࡹࠨ૶"), bstack1l1_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡑࡣࡦ࡯ࡦ࡭ࡥࠨ૷"), bstack1l1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡆࡸࡶࡦࡺࡩࡰࡰࠪ૸"),
  bstack1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡔࡨࡥࡩࡿࡔࡪ࡯ࡨࡳࡺࡺࠧૹ"),
  bstack1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡖࡨࡷࡹࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠧૺ"),
  bstack1l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡈࡵࡶࡦࡴࡤ࡫ࡪ࠭ૻ"), bstack1l1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࡅ࡯ࡦࡌࡲࡹ࡫࡮ࡵࠩૼ"),
  bstack1l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡄࡦࡸ࡬ࡧࡪࡘࡥࡢࡦࡼࡘ࡮ࡳࡥࡰࡷࡷࠫ૽"),
  bstack1l1_opy_ (u"ࠧࡢࡦࡥࡔࡴࡸࡴࠨ૾"),
  bstack1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡔࡱࡦ࡯ࡪࡺࠧ૿"),
  bstack1l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡌࡲࡸࡺࡡ࡭࡮ࡗ࡭ࡲ࡫࡯ࡶࡶࠪ଀"),
  bstack1l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡔࡦࡺࡨࠨଁ"),
  bstack1l1_opy_ (u"ࠫࡦࡼࡤࠨଂ"), bstack1l1_opy_ (u"ࠬࡧࡶࡥࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨଃ"), bstack1l1_opy_ (u"࠭ࡡࡷࡦࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨ଄"), bstack1l1_opy_ (u"ࠧࡢࡸࡧࡅࡷ࡭ࡳࠨଅ"),
  bstack1l1_opy_ (u"ࠨࡷࡶࡩࡐ࡫ࡹࡴࡶࡲࡶࡪ࠭ଆ"), bstack1l1_opy_ (u"ࠩ࡮ࡩࡾࡹࡴࡰࡴࡨࡔࡦࡺࡨࠨଇ"), bstack1l1_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡳࡴࡹࡲࡶࡩ࠭ଈ"),
  bstack1l1_opy_ (u"ࠫࡰ࡫ࡹࡂ࡮࡬ࡥࡸ࠭ଉ"), bstack1l1_opy_ (u"ࠬࡱࡥࡺࡒࡤࡷࡸࡽ࡯ࡳࡦࠪଊ"),
  bstack1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨଋ"), bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡇࡲࡨࡵࠪଌ"), bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࡇ࡭ࡷ࠭଍"), bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡄࡪࡵࡳࡲ࡫ࡍࡢࡲࡳ࡭ࡳ࡭ࡆࡪ࡮ࡨࠫ଎"), bstack1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡗࡶࡩࡘࡿࡳࡵࡧࡰࡉࡽ࡫ࡣࡶࡶࡤࡦࡱ࡫ࠧଏ"),
  bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡓࡳࡷࡺࠧଐ"), bstack1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࡴࠩ଑"),
  bstack1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡉ࡯ࡳࡢࡤ࡯ࡩࡇࡻࡩ࡭ࡦࡆ࡬ࡪࡩ࡫ࠨ଒"),
  bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳ࡜࡫ࡢࡷ࡫ࡨࡻ࡙࡯࡭ࡦࡱࡸࡸࠬଓ"),
  bstack1l1_opy_ (u"ࠨ࡫ࡱࡸࡪࡴࡴࡂࡥࡷ࡭ࡴࡴࠧଔ"), bstack1l1_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡅࡤࡸࡪ࡭࡯ࡳࡻࠪକ"), bstack1l1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡉࡰࡦ࡭ࡳࠨଖ"), bstack1l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡥࡱࡏ࡮ࡵࡧࡱࡸࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧଗ"),
  bstack1l1_opy_ (u"ࠬࡪ࡯࡯ࡶࡖࡸࡴࡶࡁࡱࡲࡒࡲࡗ࡫ࡳࡦࡶࠪଘ"),
  bstack1l1_opy_ (u"࠭ࡵ࡯࡫ࡦࡳࡩ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨଙ"), bstack1l1_opy_ (u"ࠧࡳࡧࡶࡩࡹࡑࡥࡺࡤࡲࡥࡷࡪࠧଚ"),
  bstack1l1_opy_ (u"ࠨࡰࡲࡗ࡮࡭࡮ࠨଛ"),
  bstack1l1_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࡗࡱ࡭ࡲࡶ࡯ࡳࡶࡤࡲࡹ࡜ࡩࡦࡹࡶࠫଜ"),
  bstack1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡳࡪࡲࡰ࡫ࡧ࡛ࡦࡺࡣࡩࡧࡵࡷࠬଝ"),
  bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫଞ"),
  bstack1l1_opy_ (u"ࠬࡸࡥࡤࡴࡨࡥࡹ࡫ࡃࡩࡴࡲࡱࡪࡊࡲࡪࡸࡨࡶࡘ࡫ࡳࡴ࡫ࡲࡲࡸ࠭ଟ"),
  bstack1l1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬଠ"),
  bstack1l1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡔࡥࡵࡩࡪࡴࡳࡩࡱࡷࡔࡦࡺࡨࠨଡ"),
  bstack1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡕࡳࡩࡪࡪࠧଢ"),
  bstack1l1_opy_ (u"ࠩࡪࡴࡸࡋ࡮ࡢࡤ࡯ࡩࡩ࠭ଣ"),
  bstack1l1_opy_ (u"ࠪ࡭ࡸࡎࡥࡢࡦ࡯ࡩࡸࡹࠧତ"),
  bstack1l1_opy_ (u"ࠫࡦࡪࡢࡆࡺࡨࡧ࡙࡯࡭ࡦࡱࡸࡸࠬଥ"),
  bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡩࡘࡩࡲࡪࡲࡷࠫଦ"),
  bstack1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡈࡪࡼࡩࡤࡧࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡦࡺࡩࡰࡰࠪଧ"),
  bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳࡌࡸࡡ࡯ࡶࡓࡩࡷࡳࡩࡴࡵ࡬ࡳࡳࡹࠧନ"),
  bstack1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡐࡤࡸࡺࡸࡡ࡭ࡑࡵ࡭ࡪࡴࡴࡢࡶ࡬ࡳࡳ࠭଩"),
  bstack1l1_opy_ (u"ࠩࡶࡽࡸࡺࡥ࡮ࡒࡲࡶࡹ࠭ପ"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡨࡧࡎ࡯ࡴࡶࠪଫ"),
  bstack1l1_opy_ (u"ࠫࡸࡱࡩࡱࡗࡱࡰࡴࡩ࡫ࠨବ"), bstack1l1_opy_ (u"ࠬࡻ࡮࡭ࡱࡦ࡯࡙ࡿࡰࡦࠩଭ"), bstack1l1_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰࡑࡥࡺࠩମ"),
  bstack1l1_opy_ (u"ࠧࡢࡷࡷࡳࡑࡧࡵ࡯ࡥ࡫ࠫଯ"),
  bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡒ࡯ࡨࡥࡤࡸࡈࡧࡰࡵࡷࡵࡩࠬର"),
  bstack1l1_opy_ (u"ࠩࡸࡲ࡮ࡴࡳࡵࡣ࡯ࡰࡔࡺࡨࡦࡴࡓࡥࡨࡱࡡࡨࡧࡶࠫ଱"),
  bstack1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨ࡛࡮ࡴࡤࡰࡹࡄࡲ࡮ࡳࡡࡵ࡫ࡲࡲࠬଲ"),
  bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡳࡴࡲࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨଳ"),
  bstack1l1_opy_ (u"ࠬ࡫࡮ࡧࡱࡵࡧࡪࡇࡰࡱࡋࡱࡷࡹࡧ࡬࡭ࠩ଴"),
  bstack1l1_opy_ (u"࠭ࡥ࡯ࡵࡸࡶࡪ࡝ࡥࡣࡸ࡬ࡩࡼࡹࡈࡢࡸࡨࡔࡦ࡭ࡥࡴࠩଵ"), bstack1l1_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࡅࡧࡹࡸࡴࡵ࡬ࡴࡒࡲࡶࡹ࠭ଶ"), bstack1l1_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡘࡧࡥࡺ࡮࡫ࡷࡅࡧࡷࡥ࡮ࡲࡳࡄࡱ࡯ࡰࡪࡩࡴࡪࡱࡱࠫଷ"),
  bstack1l1_opy_ (u"ࠩࡵࡩࡲࡵࡴࡦࡃࡳࡴࡸࡉࡡࡤࡪࡨࡐ࡮ࡳࡩࡵࠩସ"),
  bstack1l1_opy_ (u"ࠪࡧࡦࡲࡥ࡯ࡦࡤࡶࡋࡵࡲ࡮ࡣࡷࠫହ"),
  bstack1l1_opy_ (u"ࠫࡧࡻ࡮ࡥ࡮ࡨࡍࡩ࠭଺"),
  bstack1l1_opy_ (u"ࠬࡲࡡࡶࡰࡦ࡬࡙࡯࡭ࡦࡱࡸࡸࠬ଻"),
  bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࡔࡧࡵࡺ࡮ࡩࡥࡴࡇࡱࡥࡧࡲࡥࡥ଼ࠩ"), bstack1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡩࡩ࠭ଽ"),
  bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴࡇࡣࡤࡧࡳࡸࡆࡲࡥࡳࡶࡶࠫା"), bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵࡄࡪࡵࡰ࡭ࡸࡹࡁ࡭ࡧࡵࡸࡸ࠭ି"),
  bstack1l1_opy_ (u"ࠪࡲࡦࡺࡩࡷࡧࡌࡲࡸࡺࡲࡶ࡯ࡨࡲࡹࡹࡌࡪࡤࠪୀ"),
  bstack1l1_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨ࡛ࡪࡨࡔࡢࡲࠪୁ"),
  bstack1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡎࡴࡩࡵ࡫ࡤࡰ࡚ࡸ࡬ࠨୂ"), bstack1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡇ࡬࡭ࡱࡺࡔࡴࡶࡵࡱࡵࠪୃ"), bstack1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉࡨࡰࡲࡶࡪࡌࡲࡢࡷࡧ࡛ࡦࡸ࡮ࡪࡰࡪࠫୄ"), bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡨࡲࡑ࡯࡮࡬ࡵࡌࡲࡇࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠨ୅"),
  bstack1l1_opy_ (u"ࠩ࡮ࡩࡪࡶࡋࡦࡻࡆ࡬ࡦ࡯࡮ࡴࠩ୆"),
  bstack1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭࡫ࡽࡥࡧࡲࡥࡔࡶࡵ࡭ࡳ࡭ࡳࡅ࡫ࡵࠫେ"),
  bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡤࡧࡶࡷࡆࡸࡧࡶ࡯ࡨࡲࡹࡹࠧୈ"),
  bstack1l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡵࡏࡪࡿࡄࡦ࡮ࡤࡽࠬ୉"),
  bstack1l1_opy_ (u"࠭ࡳࡩࡱࡺࡍࡔ࡙ࡌࡰࡩࠪ୊"),
  bstack1l1_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡔࡶࡵࡥࡹ࡫ࡧࡺࠩୋ"),
  bstack1l1_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡓࡧࡶࡴࡴࡴࡳࡦࡖ࡬ࡱࡪࡵࡵࡵࠩୌ"), bstack1l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࡝ࡡࡪࡶࡗ࡭ࡲ࡫࡯ࡶࡶ୍ࠪ"),
  bstack1l1_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡇࡩࡧࡻࡧࡑࡴࡲࡼࡾ࠭୎"),
  bstack1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡸࡿ࡮ࡤࡇࡻࡩࡨࡻࡴࡦࡈࡵࡳࡲࡎࡴࡵࡲࡶࠫ୏"),
  bstack1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡏࡳ࡬ࡉࡡࡱࡶࡸࡶࡪ࠭୐"),
  bstack1l1_opy_ (u"࠭ࡷࡦࡤ࡮࡭ࡹࡊࡥࡣࡷࡪࡔࡷࡵࡸࡺࡒࡲࡶࡹ࠭୑"),
  bstack1l1_opy_ (u"ࠧࡧࡷ࡯ࡰࡈࡵ࡮ࡵࡧࡻࡸࡑ࡯ࡳࡵࠩ୒"),
  bstack1l1_opy_ (u"ࠨࡹࡤ࡭ࡹࡌ࡯ࡳࡃࡳࡴࡘࡩࡲࡪࡲࡷࠫ୓"),
  bstack1l1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡆࡳࡳࡴࡥࡤࡶࡕࡩࡹࡸࡩࡦࡵࠪ୔"),
  bstack1l1_opy_ (u"ࠪࡥࡵࡶࡎࡢ࡯ࡨࠫ୕"),
  bstack1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡘࡒࡃࡦࡴࡷࠫୖ"),
  bstack1l1_opy_ (u"ࠬࡺࡡࡱ࡙࡬ࡸ࡭࡙ࡨࡰࡴࡷࡔࡷ࡫ࡳࡴࡆࡸࡶࡦࡺࡩࡰࡰࠪୗ"),
  bstack1l1_opy_ (u"࠭ࡳࡤࡣ࡯ࡩࡋࡧࡣࡵࡱࡵࠫ୘"),
  bstack1l1_opy_ (u"ࠧࡸࡦࡤࡐࡴࡩࡡ࡭ࡒࡲࡶࡹ࠭୙"),
  bstack1l1_opy_ (u"ࠨࡵ࡫ࡳࡼ࡞ࡣࡰࡦࡨࡐࡴ࡭ࠧ୚"),
  bstack1l1_opy_ (u"ࠩ࡬ࡳࡸࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡶࡵࡨࠫ୛"),
  bstack1l1_opy_ (u"ࠪࡼࡨࡵࡤࡦࡅࡲࡲ࡫࡯ࡧࡇ࡫࡯ࡩࠬଡ଼"),
  bstack1l1_opy_ (u"ࠫࡰ࡫ࡹࡤࡪࡤ࡭ࡳࡖࡡࡴࡵࡺࡳࡷࡪࠧଢ଼"),
  bstack1l1_opy_ (u"ࠬࡻࡳࡦࡒࡵࡩࡧࡻࡩ࡭ࡶ࡚ࡈࡆ࠭୞"),
  bstack1l1_opy_ (u"࠭ࡰࡳࡧࡹࡩࡳࡺࡗࡅࡃࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠧୟ"),
  bstack1l1_opy_ (u"ࠧࡸࡧࡥࡈࡷ࡯ࡶࡦࡴࡄ࡫ࡪࡴࡴࡖࡴ࡯ࠫୠ"),
  bstack1l1_opy_ (u"ࠨ࡭ࡨࡽࡨ࡮ࡡࡪࡰࡓࡥࡹ࡮ࠧୡ"),
  bstack1l1_opy_ (u"ࠩࡸࡷࡪࡔࡥࡸ࡙ࡇࡅࠬୢ"),
  bstack1l1_opy_ (u"ࠪࡻࡩࡧࡌࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ୣ"), bstack1l1_opy_ (u"ࠫࡼࡪࡡࡄࡱࡱࡲࡪࡩࡴࡪࡱࡱࡘ࡮ࡳࡥࡰࡷࡷࠫ୤"),
  bstack1l1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡓࡷ࡭ࡉࡥࠩ୥"), bstack1l1_opy_ (u"࠭ࡸࡤࡱࡧࡩࡘ࡯ࡧ࡯࡫ࡱ࡫ࡎࡪࠧ୦"),
  bstack1l1_opy_ (u"ࠧࡶࡲࡧࡥࡹ࡫ࡤࡘࡆࡄࡆࡺࡴࡤ࡭ࡧࡌࡨࠬ୧"),
  bstack1l1_opy_ (u"ࠨࡴࡨࡷࡪࡺࡏ࡯ࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡷࡺࡏ࡯࡮ࡼࠫ୨"),
  bstack1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࡶࠫ୩"),
  bstack1l1_opy_ (u"ࠪࡻࡩࡧࡓࡵࡣࡵࡸࡺࡶࡒࡦࡶࡵ࡭ࡪࡹࠧ୪"), bstack1l1_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶࡾࡏ࡮ࡵࡧࡵࡺࡦࡲࠧ୫"),
  bstack1l1_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹࡎࡡࡳࡦࡺࡥࡷ࡫ࡋࡦࡻࡥࡳࡦࡸࡤࠨ୬"),
  bstack1l1_opy_ (u"࠭࡭ࡢࡺࡗࡽࡵ࡯࡮ࡨࡈࡵࡩࡶࡻࡥ࡯ࡥࡼࠫ୭"),
  bstack1l1_opy_ (u"ࠧࡴ࡫ࡰࡴࡱ࡫ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࡅ࡫ࡩࡨࡱࠧ୮"),
  bstack1l1_opy_ (u"ࠨࡷࡶࡩࡈࡧࡲࡵࡪࡤ࡫ࡪ࡙ࡳ࡭ࠩ୯"),
  bstack1l1_opy_ (u"ࠩࡶ࡬ࡴࡻ࡬ࡥࡗࡶࡩࡘ࡯࡮ࡨ࡮ࡨࡸࡴࡴࡔࡦࡵࡷࡑࡦࡴࡡࡨࡧࡵࠫ୰"),
  bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡋ࡚ࡈࡕ࠭ୱ"),
  bstack1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡳࡺࡩࡨࡊࡦࡈࡲࡷࡵ࡬࡭ࠩ୲"),
  bstack1l1_opy_ (u"ࠬ࡯ࡧ࡯ࡱࡵࡩࡍ࡯ࡤࡥࡧࡱࡅࡵ࡯ࡐࡰ࡮࡬ࡧࡾࡋࡲࡳࡱࡵࠫ୳"),
  bstack1l1_opy_ (u"࠭࡭ࡰࡥ࡮ࡐࡴࡩࡡࡵ࡫ࡲࡲࡆࡶࡰࠨ୴"),
  bstack1l1_opy_ (u"ࠧ࡭ࡱࡪࡧࡦࡺࡆࡰࡴࡰࡥࡹ࠭୵"), bstack1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇ࡫࡯ࡸࡪࡸࡓࡱࡧࡦࡷࠬ୶"),
  bstack1l1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡅࡧ࡯ࡥࡾࡇࡤࡣࠩ୷")
]
bstack1111l_opy_ = bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡦࡶࡩ࠮ࡥ࡯ࡳࡺࡪ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡸࡴࡱࡵࡡࡥࠩ୸")
bstack1l11_opy_ = [bstack1l1_opy_ (u"ࠫ࠳ࡧࡰ࡬ࠩ୹"), bstack1l1_opy_ (u"ࠬ࠴ࡡࡢࡤࠪ୺"), bstack1l1_opy_ (u"࠭࠮ࡪࡲࡤࠫ୻")]
bstack1llll1_opy_ = [bstack1l1_opy_ (u"ࠧࡪࡦࠪ୼"), bstack1l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭୽"), bstack1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ୾"), bstack1l1_opy_ (u"ࠪࡷ࡭ࡧࡲࡦࡣࡥࡰࡪࡥࡩࡥࠩ୿")]
bstack1lllll_opy_ = {
  bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ஀"): bstack1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ஁"),
  bstack1l1_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧஂ"): bstack1l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬஃ"),
  bstack1l1_opy_ (u"ࠨࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭஄"): bstack1l1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪஅ"),
  bstack1l1_opy_ (u"ࠪ࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ஆ"): bstack1l1_opy_ (u"ࠫࡸ࡫࠺ࡪࡧࡒࡴࡹ࡯࡯࡯ࡵࠪஇ"),
  bstack1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࡔࡶࡴࡪࡱࡱࡷࠬஈ"): bstack1l1_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧஉ")
}
bstack11l1_opy_ = [
  bstack1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬஊ"),
  bstack1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭஋"),
  bstack1l1_opy_ (u"ࠩࡰࡷ࠿࡫ࡤࡨࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ஌"),
  bstack1l1_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ஍"),
  bstack1l1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬஎ"),
]
bstack11ll_opy_ = bstack1l1l1_opy_ + bstack11l1l_opy_ + bstack111l_opy_
bstack1lll1_opy_ = [
  bstack1l1_opy_ (u"ࠬࡤ࡬ࡰࡥࡤࡰ࡭ࡵࡳࡵࠦࠪஏ"),
  bstack1l1_opy_ (u"࠭࡞ࡣࡵ࠰ࡰࡴࡩࡡ࡭࠰ࡦࡳࡲࠪࠧஐ"),
  bstack1l1_opy_ (u"ࠧ࡟࠳࠵࠻࠳࠭஑"),
  bstack1l1_opy_ (u"ࠨࡠ࠴࠴࠳࠭ஒ"),
  bstack1l1_opy_ (u"ࠩࡡ࠵࠼࠸࠮࠲࡝࠹࠱࠾ࡣ࠮ࠨஓ"),
  bstack1l1_opy_ (u"ࠪࡢ࠶࠽࠲࠯࠴࡞࠴࠲࠿࡝࠯ࠩஔ"),
  bstack1l1_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠶࡟࠵࠳࠱࡞࠰ࠪக"),
  bstack1l1_opy_ (u"ࠬࡤ࠱࠺࠴࠱࠵࠻࠾࠮ࠨ஖")
]
bstack1111ll1l_opy_ = bstack1l1_opy_ (u"࠭ࡓࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡲࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠲ࠠࡶࡵ࡬ࡲ࡬ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠼ࠣࡿࢂ࠭஗")
bstack11l1111l_opy_ = bstack1l1_opy_ (u"ࠧࡄࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡷࡪࡺࡵࡱࠣࠪ஘")
bstack111l1l_opy_ = bstack1l1_opy_ (u"ࠨࡒࡤࡶࡸ࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡࡨ࡬ࡰࡪࡀࠠࡼࡿࠪங")
bstack1ll1ll_opy_ = bstack1l1_opy_ (u"ࠩࡖࡥࡳ࡯ࡴࡪࡼࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧ࠽ࠤࢀࢃࠧச")
bstack11ll1l1l_opy_ = bstack1l1_opy_ (u"࡙ࠪࡸ࡯࡮ࡨࠢ࡫ࡹࡧࠦࡵࡳ࡮࠽ࠤࢀࢃࠧ஛")
bstack1ll1l111_opy_ = bstack1l1_opy_ (u"ࠫࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࡽࢀࠫஜ")
bstack111l111l_opy_ = bstack1l1_opy_ (u"ࠬࡘࡥࡤࡧ࡬ࡺࡪࡪࠠࡪࡰࡷࡩࡷࡸࡵࡱࡶ࠯ࠤࡪࡾࡩࡵ࡫ࡱ࡫ࠬ஝")
bstack1lllll1l_opy_ = bstack1l1_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡷࡳࠥࡸࡵ࡯ࠢࡷࡩࡸࡺࡳ࠯ࠢࡣࡴ࡮ࡶࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࡣࠫஞ")
bstack1l111ll_opy_ = bstack1l1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴࠡࡣࡱࡨࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࡤࠬட")
bstack1ll111l1_opy_ = bstack1l1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡵࡳࡧࡵࡴ࠭ࠢࡳࡥࡧࡵࡴࠡࡣࡱࡨࠥࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡬ࡪࡤࡵࡥࡷࡿࠠࡱࡣࡦ࡯ࡦ࡭ࡥࡴࠢࡷࡳࠥࡸࡵ࡯ࠢࡵࡳࡧࡵࡴࠡࡶࡨࡷࡹࡹࠠࡪࡰࠣࡴࡦࡸࡡ࡭࡮ࡨࡰ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡸ࡯ࡣࡱࡷࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡱࡣࡥࡳࡹࠦࡲࡰࡤࡲࡸ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠭ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࡮࡬ࡦࡷࡧࡲࡺࡢࠪ஠")
bstack111111l_opy_ = bstack1l1_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡦࡪ࡮ࡡࡷࡧࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴ࠰ࠣࡤࡵ࡯ࡰࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡥࡩ࡭ࡧࡶࡦࡢࠪ஡")
bstack111111_opy_ = bstack1l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡦࡶࡰࡪࡷࡰ࠱ࡨࡲࡩࡦࡰࡷࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠤࡥࡶࡩࡱࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡅࡵࡶࡩࡶ࡯࠰ࡔࡾࡺࡨࡰࡰ࠰ࡇࡱ࡯ࡥ࡯ࡶࡣࠫ஢")
bstack11lllll_opy_ = bstack1l1_opy_ (u"ࠫࡍࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤ࡮ࡲࡷࡪ࠭ண")
bstack1l1l1l_opy_ = bstack1l1_opy_ (u"ࠬࡇ࡬࡭ࠢࡧࡳࡳ࡫ࠡࠨத")
bstack111ll111_opy_ = bstack1l1_opy_ (u"࠭ࡃࡰࡰࡩ࡭࡬ࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸࠥࡧࡴࠡࠤࡾࢁࠧ࠴ࠠࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡦࡰࡺࡪࡥࠡࡣࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡱࡱࠦࡦࡪ࡮ࡨࠤࡨࡵ࡮ࡵࡣ࡬ࡲ࡮࡭ࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࡵ࠱ࠫ஥")
bstack111l1l11_opy_ = bstack1l1_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡳࡧࡧࡩࡳࡺࡩࡢ࡮ࡶࠤࡳࡵࡴࠡࡲࡵࡳࡻ࡯ࡤࡦࡦ࠱ࠤࡕࡲࡥࡢࡵࡨࠤࡦࡪࡤࠡࡶ࡫ࡩࡲࠦࡩ࡯ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡬ࡩ࡭ࡧࠣࡥࡸࠦࠢࡶࡵࡨࡶࡓࡧ࡭ࡦࠤࠣࡥࡳࡪࠠࠣࡣࡦࡧࡪࡹࡳࡌࡧࡼࠦࠥࡵࡲࠡࡵࡨࡸࠥࡺࡨࡦ࡯ࠣࡥࡸࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷࠤࡻࡧࡲࡪࡣࡥࡰࡪࡹ࠺ࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡔࡁࡎࡇࠥࠤࡦࡴࡤࠡࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠧ࠭஦")
bstack111ll1ll_opy_ = bstack1l1_opy_ (u"ࠨࡏࡤࡰ࡫ࡵࡲ࡮ࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠼ࠥࡿࢂࠨࠧ஧")
bstack1111ll_opy_ = bstack1l1_opy_ (u"ࠩࡈࡲࡨࡵࡵ࡯ࡶࡨࡶࡪࡪࠠࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡱࠢ࠰ࠤࢀࢃࠧந")
bstack1lll1111l_opy_ = bstack1l1_opy_ (u"ࠪࡗࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠪன")
bstack11lll1l_opy_ = bstack1l1_opy_ (u"ࠫࡘࡺ࡯ࡱࡲ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡒ࡯ࡤࡣ࡯ࠫப")
bstack11ll1l11_opy_ = bstack1l1_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡑࡵࡣࡢ࡮ࠣ࡭ࡸࠦ࡮ࡰࡹࠣࡶࡺࡴ࡮ࡪࡰࡪࠥࠬ஫")
bstack1111l1l1_opy_ = bstack1l1_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡶࡸࡦࡸࡴࠡࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡍࡱࡦࡥࡱࡀࠠࡼࡿࠪ஬")
bstack11lll1ll_opy_ = bstack1l1_opy_ (u"ࠧࡔࡶࡤࡶࡹ࡯࡮ࡨࠢ࡯ࡳࡨࡧ࡬ࠡࡤ࡬ࡲࡦࡸࡹࠡࡹ࡬ࡸ࡭ࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࡽࢀࠫ஭")
bstack11ll1111_opy_ = bstack1l1_opy_ (u"ࠨࡗࡳࡨࡦࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࠤࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡻࡾࠩம")
bstack1ll1l1lll_opy_ = bstack1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡰࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷࠥࢁࡽࠨய")
bstack1111l11_opy_ = bstack1l1_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡴࡷࡵࡶࡪࡦࡨࠤࡦࡴࠠࡢࡲࡳࡶࡴࡶࡲࡪࡣࡷࡩࠥࡌࡗࠡࠪࡵࡳࡧࡵࡴ࠰ࡲࡤࡦࡴࡺࠩࠡ࡫ࡱࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫࡯࡬ࡦ࠮ࠣࡷࡰ࡯ࡰࠡࡶ࡫ࡩࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡭ࡨࡽࠥ࡯࡮ࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡩ࡮ࡲ࡯ࡩࠥࡶࡹࡵࡪࡲࡲࠥࡹࡣࡳ࡫ࡳࡸࠥࡽࡩࡵࡪࡲࡹࡹࠦࡡ࡯ࡻࠣࡊ࡜࠴ࠧர")
bstack111ll11l_opy_ = bstack1l1_opy_ (u"ࠫࡘ࡫ࡴࡵ࡫ࡱ࡫ࠥ࡮ࡴࡵࡲࡓࡶࡴࡾࡹ࠰ࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࠡࡱࡱࠤࡨࡻࡲࡳࡧࡱࡸࡱࡿࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡺࡪࡸࡳࡪࡱࡱࠤࡴ࡬ࠠࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࠫࡿࢂ࠯ࠬࠡࡲ࡯ࡩࡦࡹࡥࠡࡷࡳ࡫ࡷࡧࡤࡦࠢࡷࡳ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳ࠾࠾࠶࠱࠴࠳࠶ࠠࡰࡴࠣࡶࡪ࡬ࡥࡳࠢࡷࡳࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠵ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠰ࡴࡸࡲ࠲ࡺࡥࡴࡶࡶ࠱ࡧ࡫ࡨࡪࡰࡧ࠱ࡵࡸ࡯ࡹࡻࠦࡴࡾࡺࡨࡰࡰࠣࡪࡴࡸࠠࡢࠢࡺࡳࡷࡱࡡࡳࡱࡸࡲࡩ࠴ࠧற")
bstack11ll1ll_opy_ = bstack1l1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡻࡰࡰࠥ࡬ࡩ࡭ࡧ࠱࠲ࠬல")
bstack1l1llll_opy_ = bstack1l1_opy_ (u"࠭ࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡶ࡫ࡩࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥ࡬ࡩ࡭ࡧࠤࠫள")
bstack1lll1lll_opy_ = bstack1l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣ࡫ࡪࡴࡥࡳࡣࡷࡩࠥࡺࡨࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨ࡬ࡰࡪ࠴ࠠࡼࡿࠪழ")
bstack1l1ll11l_opy_ = bstack1l1_opy_ (u"ࠨࡇࡻࡴࡪࡩࡴࡦࡦࠣࡥࡹࠦ࡬ࡦࡣࡶࡸࠥ࠷ࠠࡪࡰࡳࡹࡹ࠲ࠠࡳࡧࡦࡩ࡮ࡼࡥࡥࠢ࠳ࠫவ")
bstack1lllll111_opy_ = bstack1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡࡦࡸࡶ࡮ࡴࡧࠡࡃࡳࡴࠥࡻࡰ࡭ࡱࡤࡨ࠳ࠦࡻࡾࠩஶ")
bstack111l11_opy_ = bstack1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱ࡮ࡲࡥࡩࠦࡁࡱࡲ࠱ࠤࡎࡴࡶࡢ࡮࡬ࡨࠥ࡬ࡩ࡭ࡧࠣࡴࡦࡺࡨࠡࡲࡵࡳࡻ࡯ࡤࡦࡦࠣࡿࢂ࠴ࠧஷ")
bstack1l11l11l_opy_ = bstack1l1_opy_ (u"ࠫࡐ࡫ࡹࡴࠢࡦࡥࡳࡴ࡯ࡵࠢࡦࡳ࠲࡫ࡸࡪࡵࡷࠤࡦࡹࠠࡢࡲࡳࠤࡻࡧ࡬ࡶࡧࡶ࠰ࠥࡻࡳࡦࠢࡤࡲࡾࠦ࡯࡯ࡧࠣࡴࡷࡵࡰࡦࡴࡷࡽࠥ࡬ࡲࡰ࡯ࠣࡿ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡳࡥࡹ࡮࠼ࡴࡶࡵ࡭ࡳ࡭࠾࠭ࠢࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࡁࡹࡴࡳ࡫ࡱ࡫ࡃ࠲ࠠࡴࡪࡤࡶࡪࡧࡢ࡭ࡧࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࡽ࠭ࠢࡲࡲࡱࡿࠠࠣࡲࡤࡸ࡭ࠨࠠࡢࡰࡧࠤࠧࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠣࠢࡦࡥࡳࠦࡣࡰ࠯ࡨࡼ࡮ࡹࡴࠡࡶࡲ࡫ࡪࡺࡨࡦࡴ࠱ࠫஸ")
bstack1111l1l_opy_ = bstack1l1_opy_ (u"ࠬࡡࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡢࡲࡳࠤࡵࡸ࡯ࡱࡧࡵࡸࡾࡣࠠࡴࡷࡳࡴࡴࡸࡴࡦࡦࠣࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠠࡢࡴࡨࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧஹ")
bstack11l111l_opy_ = bstack1l1_opy_ (u"࡛࠭ࡊࡰࡹࡥࡱ࡯ࡤࠡࡣࡳࡴࠥࡶࡲࡰࡲࡨࡶࡹࡿ࡝ࠡࡕࡸࡴࡵࡵࡲࡵࡧࡧࠤࡻࡧ࡬ࡶࡧࡶࠤࡴ࡬ࠠࡢࡲࡳࠤࡦࡸࡥࠡࡱࡩࠤࢀ࡯ࡤ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡴࡦࡺࡨ࠽ࡵࡷࡶ࡮ࡴࡧ࠿࠮ࠣࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩࡂࡳࡵࡴ࡬ࡲ࡬ࡄࠬࠡࡵ࡫ࡥࡷ࡫ࡡࡣ࡮ࡨࡣ࡮ࡪ࠼ࡴࡶࡵ࡭ࡳ࡭࠾ࡾ࠰ࠣࡊࡴࡸࠠ࡮ࡱࡵࡩࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡰ࡭ࡧࡤࡷࡪࠦࡶࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡤࡰࡥࡶ࠳ࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵࡶࡩࡶ࡯࠲ࡷࡪࡺ࠭ࡶࡲ࠰ࡸࡪࡹࡴࡴ࠱ࡶࡴࡪࡩࡩࡧࡻ࠰ࡥࡵࡶࠧ஺")
bstack1ll1l11ll_opy_ = bstack1l1_opy_ (u"ࠧࡖࡵ࡬ࡲ࡬ࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡࡣࡳࡴࠥ࡯ࡤࠡࡽࢀࠤ࡫ࡵࡲࠡࡪࡤࡷ࡭ࠦ࠺ࠡࡽࢀ࠲ࠬ஻")
bstack1l111l1l_opy_ = bstack1l1_opy_ (u"ࠨࡃࡳࡴ࡛ࠥࡰ࡭ࡱࡤࡨࡪࡪࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠠࡊࡆࠣ࠾ࠥࢁࡽࠨ஼")
bstack111ll1_opy_ = bstack1l1_opy_ (u"ࠩࡘࡷ࡮ࡴࡧࠡࡃࡳࡴࠥࡀࠠࡼࡿ࠱ࠫ஽")
bstack1lllll11_opy_ = bstack1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡷࡺࡶࡰࡰࡴࡷࡩࡩࠦࡦࡰࡴࠣࡺࡦࡴࡩ࡭࡮ࡤࠤࡵࡿࡴࡩࡱࡱࠤࡹ࡫ࡳࡵࡵ࠯ࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡽࡩࡵࡪࠣࡴࡦࡸࡡ࡭࡮ࡨࡰࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡀࠤ࠶࠭ா")
bstack11111lll_opy_ = bstack1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࠽ࠤࢀࢃࠧி")
bstack1l1llll1_opy_ = bstack1l1_opy_ (u"ࠬࡉ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡥ࡯ࡳࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࡾࢁࠬீ")
bstack111llll_opy_ = bstack1l1_opy_ (u"࠭ࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡪࡩࡹࠦࡲࡦࡣࡶࡳࡳࠦࡦࡰࡴࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡪࡧࡴࡶࡴࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩ࠳ࠦࡻࡾࠩு")
bstack1ll1l1l1l_opy_ = bstack1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡳࡳࡳࡹࡥࠡࡨࡵࡳࡲࠦࡡࡱ࡫ࠣࡧࡦࡲ࡬࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࡾࢁࠬூ")
bstack111ll11_opy_ = bstack1l1_opy_ (u"ࠨࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸ࡮࡯ࡸࠢࡥࡹ࡮ࡲࡤࠡࡗࡕࡐ࠱ࠦࡡࡴࠢࡥࡹ࡮ࡲࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷࡽࠥ࡯ࡳࠡࡰࡲࡸࠥࡻࡳࡦࡦ࠱ࠫ௃")
bstack11111l1l_opy_ = bstack1l1_opy_ (u"ࠩࡖࡩࡷࡼࡥࡳࠢࡶ࡭ࡩ࡫ࠠࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠫࡿࢂ࠯ࠠࡪࡵࠣࡲࡴࡺࠠࡴࡣࡰࡩࠥࡧࡳࠡࡥ࡯࡭ࡪࡴࡴࠡࡵ࡬ࡨࡪࠦࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠪࡾࢁ࠮࠭௄")
bstack11l1ll_opy_ = bstack1l1_opy_ (u"࡚ࠪ࡮࡫ࡷࠡࡤࡸ࡭ࡱࡪࠠࡰࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡧࡥࡸ࡮ࡢࡰࡣࡵࡨ࠿ࠦࡻࡾࠩ௅")
bstack1l111l_opy_ = bstack1l1_opy_ (u"࡚ࠫࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡢࡥࡦࡩࡸࡹࠠࡢࠢࡳࡶ࡮ࡼࡡࡵࡧࠣࡨࡴࡳࡡࡪࡰ࠽ࠤࢀࢃࠠ࠯ࠢࡖࡩࡹࠦࡴࡩࡧࠣࡪࡴࡲ࡬ࡰࡹ࡬ࡲ࡬ࠦࡣࡰࡰࡩ࡭࡬ࠦࡩ࡯ࠢࡼࡳࡺࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠣࡪ࡮ࡲࡥ࠻ࠢ࡟ࡲ࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭࠮ࠢ࡟ࡲࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭࠼ࠣࡸࡷࡻࡥࠡ࡞ࡱ࠱࠲࠳࠭࠮࠯࠰࠱࠲࠳࠭ࠨெ")
bstack111lll11_opy_ = bstack1l1_opy_ (u"࡙ࠬ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࡡࡨࡶࡷࡵࡲࠡ࠼ࠣࡿࢂ࠭ே")
from ._version import __version__
bstack1ll11l_opy_ = None
CONFIG = {}
bstack1l11llll_opy_ = None
bstack1lll1llll_opy_ = None
bstack11ll1ll1_opy_ = None
bstack1l11l1l1_opy_ = -1
bstack1ll11l11_opy_ = DEFAULT_LOG_LEVEL
bstack1l1111l1_opy_ = 1
bstack1l1ll1l1_opy_ = False
bstack1l11lll1_opy_ = bstack1l1_opy_ (u"࠭ࠧை")
bstack1lll11l1_opy_ = bstack1l1_opy_ (u"ࠧࠨ௉")
bstack11l111_opy_ = False
bstack1111llll_opy_ = None
bstack1lllll11l_opy_ = None
bstack1ll1l11_opy_ = None
bstack11l1l11l_opy_ = None
bstack1ll1lll11_opy_ = None
bstack1lll11l_opy_ = None
bstack1lllll1ll_opy_ = None
bstack1l1l1l11_opy_ = None
bstack11l1l1_opy_ = None
bstack1l1l11l_opy_ = None
bstack11ll11l1_opy_ = bstack1l1_opy_ (u"ࠣࠤொ")
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1ll11l11_opy_,
                    format=bstack1l1_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧோ"),
                    datefmt=bstack1l1_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬௌ"))
def bstack1ll1ll1ll_opy_():
  global CONFIG
  global bstack1ll11l11_opy_
  if bstack1l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ்࠭") in CONFIG:
    bstack1ll11l11_opy_ = bstack11lll_opy_[CONFIG[bstack1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧ௎")]]
    logging.getLogger().setLevel(bstack1ll11l11_opy_)
def bstack1llll11l_opy_():
  from bstack1ll1ll11_opy_.version import version as bstack1l111111_opy_
  return version.parse(bstack1l111111_opy_)
def bstack1l11ll1l_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1lll1ll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥࠣ௏") in args[i].lower():
      path = args[i+1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      return path
  return None
def bstack1ll1lll1_opy_():
  bstack1l111lll_opy_ = bstack1lll1ll1_opy_()
  if bstack1l111lll_opy_ and os.path.exists(os.path.abspath(bstack1l111lll_opy_)):
    fileName = bstack1l111lll_opy_
  if bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫௐ") in os.environ and os.path.exists(os.path.abspath(os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬ௑")])) and not bstack1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ௒") in locals():
    fileName = os.environ[bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧ௓")]
  if not bstack1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࠭௔") in locals():
    fileName = bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ௕")
  bstack1ll11lll1_opy_ = os.path.abspath(fileName)
  if not os.path.exists(bstack1ll11lll1_opy_):
    fileName = bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿࡡ࡮࡮ࠪ௖")
    bstack1ll11lll1_opy_ = os.path.abspath(fileName)
    if not os.path.exists(bstack1ll11lll1_opy_):
      bstack111lll_opy_(
        bstack111ll111_opy_.format(os.getcwd()))
  with open(bstack1ll11lll1_opy_, bstack1l1_opy_ (u"ࠧࡳࠩௗ")) as stream:
    try:
      config = yaml.safe_load(stream)
      return config
    except yaml.YAMLError as exc:
      bstack111lll_opy_(bstack111ll1ll_opy_.format(str(exc)))
def bstack1ll111l_opy_(config):
  bstack111111l1_opy_ = bstack11lll11_opy_(config)
  for option in list(bstack111111l1_opy_):
    if option.lower() in bstack11111_opy_ and option != bstack11111_opy_[option.lower()]:
      bstack111111l1_opy_[bstack11111_opy_[option.lower()]] = bstack111111l1_opy_[option]
      del bstack111111l1_opy_[option]
  return config
def bstack1llll1lll_opy_(config):
  bstack1lll11ll1_opy_ = config.keys()
  for bstack1l1l1lll_opy_, bstack1ll1ll111_opy_ in bstack1ll1l_opy_.items():
    if bstack1ll1ll111_opy_ in bstack1lll11ll1_opy_:
      config[bstack1l1l1lll_opy_] = config[bstack1ll1ll111_opy_]
      del config[bstack1ll1ll111_opy_]
  for bstack1l1l1lll_opy_, bstack1ll1ll111_opy_ in bstack11ll1_opy_.items():
    if isinstance(bstack1ll1ll111_opy_, list):
      for bstack111lll1_opy_ in bstack1ll1ll111_opy_:
        if bstack111lll1_opy_ in bstack1lll11ll1_opy_:
          config[bstack1l1l1lll_opy_] = config[bstack111lll1_opy_]
          del config[bstack111lll1_opy_]
          break
    elif bstack1ll1ll111_opy_ in bstack1lll11ll1_opy_:
        config[bstack1l1l1lll_opy_] = config[bstack1ll1ll111_opy_]
        del config[bstack1ll1ll111_opy_]
  for bstack111lll1_opy_ in list(config):
    for bstack1l1l1ll1_opy_ in bstack11ll_opy_:
      if bstack111lll1_opy_.lower() == bstack1l1l1ll1_opy_.lower() and bstack111lll1_opy_ != bstack1l1l1ll1_opy_:
        config[bstack1l1l1ll1_opy_] = config[bstack111lll1_opy_]
        del config[bstack111lll1_opy_]
  bstack11l11ll1_opy_ = []
  if bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௘") in config:
    bstack11l11ll1_opy_ = config[bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௙")]
  for platform in bstack11l11ll1_opy_:
    for bstack111lll1_opy_ in list(platform):
      for bstack1l1l1ll1_opy_ in bstack11ll_opy_:
        if bstack111lll1_opy_.lower() == bstack1l1l1ll1_opy_.lower() and bstack111lll1_opy_ != bstack1l1l1ll1_opy_:
          platform[bstack1l1l1ll1_opy_] = platform[bstack111lll1_opy_]
          del platform[bstack111lll1_opy_]
  for bstack1l1l1lll_opy_, bstack1ll1ll111_opy_ in bstack11ll1_opy_.items():
    for platform in bstack11l11ll1_opy_:
      if isinstance(bstack1ll1ll111_opy_, list):
        for bstack111lll1_opy_ in bstack1ll1ll111_opy_:
          if bstack111lll1_opy_ in platform:
            platform[bstack1l1l1lll_opy_] = platform[bstack111lll1_opy_]
            del platform[bstack111lll1_opy_]
            break
      elif bstack1ll1ll111_opy_ in platform:
        platform[bstack1l1l1lll_opy_] = platform[bstack1ll1ll111_opy_]
        del platform[bstack1ll1ll111_opy_]
  for bstack1111l111_opy_ in bstack1lllll_opy_:
    if bstack1111l111_opy_ in config:
      if not bstack1lllll_opy_[bstack1111l111_opy_] in config:
        config[bstack1lllll_opy_[bstack1111l111_opy_]] = {}
      config[bstack1lllll_opy_[bstack1111l111_opy_]].update(config[bstack1111l111_opy_])
      del config[bstack1111l111_opy_]
  for platform in bstack11l11ll1_opy_:
    for bstack1111l111_opy_ in bstack1lllll_opy_:
      if bstack1111l111_opy_ in list(platform):
        if not bstack1lllll_opy_[bstack1111l111_opy_] in platform:
          platform[bstack1lllll_opy_[bstack1111l111_opy_]] = {}
        platform[bstack1lllll_opy_[bstack1111l111_opy_]].update(platform[bstack1111l111_opy_])
        del platform[bstack1111l111_opy_]
  config = bstack1ll111l_opy_(config)
  return config
def bstack111l1lll_opy_(config):
  global bstack1lll11l1_opy_
  if bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ௚") in config and str(config[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ௛")]).lower() != bstack1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ௜"):
    if not bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ௝") in config:
      config[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ௞")] = {}
    if not bstack1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ௟") in config[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭௠")]:
      if bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ௡") in os.environ:
        config[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ௢")][bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௣")] = os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ௤")]
      else:
        current_time = datetime.datetime.now()
        bstack1l1111ll_opy_ = current_time.strftime(bstack1l1_opy_ (u"ࠧࠦࡦࡢࠩࡧࡥࠥࡉࠧࡐࠫ௥"))
        hostname = socket.gethostname()
        bstack1lllll1_opy_ = bstack1l1_opy_ (u"ࠨࠩ௦").join(random.choices(string.ascii_lowercase + string.digits, k=4))
        identifier = bstack1l1_opy_ (u"ࠩࡾࢁࡤࢁࡽࡠࡽࢀࠫ௧").format(bstack1l1111ll_opy_, hostname, bstack1lllll1_opy_)
        config[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ௨")][bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭௩")] = identifier
    bstack1lll11l1_opy_ = config[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ௪")][bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௫")]
  return config
def bstack1l11l11_opy_(config):
  if bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ௬") in config and config[bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ௭")] not in bstack1lll11_opy_:
    return config[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ௮")]
  elif bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭௯") in os.environ:
    return os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡈࡉࡅࡔࡕࡢࡏࡊ࡟ࠧ௰")]
  else:
    return None
def bstack1111ll11_opy_(config):
  if bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡒࡆࡓࡅࠨ௱") in os.environ:
    return os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡓࡇࡍࡆࠩ௲")]
  elif bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ௳") in config:
    return config[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ௴")]
  else:
    return None
def bstack1ll1l1111_opy_():
  if (
    isinstance(os.getenv(bstack1l1_opy_ (u"ࠩࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠧ௵")), str) and len(os.getenv(bstack1l1_opy_ (u"ࠪࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠨ௶"))) > 0
  ) or (
    isinstance(os.getenv(bstack1l1_opy_ (u"ࠫࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠪ௷")), str) and len(os.getenv(bstack1l1_opy_ (u"ࠬࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠫ௸"))) > 0
  ):
    return os.getenv(bstack1l1_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬ௹"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠧࡄࡋࠪ௺"))).lower() == bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭௻") and str(os.getenv(bstack1l1_opy_ (u"ࠩࡆࡍࡗࡉࡌࡆࡅࡌࠫ௼"))).lower() == bstack1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨ௽"):
    return os.getenv(bstack1l1_opy_ (u"ࠫࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠧ௾"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠬࡉࡉࠨ௿"))).lower() == bstack1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫఀ") and str(os.getenv(bstack1l1_opy_ (u"ࠧࡕࡔࡄ࡚ࡎ࡙ࠧఁ"))).lower() == bstack1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ం"):
    return os.getenv(bstack1l1_opy_ (u"ࠩࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠨః"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠪࡇࡎ࠭ఄ"))).lower() == bstack1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩఅ") and str(os.getenv(bstack1l1_opy_ (u"ࠬࡉࡉࡠࡐࡄࡑࡊ࠭ఆ"))).lower() == bstack1l1_opy_ (u"࠭ࡣࡰࡦࡨࡷ࡭࡯ࡰࠨఇ"):
    return 0 # bstack11lllll1_opy_ bstack1ll11111_opy_ not set build number env
  if os.getenv(bstack1l1_opy_ (u"ࠧࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆࡗࡇࡎࡄࡊࠪఈ")) and os.getenv(bstack1l1_opy_ (u"ࠨࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡈࡕࡍࡎࡋࡗࠫఉ")):
    return os.getenv(bstack1l1_opy_ (u"ࠩࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠫఊ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠪࡇࡎ࠭ఋ"))).lower() == bstack1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩఌ") and str(os.getenv(bstack1l1_opy_ (u"ࠬࡊࡒࡐࡐࡈࠫ఍"))).lower() == bstack1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫఎ"):
    return os.getenv(bstack1l1_opy_ (u"ࠧࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠬఏ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠨࡅࡌࠫఐ"))).lower() == bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ఑") and str(os.getenv(bstack1l1_opy_ (u"ࠪࡗࡊࡓࡁࡑࡊࡒࡖࡊ࠭ఒ"))).lower() == bstack1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩఓ"):
    return os.getenv(bstack1l1_opy_ (u"࡙ࠬࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠨఔ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"࠭ࡃࡊࠩక"))).lower() == bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬఖ") and str(os.getenv(bstack1l1_opy_ (u"ࠨࡉࡌࡘࡑࡇࡂࡠࡅࡌࠫగ"))).lower() == bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧఘ"):
    return os.getenv(bstack1l1_opy_ (u"ࠪࡇࡎࡥࡊࡐࡄࡢࡍࡉ࠭ఙ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠫࡈࡏࠧచ"))).lower() == bstack1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪఛ") and str(os.getenv(bstack1l1_opy_ (u"࠭ࡂࡖࡋࡏࡈࡐࡏࡔࡆࠩజ"))).lower() == bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬఝ"):
    return os.getenv(bstack1l1_opy_ (u"ࠨࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠪఞ"), 0)
  if str(os.getenv(bstack1l1_opy_ (u"ࠩࡗࡊࡤࡈࡕࡊࡎࡇࠫట"))).lower() == bstack1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨఠ"):
    return os.getenv(bstack1l1_opy_ (u"ࠫࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠫడ"), 0)
  return -1
def bstack11l1ll1l_opy_(bstack1llll1ll_opy_):
  global CONFIG
  if not bstack1l1_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧఢ") in CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨణ")]:
    return
  CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩత")] = CONFIG[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪథ")].replace(
    bstack1l1_opy_ (u"ࠩࠧࡿࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࢀࠫద"),
    str(bstack1llll1ll_opy_)
  )
def bstack1l11lll_opy_():
  global CONFIG
  if not bstack1l1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩధ") in CONFIG[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭న")]:
    return
  current_time = datetime.datetime.now()
  bstack1l1111ll_opy_ = current_time.strftime(bstack1l1_opy_ (u"ࠬࠫࡤ࠮ࠧࡥ࠱ࠪࡎ࠺ࠦࡏࠪ఩"))
  CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨప")] = CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩఫ")].replace(
    bstack1l1_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧబ"),
    bstack1l1111ll_opy_
  )
def bstack1l1l11_opy_():
  global CONFIG
  if bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫభ") in CONFIG and not bool(CONFIG[bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬమ")]):
    del CONFIG[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭య")]
    return
  if not bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧర") in CONFIG:
    CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨఱ")] = bstack1l1_opy_ (u"ࠧࠤࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪల")
  if bstack1l1_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧళ") in CONFIG[bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫఴ")]:
    bstack1l11lll_opy_()
    os.environ[bstack1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧవ")] = CONFIG[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭శ")]
  if not bstack1l1_opy_ (u"ࠬࠪࡻࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࢃࠧష") in CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨస")]:
    return
  bstack1llll1ll_opy_ = bstack1l1_opy_ (u"ࠧࠨహ")
  bstack1lll111l1_opy_ = bstack1ll1l1111_opy_()
  if bstack1lll111l1_opy_ != -1:
    bstack1llll1ll_opy_ = bstack1l1_opy_ (u"ࠨࡅࡌࠤࠬ఺") + str(bstack1lll111l1_opy_)
  if bstack1llll1ll_opy_ == bstack1l1_opy_ (u"ࠩࠪ఻"):
    bstack11l1l111_opy_ = bstack1lll11l11_opy_(CONFIG[bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ఼࠭")])
    if bstack11l1l111_opy_ != -1:
      bstack1llll1ll_opy_ = str(bstack11l1l111_opy_)
  if bstack1llll1ll_opy_:
    bstack11l1ll1l_opy_(bstack1llll1ll_opy_)
    os.environ[bstack1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨఽ")] = CONFIG[bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧా")]
def bstack1l11l1ll_opy_(bstack1111lll1_opy_, bstack1ll1lllll_opy_, path):
  bstack11111l11_opy_ = {
    bstack1l1_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪి"): bstack1ll1lllll_opy_
  }
  if os.path.exists(path):
    bstack1lll111ll_opy_ = json.load(open(path, bstack1l1_opy_ (u"ࠧࡳࡤࠪీ")))
  else:
    bstack1lll111ll_opy_ = {}
  bstack1lll111ll_opy_[bstack1111lll1_opy_] = bstack11111l11_opy_
  with open(path, bstack1l1_opy_ (u"ࠣࡹ࠮ࠦు")) as outfile:
    json.dump(bstack1lll111ll_opy_, outfile)
def bstack1lll11l11_opy_(bstack1111lll1_opy_):
  bstack1111lll1_opy_ = str(bstack1111lll1_opy_)
  bstack1l1ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠩࢁࠫూ")), bstack1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪృ"))
  try:
    if not os.path.exists(bstack1l1ll1ll_opy_):
      os.makedirs(bstack1l1ll1ll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠫࢃ࠭ౄ")), bstack1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ౅"), bstack1l1_opy_ (u"࠭࠮ࡣࡷ࡬ࡰࡩ࠳࡮ࡢ࡯ࡨ࠱ࡨࡧࡣࡩࡧ࠱࡮ࡸࡵ࡮ࠨె"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1l1_opy_ (u"ࠧࡸࠩే")):
        pass
      with open(file_path, bstack1l1_opy_ (u"ࠣࡹ࠮ࠦై")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1l1_opy_ (u"ࠩࡵࠫ౉")) as bstack11lll1l1_opy_:
      bstack111l1111_opy_ = json.load(bstack11lll1l1_opy_)
    if bstack1111lll1_opy_ in bstack111l1111_opy_:
      bstack1111111l_opy_ = bstack111l1111_opy_[bstack1111lll1_opy_][bstack1l1_opy_ (u"ࠪ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧొ")]
      bstack1ll11l1_opy_ = int(bstack1111111l_opy_) + 1
      bstack1l11l1ll_opy_(bstack1111lll1_opy_, bstack1ll11l1_opy_, file_path)
      return bstack1ll11l1_opy_
    else:
      bstack1l11l1ll_opy_(bstack1111lll1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack11111lll_opy_.format(str(e)))
    return -1
def bstack11lll111_opy_(config):
  if bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ో") in config and config[bstack1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧౌ")] not in bstack1llll_opy_:
    return config[bstack1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ్")]
  elif bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ౎") in os.environ:
    return os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ౏")]
  else:
    return None
def bstack1llllll11_opy_(config):
  if not bstack11lll111_opy_(config) or not bstack1l11l11_opy_(config):
    return True
  else:
    return False
def bstack11llllll_opy_(config):
  if bstack1l11ll1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨ౐")):
    return False
  if bstack1l11ll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩ౑")):
    return True
  if bstack1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ౒") in config and config[bstack1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ౓")] == False:
    return False
  else:
    return True
def bstack111lllll_opy_(config, index = 0):
  global bstack11l111_opy_
  bstack1l1lllll_opy_ = {}
  caps = bstack1l1l1_opy_ + bstack1ll11_opy_
  if bstack11l111_opy_:
    caps += bstack111l_opy_
  for key in config:
    if key in caps + [bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౔")]:
      continue
    bstack1l1lllll_opy_[key] = config[key]
  if bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵౕࠪ") in config:
    for bstack111l11l_opy_ in config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶౖࠫ")][index]:
      if bstack111l11l_opy_ in caps + [bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ౗"), bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫౘ")]:
        continue
      bstack1l1lllll_opy_[bstack111l11l_opy_] = config[bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౙ")][index][bstack111l11l_opy_]
  bstack1l1lllll_opy_[bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࠧౚ")] = socket.gethostname()
  return bstack1l1lllll_opy_
def bstack11l1lll_opy_(config):
  global bstack11l111_opy_
  bstack1ll1l1l_opy_ = {}
  caps = bstack1ll11_opy_
  if bstack11l111_opy_:
    caps+= bstack111l_opy_
  for key in caps:
    if key in config:
      bstack1ll1l1l_opy_[key] = config[key]
  return bstack1ll1l1l_opy_
def bstack11l11ll_opy_(bstack1l1lllll_opy_, bstack1ll1l1l_opy_):
  bstack1l1l111_opy_ = {}
  for key in bstack1l1lllll_opy_.keys():
    if key in bstack1ll1l_opy_:
      bstack1l1l111_opy_[bstack1ll1l_opy_[key]] = bstack1l1lllll_opy_[key]
    else:
      bstack1l1l111_opy_[key] = bstack1l1lllll_opy_[key]
  for key in bstack1ll1l1l_opy_:
    if key in bstack1ll1l_opy_:
      bstack1l1l111_opy_[bstack1ll1l_opy_[key]] = bstack1ll1l1l_opy_[key]
    else:
      bstack1l1l111_opy_[key] = bstack1ll1l1l_opy_[key]
  return bstack1l1l111_opy_
def bstack1ll111ll_opy_(config, index = 0):
  global bstack11l111_opy_
  caps = {}
  bstack1ll1l1l_opy_ = bstack11l1lll_opy_(config)
  bstack11l1lll1_opy_ = bstack1ll11_opy_
  bstack11l1lll1_opy_ += bstack11l1_opy_
  if bstack11l111_opy_:
    bstack11l1lll1_opy_ += bstack111l_opy_
  if bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౛") in config:
    if bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ౜") in config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫౝ")][index]:
      caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ౞")] = config[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౟")][index][bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩౠ")]
    if bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ౡ") in config[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩౢ")][index]:
      caps[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨౣ")] = str(config[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ౤")][index][bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ౥")])
    bstack11llll_opy_ = {}
    for bstack1lll1111_opy_ in bstack11l1lll1_opy_:
      if bstack1lll1111_opy_ in config[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౦")][index]:
        if bstack1lll1111_opy_ == bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౧"):
          bstack11llll_opy_[bstack1lll1111_opy_] = str(config[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ౨")][index][bstack1lll1111_opy_] * 1.0)
        else:
          bstack11llll_opy_[bstack1lll1111_opy_] = config[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ౩")][index][bstack1lll1111_opy_]
        del(config[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ౪")][index][bstack1lll1111_opy_])
    bstack1ll1l1l_opy_ = update(bstack1ll1l1l_opy_, bstack11llll_opy_)
  bstack1l1lllll_opy_ = bstack111lllll_opy_(config, index)
  for bstack111lll1_opy_ in bstack1ll11_opy_ + [bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭౫"), bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ౬")]:
    if bstack111lll1_opy_ in bstack1l1lllll_opy_:
      bstack1ll1l1l_opy_[bstack111lll1_opy_] = bstack1l1lllll_opy_[bstack111lll1_opy_]
      del(bstack1l1lllll_opy_[bstack111lll1_opy_])
  if bstack11llllll_opy_(config):
    bstack1l1lllll_opy_[bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ౭")] = True
    caps.update(bstack1ll1l1l_opy_)
    caps[bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ౮")] = bstack1l1lllll_opy_
  else:
    bstack1l1lllll_opy_[bstack1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ౯")] = False
    caps.update(bstack11l11ll_opy_(bstack1l1lllll_opy_, bstack1ll1l1l_opy_))
    if bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ౰") in caps:
      caps[bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨ౱")] = caps[bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭౲")]
      del(caps[bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ౳")])
    if bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ౴") in caps:
      caps[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭౵")] = caps[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭౶")]
      del(caps[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ౷")])
  return caps
def bstack1lll11lll_opy_():
  if bstack1l11ll1l_opy_() <= version.parse(bstack1l1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ౸")):
    return bstack11l11_opy_
  return bstack111l1_opy_
def bstack1l11l1_opy_(options):
  return hasattr(options, bstack1l1_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩ౹"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack111111ll_opy_(options, bstack1llllllll_opy_):
  for bstack11lll1_opy_ in bstack1llllllll_opy_:
    if bstack11lll1_opy_ in [bstack1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ౺"), bstack1l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ౻")]:
      next
    if bstack11lll1_opy_ in options._experimental_options:
      options._experimental_options[bstack11lll1_opy_]= update(options._experimental_options[bstack11lll1_opy_], bstack1llllllll_opy_[bstack11lll1_opy_])
    else:
      options.add_experimental_option(bstack11lll1_opy_, bstack1llllllll_opy_[bstack11lll1_opy_])
  if bstack1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩ౼") in bstack1llllllll_opy_:
    for arg in bstack1llllllll_opy_[bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪ౽")]:
      options.add_argument(arg)
    del(bstack1llllllll_opy_[bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫ౾")])
  if bstack1l1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ౿") in bstack1llllllll_opy_:
    for ext in bstack1llllllll_opy_[bstack1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬಀ")]:
      options.add_extension(ext)
    del(bstack1llllllll_opy_[bstack1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ಁ")])
def bstack1ll111_opy_(options, bstack1llll11ll_opy_):
  if bstack1l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩಂ") in bstack1llll11ll_opy_:
    for bstack1l1lll_opy_ in bstack1llll11ll_opy_[bstack1l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪಃ")]:
      if bstack1l1lll_opy_ in options._preferences:
        options._preferences[bstack1l1lll_opy_] = update(options._preferences[bstack1l1lll_opy_], bstack1llll11ll_opy_[bstack1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ಄")][bstack1l1lll_opy_])
      else:
        options.set_preference(bstack1l1lll_opy_, bstack1llll11ll_opy_[bstack1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬಅ")][bstack1l1lll_opy_])
  if bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬಆ") in bstack1llll11ll_opy_:
    for arg in bstack1llll11ll_opy_[bstack1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ಇ")]:
      options.add_argument(arg)
def bstack1ll1l1ll_opy_(options, bstack1lllllll_opy_):
  if bstack1l1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࠪಈ") in bstack1lllllll_opy_:
    options.use_webview(bool(bstack1lllllll_opy_[bstack1l1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫಉ")]))
  bstack111111ll_opy_(options, bstack1lllllll_opy_)
def bstack111l1ll_opy_(options, bstack1ll11l1l_opy_):
  for bstack1ll1111l_opy_ in bstack1ll11l1l_opy_:
    if bstack1ll1111l_opy_ in [bstack1l1_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨಊ"), bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪಋ")]:
      next
    options.set_capability(bstack1ll1111l_opy_, bstack1ll11l1l_opy_[bstack1ll1111l_opy_])
  if bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫಌ") in bstack1ll11l1l_opy_:
    for arg in bstack1ll11l1l_opy_[bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ಍")]:
      options.add_argument(arg)
  if bstack1l1_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬಎ") in bstack1ll11l1l_opy_:
    options.use_technology_preview(bool(bstack1ll11l1l_opy_[bstack1l1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ಏ")]))
def bstack1l1l1ll_opy_(options, bstack1l11111l_opy_):
  for bstack11l1llll_opy_ in bstack1l11111l_opy_:
    if bstack11l1llll_opy_ in [bstack1l1_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧಐ"), bstack1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩ಑")]:
      next
    options._options[bstack11l1llll_opy_] = bstack1l11111l_opy_[bstack11l1llll_opy_]
  if bstack1l1_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩಒ") in bstack1l11111l_opy_:
    for bstack1llllll1l_opy_ in bstack1l11111l_opy_[bstack1l1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪಓ")]:
      options.add_additional_option(
          bstack1llllll1l_opy_, bstack1l11111l_opy_[bstack1l1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫಔ")][bstack1llllll1l_opy_])
  if bstack1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ಕ") in bstack1l11111l_opy_:
    for arg in bstack1l11111l_opy_[bstack1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧಖ")]:
      options.add_argument(arg)
def bstack11llll11_opy_(options, caps):
  if not hasattr(options, bstack1l1_opy_ (u"ࠪࡏࡊ࡟ࠧಗ")):
    return
  if options.KEY == bstack1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩಘ") and options.KEY in caps:
    bstack111111ll_opy_(options, caps[bstack1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪಙ")])
  elif options.KEY == bstack1l1_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫಚ") and options.KEY in caps:
    bstack1ll111_opy_(options, caps[bstack1l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬಛ")])
  elif options.KEY == bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩಜ") and options.KEY in caps:
    bstack111l1ll_opy_(options, caps[bstack1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪಝ")])
  elif options.KEY == bstack1l1_opy_ (u"ࠪࡱࡸࡀࡥࡥࡩࡨࡓࡵࡺࡩࡰࡰࡶࠫಞ") and options.KEY in caps:
    bstack1ll1l1ll_opy_(options, caps[bstack1l1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬಟ")])
  elif options.KEY == bstack1l1_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫಠ") and options.KEY in caps:
    bstack1l1l1ll_opy_(options, caps[bstack1l1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬಡ")])
def bstack1llll1l_opy_(caps):
  global bstack11l111_opy_
  if bstack11l111_opy_:
    if bstack1llll11l_opy_() < version.parse(bstack1l1_opy_ (u"ࠧ࠳࠰࠶࠲࠵࠭ಢ")):
      return None
    else:
      from bstack1ll1ll11_opy_.options.common.base import bstack1lll11111_opy_
      options = bstack1lll11111_opy_().bstack1l1l11ll_opy_(caps)
      return options
  else:
    browser = bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨಣ")
    if bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧತ") in caps:
      browser = caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨಥ")]
    elif bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬದ") in caps:
      browser = caps[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ಧ")]
    browser = str(browser).lower()
    if browser == bstack1l1_opy_ (u"࠭ࡩࡱࡪࡲࡲࡪ࠭ನ") or browser == bstack1l1_opy_ (u"ࠧࡪࡲࡤࡨࠬ಩"):
      browser = bstack1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࠨಪ")
    if browser == bstack1l1_opy_ (u"ࠩࡶࡥࡲࡹࡵ࡯ࡩࠪಫ"):
      browser = bstack1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪಬ")
    if browser not in [bstack1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫಭ"), bstack1l1_opy_ (u"ࠬ࡫ࡤࡨࡧࠪಮ"), bstack1l1_opy_ (u"࠭ࡩࡦࠩಯ"), bstack1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧರ"), bstack1l1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩಱ")]:
      return None
    try:
      package = bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡼࡿ࠱ࡳࡵࡺࡩࡰࡰࡶࠫಲ").format(browser)
      name = bstack1l1_opy_ (u"ࠪࡓࡵࡺࡩࡰࡰࡶࠫಳ")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1l11l1_opy_(options):
        return None
      for bstack111lll1_opy_ in caps.keys():
        options.set_capability(bstack111lll1_opy_, caps[bstack111lll1_opy_])
      bstack11llll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111l11l1_opy_(options, bstack1llll1l1l_opy_):
  if not bstack1l11l1_opy_(options):
    return
  for bstack111lll1_opy_ in bstack1llll1l1l_opy_.keys():
    if bstack111lll1_opy_ in bstack11l1_opy_:
      next
    if bstack111lll1_opy_ in options._caps and type(options._caps[bstack111lll1_opy_]) in [dict, list]:
      options._caps[bstack111lll1_opy_] = update(options._caps[bstack111lll1_opy_], bstack1llll1l1l_opy_[bstack111lll1_opy_])
    else:
      options.set_capability(bstack111lll1_opy_, bstack1llll1l1l_opy_[bstack111lll1_opy_])
  bstack11llll11_opy_(options, bstack1llll1l1l_opy_)
  if bstack1l1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪ಴") in options._caps:
    if options._caps[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪವ")] and options._caps[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫಶ")].lower() != bstack1l1_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨಷ"):
      del options._caps[bstack1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧಸ")]
def bstack1lll111_opy_(proxy_config):
  if bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ಹ") in proxy_config:
    proxy_config[bstack1l1_opy_ (u"ࠪࡷࡸࡲࡐࡳࡱࡻࡽࠬ಺")] = proxy_config[bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ಻")]
    del(proxy_config[bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺ಼ࠩ")])
  if bstack1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩಽ") in proxy_config and proxy_config[bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡚ࡹࡱࡧࠪಾ")].lower() != bstack1l1_opy_ (u"ࠨࡦ࡬ࡶࡪࡩࡴࠨಿ"):
    proxy_config[bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬೀ")] = bstack1l1_opy_ (u"ࠪࡱࡦࡴࡵࡢ࡮ࠪು")
  if bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡄࡹࡹࡵࡣࡰࡰࡩ࡭࡬࡛ࡲ࡭ࠩೂ") in proxy_config:
    proxy_config[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨೃ")] = bstack1l1_opy_ (u"࠭ࡰࡢࡥࠪೄ")
  return proxy_config
def bstack11ll111_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭೅") in config:
    return proxy
  config[bstack1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧೆ")] = bstack1lll111_opy_(config[bstack1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨೇ")])
  if proxy == None:
    proxy = Proxy(config[bstack1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩೈ")])
  return proxy
def bstack11l11l1l_opy_(self):
  global CONFIG
  global bstack1l1l1l11_opy_
  if bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ೉") in CONFIG and bstack1lll11lll_opy_().startswith(bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࠭ೊ")):
    return CONFIG[bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩೋ")]
  elif bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫೌ") in CONFIG and bstack1lll11lll_opy_().startswith(bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱್ࠪ")):
    return CONFIG[bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭೎")]
  else:
    return bstack1l1l1l11_opy_(self)
def bstack11ll1l1_opy_():
  if bstack1l11ll1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࠩ೏")):
    logger.warning(bstack111ll11l_opy_.format(bstack1l11ll1l_opy_()))
    return
  global bstack1l1l1l11_opy_
  from selenium.webdriver.remote.remote_connection import RemoteConnection
  bstack1l1l1l11_opy_ = RemoteConnection._get_proxy_url
  RemoteConnection._get_proxy_url = bstack11l11l1l_opy_
def bstack11l1l11_opy_(config):
  if bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ೐") in config:
    if str(config[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ೑")]).lower() == bstack1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫ೒"):
      return True
    else:
      return False
  elif bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࠬ೓") in os.environ:
    if str(os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑ࠭೔")]).lower() == bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧೕ"):
      return True
    else:
      return False
  else:
    return False
def bstack11lll11_opy_(config):
  if bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧೖ") in config:
    return config[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ೗")]
  if bstack1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ೘") in config:
    return config[bstack1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬ೙")]
  return {}
def bstack1ll1ll1_opy_(caps):
  global bstack1lll11l1_opy_
  if bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ೚") in caps:
    caps[bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ೛")][bstack1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨ೜")] = True
    if bstack1lll11l1_opy_:
      caps[bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫೝ")][bstack1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ೞ")] = bstack1lll11l1_opy_
  else:
    caps[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪ೟")] = True
    if bstack1lll11l1_opy_:
      caps[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧೠ")] = bstack1lll11l1_opy_
def bstack11l1ll1_opy_():
  global CONFIG
  if bstack11l1l11_opy_(CONFIG):
    bstack111111l1_opy_ = bstack11lll11_opy_(CONFIG)
    bstack111l1ll1_opy_(bstack1l11l11_opy_(CONFIG), bstack111111l1_opy_)
def bstack111l1ll1_opy_(key, bstack111111l1_opy_):
  global bstack1ll11l_opy_
  logger.info(bstack1lll1111l_opy_)
  try:
    bstack1ll11l_opy_ = Local()
    bstack1l111ll1_opy_ = {bstack1l1_opy_ (u"ࠧ࡬ࡧࡼࠫೡ"): key}
    bstack1l111ll1_opy_.update(bstack111111l1_opy_)
    logger.debug(bstack11lll1ll_opy_.format(str(bstack1l111ll1_opy_)))
    bstack1ll11l_opy_.start(**bstack1l111ll1_opy_)
    if bstack1ll11l_opy_.isRunning():
      logger.info(bstack11ll1l11_opy_)
  except Exception as e:
    bstack111lll_opy_(bstack1111l1l1_opy_.format(str(e)))
def bstack1llllll1_opy_():
  global bstack1ll11l_opy_
  if bstack1ll11l_opy_.isRunning():
    logger.info(bstack11lll1l_opy_)
    bstack1ll11l_opy_.stop()
  bstack1ll11l_opy_ = None
def bstack111lll1l_opy_():
  global bstack11ll11l1_opy_
  if bstack11ll11l1_opy_:
    logger.warning(bstack1l111l_opy_.format(str(bstack11ll11l1_opy_)))
  logger.info(bstack11lllll_opy_)
  global bstack1ll11l_opy_
  if bstack1ll11l_opy_:
    bstack1llllll1_opy_()
  logger.info(bstack1l1l1l_opy_)
def bstack1ll1l1l1_opy_(self, *args):
  logger.error(bstack111l111l_opy_)
  bstack111lll1l_opy_()
  sys.exit(1)
def bstack111lll_opy_(err):
  logger.critical(bstack1111ll_opy_.format(str(err)))
  atexit.unregister(bstack111lll1l_opy_)
  sys.exit(1)
def bstack1lll1ll11_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  atexit.unregister(bstack111lll1l_opy_)
  sys.exit(1)
def bstack11l1111_opy_():
  global CONFIG
  CONFIG = bstack1ll1lll1_opy_()
  CONFIG = bstack1llll1lll_opy_(CONFIG)
  CONFIG = bstack111l1lll_opy_(CONFIG)
  if bstack1llllll11_opy_(CONFIG):
    bstack111lll_opy_(bstack111l1l11_opy_)
  CONFIG[bstack1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪೢ")] = bstack11lll111_opy_(CONFIG)
  CONFIG[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬೣ")] = bstack1l11l11_opy_(CONFIG)
  if bstack1111ll11_opy_(CONFIG):
    CONFIG[bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭೤")] = bstack1111ll11_opy_(CONFIG)
    if not os.getenv(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠧ೥")):
      if os.getenv(bstack1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩ೦")):
        CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೧")] = os.getenv(bstack1l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ೨"))
      else:
        bstack1l1l11_opy_()
    else:
      if bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ೩") in CONFIG:
        del(CONFIG[bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೪")])
  bstack1ll1lll_opy_()
  bstack1l1ll1l_opy_()
  if bstack11l111_opy_:
    CONFIG[bstack1l1_opy_ (u"ࠪࡥࡵࡶࠧ೫")] = bstack11l11lll_opy_(CONFIG)
    logger.info(bstack111ll1_opy_.format(CONFIG[bstack1l1_opy_ (u"ࠫࡦࡶࡰࠨ೬")]))
def bstack1l1ll1l_opy_():
  global CONFIG
  global bstack11l111_opy_
  if bstack1l1_opy_ (u"ࠬࡧࡰࡱࠩ೭") in CONFIG:
    try:
      from bstack1ll1ll11_opy_ import version
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack111111_opy_)
    bstack11l111_opy_ = True
def bstack11l11lll_opy_(config):
  bstack111llll1_opy_ = bstack1l1_opy_ (u"࠭ࠧ೮")
  app = config[bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫ೯")]
  if isinstance(config[bstack1l1_opy_ (u"ࠨࡣࡳࡴࠬ೰")], str):
    if os.path.splitext(app)[1] in bstack1l11_opy_:
      if os.path.exists(app):
        bstack111llll1_opy_ = bstack1ll1llll_opy_(config, app)
      elif bstack1l1111_opy_(app):
        bstack111llll1_opy_ = app
      else:
        bstack111lll_opy_(bstack111l11_opy_.format(app))
    else:
      if bstack1l1111_opy_(app):
        bstack111llll1_opy_ = app
      elif os.path.exists(app):
        bstack111llll1_opy_ = bstack1ll1llll_opy_(app)
      else:
        bstack111lll_opy_(bstack11l111l_opy_)
  else:
    if len(app) > 2:
      bstack111lll_opy_(bstack1l11l11l_opy_)
    elif len(app) == 2:
      if bstack1l1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧೱ") in app and bstack1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢ࡭ࡩ࠭ೲ") in app:
        if os.path.exists(app[bstack1l1_opy_ (u"ࠫࡵࡧࡴࡩࠩೳ")]):
          bstack111llll1_opy_ = bstack1ll1llll_opy_(config, app[bstack1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ೴")], app[bstack1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ೵")])
        else:
          bstack111lll_opy_(bstack111l11_opy_.format(app))
      else:
        bstack111lll_opy_(bstack1l11l11l_opy_)
    else:
      for key in app:
        if key in bstack1llll1_opy_:
          if key == bstack1l1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ೶"):
            if os.path.exists(app[key]):
              bstack111llll1_opy_ = bstack1ll1llll_opy_(config, app[key])
            else:
              bstack111lll_opy_(bstack111l11_opy_.format(app))
          else:
            bstack111llll1_opy_ = app[key]
        else:
          bstack111lll_opy_(bstack1111l1l_opy_)
  return bstack111llll1_opy_
def bstack1l1111_opy_(bstack111llll1_opy_):
  import re
  bstack1lllll1l1_opy_ = re.compile(bstack1l1_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰ࠤࠣ೷"))
  bstack111l11ll_opy_ = re.compile(bstack1l1_opy_ (u"ࡴࠥࡢࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪ࠰࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ೸"))
  if bstack1l1_opy_ (u"ࠪࡦࡸࡀ࠯࠰ࠩ೹") in bstack111llll1_opy_ or re.fullmatch(bstack1lllll1l1_opy_, bstack111llll1_opy_) or re.fullmatch(bstack111l11ll_opy_, bstack111llll1_opy_):
    return True
  else:
    return False
def bstack1ll1llll_opy_(config, path, bstack11l1l1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1l1_opy_ (u"ࠫࡷࡨࠧ೺")).read()).hexdigest()
  bstack11l11111_opy_ = bstack1ll1ll1l_opy_(md5_hash)
  bstack111llll1_opy_ = None
  if bstack11l11111_opy_:
    logger.info(bstack1ll1l11ll_opy_.format(bstack11l11111_opy_, md5_hash))
    return bstack11l11111_opy_
  bstack1llll11l1_opy_ = MultipartEncoder(
    fields={
        bstack1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࠪ೻"): (os.path.basename(path), open(os.path.abspath(path), bstack1l1_opy_ (u"࠭ࡲࡣࠩ೼")), bstack1l1_opy_ (u"ࠧࡵࡧࡻࡸ࠴ࡶ࡬ࡢ࡫ࡱࠫ೽")),
        bstack1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫ೾"): bstack11l1l1ll_opy_
    }
  )
  response = requests.post(bstack1111l_opy_, data=bstack1llll11l1_opy_,
                         headers={bstack1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ೿"): bstack1llll11l1_opy_.content_type}, auth=(bstack11lll111_opy_(config), bstack1l11l11_opy_(config)))
  try:
    res = json.loads(response.text)
    bstack111llll1_opy_ = res[bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫഀ")]
    logger.info(bstack1l111l1l_opy_.format(bstack111llll1_opy_))
    bstack11ll111l_opy_(md5_hash, bstack111llll1_opy_)
  except ValueError as err:
    bstack111lll_opy_(bstack1lllll111_opy_.format(str(err)))
  return bstack111llll1_opy_
def bstack1ll1lll_opy_():
  global CONFIG
  global bstack1l1111l1_opy_
  bstack1lll1l1ll_opy_ = 1
  if bstack1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫഁ") in CONFIG:
    bstack1lll1l1ll_opy_ = CONFIG[bstack1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬം")]
  bstack1l111l1_opy_ = 0
  if bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩഃ") in CONFIG:
    bstack1l111l1_opy_ = len(CONFIG[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪഄ")])
  bstack1l1111l1_opy_ = int(bstack1lll1l1ll_opy_) * int(bstack1l111l1_opy_)
def bstack1ll1ll1l_opy_(md5_hash):
  bstack11lll11l_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠨࢀࠪഅ")), bstack1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩആ"), bstack1l1_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫഇ"))
  if os.path.exists(bstack11lll11l_opy_):
    bstack1l11ll1_opy_ = json.load(open(bstack11lll11l_opy_,bstack1l1_opy_ (u"ࠫࡷࡨࠧഈ")))
    if md5_hash in bstack1l11ll1_opy_:
      bstack1l1lll1l_opy_ = bstack1l11ll1_opy_[md5_hash]
      bstack11111ll1_opy_ = datetime.datetime.now()
      bstack1ll1l11l1_opy_ = datetime.datetime.strptime(bstack1l1lll1l_opy_[bstack1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨഉ")], bstack1l1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪഊ"))
      if (bstack11111ll1_opy_ - bstack1ll1l11l1_opy_).days > 60:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1lll1l_opy_[bstack1l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬഋ")]):
        return None
      return bstack1l1lll1l_opy_[bstack1l1_opy_ (u"ࠨ࡫ࡧࠫഌ")]
  else:
    return None
def bstack11ll111l_opy_(md5_hash, bstack111llll1_opy_):
  bstack1l1ll1ll_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠩࢁࠫ഍")), bstack1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪഎ"))
  if not os.path.exists(bstack1l1ll1ll_opy_):
    os.makedirs(bstack1l1ll1ll_opy_)
  bstack11lll11l_opy_ = os.path.join(os.path.expanduser(bstack1l1_opy_ (u"ࠫࢃ࠭ഏ")), bstack1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬഐ"), bstack1l1_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ഑"))
  bstack1l1ll11_opy_ = {
    bstack1l1_opy_ (u"ࠧࡪࡦࠪഒ"): bstack111llll1_opy_,
    bstack1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫഓ"): datetime.datetime.strftime(datetime.datetime.now(), bstack1l1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ഔ")),
    bstack1l1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨക"): str(__version__)
  }
  if os.path.exists(bstack11lll11l_opy_):
    bstack1l11ll1_opy_ = json.load(open(bstack11lll11l_opy_,bstack1l1_opy_ (u"ࠫࡷࡨࠧഖ")))
  else:
    bstack1l11ll1_opy_ = {}
  bstack1l11ll1_opy_[md5_hash] = bstack1l1ll11_opy_
  with open(bstack11lll11l_opy_, bstack1l1_opy_ (u"ࠧࡽࠫࠣഗ")) as outfile:
    json.dump(bstack1l11ll1_opy_, outfile)
def bstack1ll11llll_opy_(self):
  return
def bstack1l1l11l1_opy_(self):
  return
def bstack11l1l1l1_opy_(self):
  from selenium.webdriver.remote.webdriver import WebDriver
  WebDriver.quit(self)
def bstack1ll1l1l11_opy_(self, command_executor,
        desired_capabilities=None, browser_profile=None, proxy=None,
        keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l11llll_opy_
  global bstack1l11l1l1_opy_
  global bstack11ll1ll1_opy_
  global bstack1l1ll1l1_opy_
  global bstack1l11lll1_opy_
  global bstack1111llll_opy_
  CONFIG[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨഘ")] = str(bstack1l11lll1_opy_) + str(__version__)
  command_executor = bstack1lll11lll_opy_()
  logger.debug(bstack11ll1l1l_opy_.format(command_executor))
  proxy = bstack11ll111_opy_(CONFIG, proxy)
  bstack1lll1l1_opy_ = 0 if bstack1l11l1l1_opy_ < 0 else bstack1l11l1l1_opy_
  if bstack1l1ll1l1_opy_ is True:
    bstack1lll1l1_opy_ = int(threading.current_thread().getName())
  bstack1llll1l1l_opy_ = bstack1ll111ll_opy_(CONFIG, bstack1lll1l1_opy_)
  logger.debug(bstack111l1l_opy_.format(str(bstack1llll1l1l_opy_)))
  if bstack11l1l11_opy_(CONFIG):
    bstack1ll1ll1_opy_(bstack1llll1l1l_opy_)
  if desired_capabilities:
    bstack1111l11l_opy_ = bstack1ll111ll_opy_(bstack1llll1lll_opy_(desired_capabilities))
    if bstack1111l11l_opy_:
      bstack1llll1l1l_opy_ = update(bstack1111l11l_opy_, bstack1llll1l1l_opy_)
    desired_capabilities = None
  if options:
    bstack111l11l1_opy_(options, bstack1llll1l1l_opy_)
  if not options:
    options = bstack1llll1l_opy_(bstack1llll1l1l_opy_)
  if options and bstack1l11ll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ങ")):
    desired_capabilities = None
  if (
      not options and not desired_capabilities
  ) or (
      bstack1l11ll1l_opy_() < version.parse(bstack1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧച")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1llll1l1l_opy_)
  logger.info(bstack11l1111l_opy_)
  if bstack1l11ll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨഛ")):
    bstack1111llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities, options=options,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l11ll1l_opy_() >= version.parse(bstack1l1_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪജ")):
    bstack1111llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1111llll_opy_(self, command_executor=command_executor,
          desired_capabilities=desired_capabilities,
          browser_profile=browser_profile, proxy=proxy,
          keep_alive=keep_alive)
  bstack1l11llll_opy_ = self.session_id
  if bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഝ") in CONFIG and bstack1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪഞ") in CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩട")][bstack1lll1l1_opy_]:
    bstack11ll1ll1_opy_ = CONFIG[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪഠ")][bstack1lll1l1_opy_][bstack1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ഡ")]
  logger.debug(bstack1ll1l111_opy_.format(bstack1l11llll_opy_))
def bstack1l11l111_opy_(self, url):
  global bstack1l1l11l_opy_
  try:
    bstack11l1l1l_opy_(url)
  except Exception as err:
    logger.debug(bstack111lll11_opy_.format(str(err)))
  bstack1l1l11l_opy_(self, url)
def bstack1ll1l111l_opy_(self, test):
  global CONFIG
  global bstack1l11llll_opy_
  global bstack1lll1llll_opy_
  global bstack11ll1ll1_opy_
  global bstack1lllll11l_opy_
  if bstack1l11llll_opy_:
    try:
      data = {}
      bstack11l11l_opy_ = None
      if test:
        bstack11l11l_opy_ = str(test.data)
      if bstack11l11l_opy_ and not bstack11ll1ll1_opy_:
        data[bstack1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧഢ")] = bstack11l11l_opy_
      if bstack1lll1llll_opy_:
        if bstack1lll1llll_opy_.status == bstack1l1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨണ"):
          data[bstack1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫത")] = bstack1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬഥ")
        elif bstack1lll1llll_opy_.status == bstack1l1_opy_ (u"࠭ࡆࡂࡋࡏࠫദ"):
          data[bstack1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧധ")] = bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨന")
          if bstack1lll1llll_opy_.message:
            data[bstack1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩഩ")] = str(bstack1lll1llll_opy_.message)
      user = CONFIG[bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬപ")]
      key = CONFIG[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧഫ")]
      url = bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪബ").format(user, key, bstack1l11llll_opy_)
      headers = {
        bstack1l1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬഭ"): bstack1l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪമ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1ll1l1lll_opy_.format(str(e)))
  bstack1lllll11l_opy_(self, test)
def bstack11l111ll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1ll1l11_opy_
  bstack1ll1l11_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1lll1llll_opy_
  bstack1lll1llll_opy_ = self._test
def bstack1l1l1l1l_opy_(outs_dir, options, tests_root_name, stats, copied_artifacts, outputfile=None):
  from pabot import pabot
  outputfile = outputfile or options.get(bstack1l1_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠣയ"), bstack1l1_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵ࠰ࡻࡱࡱࠨര"))
  output_path = os.path.abspath(
    os.path.join(options.get(bstack1l1_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶࡧ࡭ࡷࠨറ"), bstack1l1_opy_ (u"ࠦ࠳ࠨല")), outputfile)
  )
  files = sorted(pabot.glob(os.path.join(pabot._glob_escape(outs_dir), bstack1l1_opy_ (u"ࠧ࠰࠮ࡹ࡯࡯ࠦള"))))
  if not files:
    pabot._write(bstack1l1_opy_ (u"࠭ࡗࡂࡔࡑ࠾ࠥࡔ࡯ࠡࡱࡸࡸࡵࡻࡴࠡࡨ࡬ࡰࡪࡹࠠࡪࡰࠣࠦࠪࡹࠢࠨഴ") % outs_dir, pabot.Color.YELLOW)
    return bstack1l1_opy_ (u"ࠢࠣവ")
  def invalid_xml_callback():
    global _ABNORMAL_EXIT_HAPPENED
    _ABNORMAL_EXIT_HAPPENED = True
  resu = pabot.merge(
    files, options, tests_root_name, copied_artifacts, invalid_xml_callback
  )
  pabot._update_stats(resu, stats)
  resu.save(output_path)
  return output_path
def bstack1l11ll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  from pabot import pabot
  from robot import __version__ as ROBOT_VERSION
  from robot import rebot
  if bstack1l1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧശ") in options:
    del options[bstack1l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨഷ")]
  if ROBOT_VERSION < bstack1l1_opy_ (u"ࠥ࠸࠳࠶ࠢസ"):
    stats = {
      bstack1l1_opy_ (u"ࠦࡨࡸࡩࡵ࡫ࡦࡥࡱࠨഹ"): {bstack1l1_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࠦഺ"): 0, bstack1l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨ഻"): 0, bstack1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪ഼ࠢ"): 0},
      bstack1l1_opy_ (u"ࠣࡣ࡯ࡰࠧഽ"): {bstack1l1_opy_ (u"ࠤࡷࡳࡹࡧ࡬ࠣാ"): 0, bstack1l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥി"): 0, bstack1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦീ"): 0},
    }
  else:
    stats = {
      bstack1l1_opy_ (u"ࠧࡺ࡯ࡵࡣ࡯ࠦു"): 0,
      bstack1l1_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠨൂ"): 0,
      bstack1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢൃ"): 0,
      bstack1l1_opy_ (u"ࠣࡵ࡮࡭ࡵࡶࡥࡥࠤൄ"): 0,
    }
  if pabot_args[bstack1l1_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ൅")]:
    outputs = []
    for index, _ in enumerate(pabot_args[bstack1l1_opy_ (u"ࠥࡆࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡤࡘࡕࡏࠤെ")]):
      copied_artifacts = pabot._copy_output_artifacts(
        options, pabot_args[bstack1l1_opy_ (u"ࠦࡦࡸࡴࡪࡨࡤࡧࡹࡹࠢേ")], pabot_args[bstack1l1_opy_ (u"ࠧࡧࡲࡵ࡫ࡩࡥࡨࡺࡳࡪࡰࡶࡹࡧ࡬࡯࡭ࡦࡨࡶࡸࠨൈ")]
      )
      outputs += [
        bstack1l1l1l1l_opy_(
          os.path.join(outs_dir, str(index)+ bstack1l1_opy_ (u"ࠨ࠯ࠣ൉")),
          options,
          tests_root_name,
          stats,
          copied_artifacts,
          outputfile=os.path.join(bstack1l1_opy_ (u"ࠢࡱࡣࡥࡳࡹࡥࡲࡦࡵࡸࡰࡹࡹࠢൊ"), bstack1l1_opy_ (u"ࠣࡱࡸࡸࡵࡻࡴࠦࡵ࠱ࡼࡲࡲࠢോ") % index),
        )
      ]
    if bstack1l1_opy_ (u"ࠤࡲࡹࡹࡶࡵࡵࠤൌ") not in options:
      options[bstack1l1_opy_ (u"ࠥࡳࡺࡺࡰࡶࡶ്ࠥ")] = bstack1l1_opy_ (u"ࠦࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠣൎ")
    pabot._write_stats(stats)
    return rebot(*outputs, **pabot._options_for_rebot(options, start_time_string, pabot._now()))
  else:
    return pabot._report_results(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1111l1ll_opy_(self, ff_profile_dir):
  global bstack11l1l11l_opy_
  if not ff_profile_dir:
    return None
  return bstack11l1l11l_opy_(self, ff_profile_dir)
def bstack1llll1l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1lll11l1_opy_
  bstack1lll1l11_opy_ = []
  if bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ൏") in CONFIG:
    bstack1lll1l11_opy_ = CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ൐")]
  bstack1l1111l_opy_ = len(suite_group) * len(pabot_args[bstack1l1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢ൑")] or [(bstack1l1_opy_ (u"ࠣࠤ൒"), None)]) * len(bstack1lll1l11_opy_)
  pabot_args[bstack1l1_opy_ (u"ࠤࡅࡗ࡙ࡇࡃࡌࡡࡓࡅࡗࡇࡌࡍࡇࡏࡣࡗ࡛ࡎࠣ൓")] = []
  for q in range(bstack1l1111l_opy_):
    pabot_args[bstack1l1_opy_ (u"ࠥࡆࡘ࡚ࡁࡄࡍࡢࡔࡆࡘࡁࡍࡎࡈࡐࡤࡘࡕࡏࠤൔ")].append(str(q))
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1l1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧൕ")],
      pabot_args[bstack1l1_opy_ (u"ࠧࡼࡥࡳࡤࡲࡷࡪࠨൖ")],
      argfile,
      pabot_args.get(bstack1l1_opy_ (u"ࠨࡨࡪࡸࡨࠦൗ")),
      pabot_args[bstack1l1_opy_ (u"ࠢࡱࡴࡲࡧࡪࡹࡳࡦࡵࠥ൘")],
      platform[0],
      bstack1lll11l1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1l1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡩ࡭ࡱ࡫ࡳࠣ൙")] or [(bstack1l1_opy_ (u"ࠤࠥ൚"), None)]
    for platform in enumerate(bstack1lll1l11_opy_)
  ]
def bstack1ll1l11l_opy_(self, datasources, outs_dir, options,
  execution_item, command, verbose, argfile,
  hive=None, processes=0,platform_index=0,bstack1l1ll1_opy_=bstack1l1_opy_ (u"ࠪࠫ൛")):
  global bstack1lll11l_opy_
  self.platform_index = platform_index
  self.bstack1lll1ll_opy_ = bstack1l1ll1_opy_
  bstack1lll11l_opy_(self, datasources, outs_dir, options,
    execution_item, command, verbose, argfile, hive, processes)
def bstack11l11l1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1lllll1ll_opy_
  if not bstack1l1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭൜") in item.options:
    item.options[bstack1l1_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ൝")] = []
  for v in item.options[bstack1l1_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ൞")]:
    if bstack1l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭ൟ") in v:
      item.options[bstack1l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪൠ")].remove(v)
  item.options[bstack1l1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫൡ")].insert(0, bstack1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬൢ").format(item.platform_index))
  item.options[bstack1l1_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭ൣ")].insert(0, bstack1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓ࠼ࡾࢁࠬ൤").format(item.bstack1lll1ll_opy_))
  return bstack1lllll1ll_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack111ll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1ll1lll11_opy_
  command[0] = command[0].replace(bstack1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൥"), bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠳ࡳࡥ࡭ࠣࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫ൦"), 1)
  return bstack1ll1lll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1ll1l1ll1_opy_(self, runner, quiet=False, capture=True):
  global bstack1l1l111l_opy_
  bstack11111l1_opy_ = bstack1l1l111l_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1l1_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࡣࡦࡸࡲࠨ൧")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1l1_opy_ (u"ࠩࡨࡼࡨࡥࡴࡳࡣࡦࡩࡧࡧࡣ࡬ࡡࡤࡶࡷ࠭൨")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack11111l1_opy_
def bstack1lll1lll1_opy_(self, name, context, *args):
  global bstack1l1l1l1_opy_
  if name in [bstack1l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠫ൩"), bstack1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭൪")]:
    bstack1l1l1l1_opy_(self, name, context, *args)
  if name == bstack1l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭൫"):
    try:
      bstack1l1lll11_opy_ = str(self.feature.name)
      context.browser.execute_script(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ൬") + json.dumps(bstack1l1lll11_opy_) + bstack1l1_opy_ (u"ࠧࡾࡿࠪ൭"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ൮").format(str(e)))
  if name == bstack1l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ൯"):
    try:
      if not hasattr(self, bstack1l1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ൰")):
        self.driver_before_scenario = True
      bstack1l1lll1_opy_ = args[0].name
      bstack1l11111_opy_ = bstack1l1lll11_opy_ = str(self.feature.name)
      bstack1l1lll11_opy_ = bstack1l11111_opy_ + bstack1l1_opy_ (u"ࠫࠥ࠳ࠠࠨ൱") + bstack1l1lll1_opy_
      if self.driver_before_scenario:
        context.browser.execute_script(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ൲") + json.dumps(bstack1l1lll11_opy_) + bstack1l1_opy_ (u"࠭ࡽࡾࠩ൳"))
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨ൴").format(str(e)))
  if name == bstack1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ൵"):
    try:
      bstack1ll11ll_opy_ = args[0].status.name
      if str(bstack1ll11ll_opy_).lower() == bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ൶"):
        bstack11ll11l_opy_ = bstack1l1_opy_ (u"ࠪࠫ൷")
        bstack111l1l1l_opy_ = bstack1l1_opy_ (u"ࠫࠬ൸")
        bstack1llll1111_opy_ = bstack1l1_opy_ (u"ࠬ࠭൹")
        try:
          import traceback
          bstack11ll11l_opy_ = self.exception.__class__.__name__
          bstack1ll1ll11l_opy_ = traceback.format_tb(self.exc_traceback)
          bstack111l1l1l_opy_ = bstack1l1_opy_ (u"࠭ࠠࠨൺ").join(bstack1ll1ll11l_opy_)
          bstack1llll1111_opy_ = bstack1ll1ll11l_opy_[-1]
        except Exception as e:
          logger.debug(bstack111llll_opy_.format(str(e)))
        bstack11ll11l_opy_ += bstack1llll1111_opy_
        context.browser.execute_script(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬൻ") + json.dumps(str(args[0].name) + bstack1l1_opy_ (u"ࠣࠢ࠰ࠤࡋࡧࡩ࡭ࡧࡧࠥࡡࡴࠢർ") + str(bstack111l1l1l_opy_)) + bstack1l1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩൽ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡶࡸࡦࡺࡵࡴࠤ࠽ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ࠱ࠦࠢࡳࡧࡤࡷࡴࡴࠢ࠻ࠢࠪൾ") + json.dumps(bstack1l1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣൿ") + str(bstack11ll11l_opy_)) + bstack1l1_opy_ (u"ࠬࢃࡽࠨ඀"))
      else:
        context.browser.execute_script(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫඁ") + json.dumps(str(args[0].name) + bstack1l1_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦං")) + bstack1l1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧඃ"))
        if self.driver_before_scenario:
          context.browser.execute_script(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡵࡷࡥࡹࡻࡳࠣ࠼ࠥࡴࡦࡹࡳࡦࡦࠥࢁࢂ࠭඄"))
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬඅ").format(str(e)))
  if name == bstack1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡪࡪࡧࡴࡶࡴࡨࠫආ"):
    try:
      if context.failed is True:
        bstack1ll1lll1l_opy_ = []
        bstack1lll1l1l_opy_ = []
        bstack1lll1l111_opy_ = []
        bstack1lll1l1l1_opy_ = bstack1l1_opy_ (u"ࠬ࠭ඇ")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1ll1lll1l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll1ll11l_opy_ = traceback.format_tb(exc_tb)
            bstack1ll11lll_opy_ = bstack1l1_opy_ (u"࠭ࠠࠨඈ").join(bstack1ll1ll11l_opy_)
            bstack1lll1l1l_opy_.append(bstack1ll11lll_opy_)
            bstack1lll1l111_opy_.append(bstack1ll1ll11l_opy_[-1])
        except Exception as e:
          logger.debug(bstack111llll_opy_.format(str(e)))
        bstack11ll11l_opy_ = bstack1l1_opy_ (u"ࠧࠨඉ")
        for i in range(len(bstack1ll1lll1l_opy_)):
          bstack11ll11l_opy_ += bstack1ll1lll1l_opy_[i] + bstack1lll1l111_opy_[i] + bstack1l1_opy_ (u"ࠨ࡞ࡱࠫඊ")
        bstack1lll1l1l1_opy_ = bstack1l1_opy_ (u"ࠩࠣࠫඋ").join(bstack1lll1l1l_opy_)
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨඌ") + json.dumps(bstack1lll1l1l1_opy_) + bstack1l1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫඍ"))
          context.browser.execute_script(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡦࡢ࡫࡯ࡩࡩࠨࠬࠡࠤࡵࡩࡦࡹ࡯࡯ࠤ࠽ࠤࠬඎ") + json.dumps(bstack1l1_opy_ (u"ࠨࡓࡰ࡯ࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡹࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡞ࡱࠦඏ") + str(bstack11ll11l_opy_)) + bstack1l1_opy_ (u"ࠧࡾࡿࠪඐ"))
      else:
        if not self.driver_before_scenario:
          context.browser.execute_script(bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭එ") + json.dumps(bstack1l1_opy_ (u"ࠤࡉࡩࡦࡺࡵࡳࡧ࠽ࠤࠧඒ") + str(self.feature.name) + bstack1l1_opy_ (u"ࠥࠤࡵࡧࡳࡴࡧࡧࠥࠧඓ")) + bstack1l1_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪඔ"))
          context.browser.execute_script(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡸࡺࡡࡵࡷࡶࠦ࠿ࠨࡰࡢࡵࡶࡩࡩࠨࡽࡾࠩඕ"))
    except Exception as e:
      logger.debug(bstack1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨඖ").format(str(e)))
  if name in [bstack1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ඗"), bstack1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠩ඘")]:
    bstack1l1l1l1_opy_(self, name, context, *args)
def bstack111ll1l1_opy_(bstack1ll1l1_opy_):
  global bstack1l11lll1_opy_
  bstack1l11lll1_opy_ = bstack1ll1l1_opy_
  logger.info(bstack1111ll1l_opy_.format(bstack1l11lll1_opy_.split(bstack1l1_opy_ (u"ࠩ࠰ࠫ඙"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1lll1ll11_opy_(e, bstack1lllll1l_opy_)
  Service.start = bstack1ll11llll_opy_
  Service.stop = bstack1l1l11l1_opy_
  webdriver.Remote.__init__ = bstack1ll1l1l11_opy_
  webdriver.Remote.get = bstack1l11l111_opy_
  WebDriver.close = bstack11l1l1l1_opy_
  if (bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩක") in str(bstack1ll1l1_opy_).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack1ll111l1_opy_)
    Output.end_test = bstack1ll1l111l_opy_
    TestStatus.__init__ = bstack11l111ll_opy_
    WebDriverCreator._get_ff_profile = bstack1111l1ll_opy_
    QueueItem.__init__ = bstack1ll1l11l_opy_
    pabot._create_items = bstack1llll1l1_opy_
    pabot._run = bstack111ll1l_opy_
    pabot._create_command_for_execution = bstack11l11l1_opy_
    pabot._report_results = bstack1l11ll_opy_
  if bstack1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫඛ") in str(bstack1ll1l1_opy_).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack111111l_opy_)
    Runner.run_hook = bstack1lll1lll1_opy_
    Step.run = bstack1ll1l1ll1_opy_
def bstack11l111l1_opy_():
  global CONFIG
  if bstack1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬග") in CONFIG and int(CONFIG[bstack1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ඝ")]) > 1:
    logger.warn(bstack1lllll11_opy_)
def bstack1l11ll11_opy_(bstack1llll111_opy_, index):
  bstack111ll1l1_opy_(bstack1l111_opy_)
  exec(open(bstack1llll111_opy_).read())
def bstack11ll1l_opy_(arg):
  global CONFIG
  bstack111ll1l1_opy_(bstack1l1ll_opy_)
  os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨඞ")] = CONFIG[bstack1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪඟ")]
  os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬච")] = CONFIG[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ඡ")]
  from _pytest.config import main as bstack11111111_opy_
  bstack11111111_opy_(arg)
def bstack1llll1ll1_opy_(arg):
  bstack111ll1l1_opy_(bstack1lll1l_opy_)
  from behave.__main__ import main as bstack1ll1111_opy_
  bstack1ll1111_opy_(arg)
def bstack1lll11l1l_opy_():
  logger.info(bstack11ll1ll_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪජ"), help=bstack1l1_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ඣ"))
  parser.add_argument(bstack1l1_opy_ (u"࠭࠭ࡶࠩඤ"), bstack1l1_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫඥ"), help=bstack1l1_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧඦ"))
  parser.add_argument(bstack1l1_opy_ (u"ࠩ࠰࡯ࠬට"), bstack1l1_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩඨ"), help=bstack1l1_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬඩ"))
  parser.add_argument(bstack1l1_opy_ (u"ࠬ࠳ࡦࠨඪ"), bstack1l1_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫණ"), help=bstack1l1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ඬ"))
  bstack1ll1ll1l1_opy_ = parser.parse_args()
  try:
    bstack1l111l11_opy_ = bstack1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬත")
    if bstack1ll1ll1l1_opy_.framework and bstack1ll1ll1l1_opy_.framework not in (bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩථ"), bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫද")):
      bstack1l111l11_opy_ = bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪධ")
    bstack1lll1ll1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1l111l11_opy_)
    bstack1lll111l_opy_ = open(bstack1lll1ll1l_opy_, bstack1l1_opy_ (u"ࠬࡸࠧන"))
    bstack1111lll_opy_ = bstack1lll111l_opy_.read()
    bstack1lll111l_opy_.close()
    if bstack1ll1ll1l1_opy_.username:
      bstack1111lll_opy_ = bstack1111lll_opy_.replace(bstack1l1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭඲"), bstack1ll1ll1l1_opy_.username)
    if bstack1ll1ll1l1_opy_.key:
      bstack1111lll_opy_ = bstack1111lll_opy_.replace(bstack1l1_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩඳ"), bstack1ll1ll1l1_opy_.key)
    if bstack1ll1ll1l1_opy_.framework:
      bstack1111lll_opy_ = bstack1111lll_opy_.replace(bstack1l1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩප"), bstack1ll1ll1l1_opy_.framework)
    file_name = bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬඵ")
    file_path = os.path.abspath(file_name)
    bstack1lll1l11l_opy_ = open(file_path, bstack1l1_opy_ (u"ࠪࡻࠬබ"))
    bstack1lll1l11l_opy_.write(bstack1111lll_opy_)
    bstack1lll1l11l_opy_.close()
    logger.info(bstack1l1llll_opy_)
  except Exception as e:
    logger.error(bstack1lll1lll_opy_.format(str(e)))
def bstack1ll1llll1_opy_():
  global CONFIG
  if bool(CONFIG):
    return
  bstack11l1111_opy_()
  logger.debug(bstack1ll1ll_opy_.format(str(CONFIG)))
  bstack1ll1ll1ll_opy_()
  atexit.register(bstack111lll1l_opy_)
  signal.signal(signal.SIGINT, bstack1ll1l1l1_opy_)
  signal.signal(signal.SIGTERM, bstack1ll1l1l1_opy_)
def bstack1111ll1_opy_(bstack11ll11ll_opy_, size):
  bstack11111ll_opy_ = []
  while len(bstack11ll11ll_opy_) > size:
    bstack111l111_opy_ = bstack11ll11ll_opy_[:size]
    bstack11111ll_opy_.append(bstack111l111_opy_)
    bstack11ll11ll_opy_   = bstack11ll11ll_opy_[size:]
  bstack11111ll_opy_.append(bstack11ll11ll_opy_)
  return bstack11111ll_opy_
def run_on_browserstack():
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1ll11l_opy_)
    return
  if sys.argv[1] == bstack1l1_opy_ (u"ࠫ࠲࠳ࡶࡦࡴࡶ࡭ࡴࡴࠧභ")  or sys.argv[1] == bstack1l1_opy_ (u"ࠬ࠳ࡶࠨම"):
    logger.info(bstack1l1_opy_ (u"࠭ࡂࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡖࡹࡵࡪࡲࡲ࡙ࠥࡄࡌࠢࡹࡿࢂ࠭ඹ").format(__version__))
    return
  if sys.argv[1] == bstack1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ය"):
    bstack1lll11l1l_opy_()
    return
  args = sys.argv
  bstack1ll1llll1_opy_()
  global CONFIG
  global bstack1l1111l1_opy_
  global bstack1l1ll1l1_opy_
  global bstack1l11l1l1_opy_
  global bstack1lll11l1_opy_
  bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠨࠩර")
  if args[1] == bstack1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ඼") or args[1] == bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫල"):
    bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ඾")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ඿"):
    bstack11llll1l_opy_ = bstack1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬව")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ශ"):
    bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧෂ")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪස"):
    bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫහ")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫළ"):
    bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬෆ")
    args = args[2:]
  elif args[1] == bstack1l1_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭෇"):
    bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ෈")
    args = args[2:]
  else:
    if not bstack1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෉") in CONFIG or str(CONFIG[bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯්ࠬ")]).lower() in [bstack1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ෋"), bstack1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ෌")]:
      bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ෍")
      args = args[1:]
    elif str(CONFIG[bstack1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ෎")]).lower() == bstack1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ා"):
      bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧැ")
      args = args[1:]
    elif str(CONFIG[bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬෑ")]).lower() == bstack1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩි"):
      bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪී")
      args = args[1:]
    elif str(CONFIG[bstack1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨු")]).lower() == bstack1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭෕"):
      bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧූ")
      args = args[1:]
    elif str(CONFIG[bstack1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ෗")]).lower() == bstack1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩෘ"):
      bstack11llll1l_opy_ = bstack1l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪෙ")
      args = args[1:]
    else:
      bstack111lll_opy_(bstack1111l11_opy_)
  global bstack1111llll_opy_
  global bstack1lllll11l_opy_
  global bstack1ll1l11_opy_
  global bstack11l1l11l_opy_
  global bstack1ll1lll11_opy_
  global bstack1lll11l_opy_
  global bstack1lllll1ll_opy_
  global bstack11l1l1_opy_
  global bstack1l1l1l1_opy_
  global bstack1l1l111l_opy_
  global bstack1l1l11l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
  except Exception as e:
    bstack1lll1ll11_opy_(e, bstack1lllll1l_opy_)
  bstack1111llll_opy_ = webdriver.Remote.__init__
  bstack11l1l1_opy_ = WebDriver.close
  bstack1l1l11l_opy_ = WebDriver.get
  if (bstack11llll1l_opy_ in [bstack1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪේ"), bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫෛ"), bstack1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧො")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
      from pabot.pabot import QueueItem
      from pabot import pabot
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack1ll111l1_opy_)
    bstack1lllll11l_opy_ = Output.end_test
    bstack1ll1l11_opy_ = TestStatus.__init__
    bstack11l1l11l_opy_ = WebDriverCreator._get_ff_profile
    bstack1ll1lll11_opy_ = pabot._run
    bstack1lll11l_opy_ = QueueItem.__init__
    bstack1lllll1ll_opy_ = pabot._create_command_for_execution
  if bstack11llll1l_opy_ == bstack1l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧෝ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack111111l_opy_)
    bstack1l1l1l1_opy_ = Runner.run_hook
    bstack1l1l111l_opy_ = Step.run
  if bstack11llll1l_opy_ == bstack1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨෞ"):
    bstack11l1ll1_opy_()
    bstack11l111l1_opy_()
    if bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬෟ") in CONFIG:
      bstack1l1ll1l1_opy_ = True
      bstack1l1l1111_opy_ = []
      for index, platform in enumerate(CONFIG[bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෠")]):
        bstack1l1l1111_opy_.append(threading.Thread(name=str(index),
                                      target=bstack1l11ll11_opy_, args=(args[0], index)))
      for t in bstack1l1l1111_opy_:
        t.start()
      for t in bstack1l1l1111_opy_:
        t.join()
    else:
      bstack111ll1l1_opy_(bstack1l111_opy_)
      exec(open(args[0]).read())
  elif bstack11llll1l_opy_ == bstack1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ෡") or bstack11llll1l_opy_ == bstack1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ෢"):
    try:
      from pabot import pabot
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack1ll111l1_opy_)
    bstack11l1ll1_opy_()
    bstack111ll1l1_opy_(bstack1l11l_opy_)
    if bstack1l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ෣") in args:
      i = args.index(bstack1l1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ෤"))
      args.pop(i)
      args.pop(i)
    args.insert(0, str(bstack1l1111l1_opy_))
    args.insert(0, str(bstack1l1_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭෥")))
    pabot.main(args)
  elif bstack11llll1l_opy_ == bstack1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ෦"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack1ll111l1_opy_)
    for a in args:
      if bstack1l1_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ෧") in a:
        bstack1l11l1l1_opy_ = int(a.split(bstack1l1_opy_ (u"ࠫ࠿࠭෨"))[1])
      if bstack1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ෩") in a:
        bstack1lll11l1_opy_ = str(a.split(bstack1l1_opy_ (u"࠭࠺ࠨ෪"))[1])
    bstack111ll1l1_opy_(bstack1l11l_opy_)
    run_cli(args)
  elif bstack11llll1l_opy_ == bstack1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ෫"):
    try:
      from _pytest.config import _prepareconfig
      import importlib
      bstack1llll111l_opy_ = importlib.find_loader(bstack1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪ෬"))
      if bstack1llll111l_opy_ is None:
        bstack1lll1ll11_opy_(e, bstack1l111ll_opy_)
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack1l111ll_opy_)
    bstack11l1ll1_opy_()
    try:
      if bstack1l1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫ෭") in args:
        i = args.index(bstack1l1_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ෮"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1_opy_ (u"ࠫ࠲࠳࡮ࡶ࡯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ෯") in args:
        i = args.index(bstack1l1_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭෰"))
        args.pop(i+1)
        args.pop(i)
      if bstack1l1_opy_ (u"࠭࠭࡯ࠩ෱") in args:
        i = args.index(bstack1l1_opy_ (u"ࠧ࠮ࡰࠪෲ"))
        args.pop(i+1)
        args.pop(i)
    except Exception as exc:
      logger.error(str(exc))
    config = _prepareconfig(args)
    bstack1lllllll1_opy_ = config.args
    bstack11ll1lll_opy_ = config.invocation_params.args
    bstack11ll1lll_opy_ = list(bstack11ll1lll_opy_)
    bstack111l1l1_opy_ = []
    for arg in bstack11ll1lll_opy_:
      if arg not in bstack1lllllll1_opy_:
        bstack111l1l1_opy_.append(arg)
    bstack111l1l1_opy_.append(bstack1l1_opy_ (u"ࠨ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠪෳ"))
    bstack111l1l1_opy_.append(bstack1l1_opy_ (u"ࠩࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠨ෴"))
    bstack11111l_opy_ = []
    for spec in bstack1lllllll1_opy_:
      bstack11l1ll11_opy_ = []
      bstack11l1ll11_opy_.append(spec)
      bstack11l1ll11_opy_ += bstack111l1l1_opy_
      bstack11111l_opy_.append(bstack11l1ll11_opy_)
    bstack1l1ll1l1_opy_ = True
    bstack11ll11_opy_ = 1
    if bstack1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෵") in CONFIG:
      bstack11ll11_opy_ = CONFIG[bstack1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෶")]
    bstack1lll11ll_opy_ = int(bstack11ll11_opy_)*int(len(CONFIG[bstack1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෷")]))
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෸")]):
      for bstack11l1ll11_opy_ in bstack11111l_opy_:
        item = {}
        item[bstack1l1_opy_ (u"ࠧࡢࡴࡪࠫ෹")] = bstack11l1ll11_opy_
        item[bstack1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ෺")] = index
        execution_items.append(item)
    bstack1ll11ll1_opy_ = bstack1111ll1_opy_(execution_items, bstack1lll11ll_opy_)
    for execution_item in bstack1ll11ll1_opy_:
      bstack1l1l1111_opy_ = []
      for item in execution_item:
        bstack1l1l1111_opy_.append(threading.Thread(name=str(item[bstack1l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ෻")]),
                                            target=bstack11ll1l_opy_,
                                            args=(item[bstack1l1_opy_ (u"ࠪࡥࡷ࡭ࠧ෼")],)))
      for t in bstack1l1l1111_opy_:
        t.start()
      for t in bstack1l1l1111_opy_:
        t.join()
  elif bstack11llll1l_opy_ == bstack1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ෽"):
    try:
      from behave.__main__ import main as bstack1ll1111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1lll1ll11_opy_(e, bstack111111l_opy_)
    bstack11l1ll1_opy_()
    bstack1l1ll1l1_opy_ = True
    bstack11ll11_opy_ = 1
    if bstack1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෾") in CONFIG:
      bstack11ll11_opy_ = CONFIG[bstack1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭෿")]
    bstack1lll11ll_opy_ = int(bstack11ll11_opy_)*int(len(CONFIG[bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ฀")]))
    config = Configuration(args)
    bstack1lllllll1_opy_ = config.paths
    bstack1llll11_opy_ = []
    for arg in args:
      if arg not in bstack1lllllll1_opy_:
        bstack1llll11_opy_.append(arg)
    bstack11111l_opy_ = []
    for spec in bstack1lllllll1_opy_:
      bstack11l1ll11_opy_ = []
      bstack11l1ll11_opy_ += bstack1llll11_opy_
      bstack11l1ll11_opy_.append(spec)
      bstack11111l_opy_.append(bstack11l1ll11_opy_)
    execution_items = []
    for index, _ in enumerate(CONFIG[bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫก")]):
      for bstack11l1ll11_opy_ in bstack11111l_opy_:
        item = {}
        item[bstack1l1_opy_ (u"ࠩࡤࡶ࡬࠭ข")] = bstack1l1_opy_ (u"ࠪࠤࠬฃ").join(bstack11l1ll11_opy_)
        item[bstack1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪค")] = index
        execution_items.append(item)
    bstack1ll11ll1_opy_ = bstack1111ll1_opy_(execution_items, bstack1lll11ll_opy_)
    for execution_item in bstack1ll11ll1_opy_:
      bstack1l1l1111_opy_ = []
      for item in execution_item:
        bstack1l1l1111_opy_.append(threading.Thread(name=str(item[bstack1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫฅ")]),
                                            target=bstack1llll1ll1_opy_,
                                            args=(item[bstack1l1_opy_ (u"࠭ࡡࡳࡩࠪฆ")],)))
      for t in bstack1l1l1111_opy_:
        t.start()
      for t in bstack1l1l1111_opy_:
        t.join()
  else:
    bstack111lll_opy_(bstack1111l11_opy_)
  bstack11llll1_opy_()
def bstack11llll1_opy_():
  global CONFIG
  try:
    if bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪง") in CONFIG:
      host = bstack1l1_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫจ") if bstack1l1_opy_ (u"ࠩࡤࡴࡵ࠭ฉ") in CONFIG else bstack1l1_opy_ (u"ࠪࡥࡵ࡯ࠧช")
      user = CONFIG[bstack1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ซ")]
      key = CONFIG[bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨฌ")]
      bstack11l11l11_opy_ = bstack1l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬญ") if bstack1l1_opy_ (u"ࠧࡢࡲࡳࠫฎ") in CONFIG else bstack1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪฏ")
      url = bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩฐ").format(user, key, host, bstack11l11l11_opy_)
      headers = {
        bstack1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩฑ"): bstack1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧฒ"),
      }
      if bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧณ") in CONFIG:
        params = {bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫด"):CONFIG[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪต")], bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫถ"):CONFIG[bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫท")]}
      else:
        params = {bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨธ"):CONFIG[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧน")]}
      response = requests.get(url, params=params, headers=headers)
      if response.json():
        bstack1llllll_opy_ = response.json()[0][bstack1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨบ")]
        if bstack1llllll_opy_:
          bstack1l1ll111_opy_ = bstack1llllll_opy_[bstack1l1_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪป")].split(bstack1l1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ผ"))[0] + bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩฝ") + bstack1llllll_opy_[bstack1l1_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬพ")]
          logger.info(bstack11l1ll_opy_.format(bstack1l1ll111_opy_))
          bstack1111l1_opy_ = CONFIG[bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ฟ")]
          if bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ภ") in CONFIG:
            bstack1111l1_opy_ += bstack1l1_opy_ (u"ࠬࠦࠧม") + CONFIG[bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨย")]
          if bstack1111l1_opy_!= bstack1llllll_opy_[bstack1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬร")]:
            logger.debug(bstack11111l1l_opy_.format(bstack1llllll_opy_[bstack1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ฤ")], bstack1111l1_opy_))
    else:
      logger.warn(bstack111ll11_opy_)
  except Exception as e:
    logger.debug(bstack1ll1l1l1l_opy_.format(str(e)))
def bstack11l1l1l_opy_(url):
  global CONFIG
  global bstack11ll11l1_opy_
  if not bstack11ll11l1_opy_:
    hostname = bstack1llll1l11_opy_(url)
    is_private = bstack1111111_opy_(hostname)
    if not bstack11l1l11_opy_(CONFIG) and is_private:
      bstack11ll11l1_opy_ = hostname
def bstack1llll1l11_opy_(url):
  return urlparse(url).hostname
def bstack1111111_opy_(hostname):
  for bstack1l11l1l_opy_ in bstack1lll1_opy_:
    regex = re.compile(bstack1l11l1l_opy_)
    if regex.match(hostname):
      return True
  return False