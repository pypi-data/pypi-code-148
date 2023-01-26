# Copyright 2019-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import collections

Repo = collections.namedtuple(
    'Repo', 'nickname package_name git_repo settings_module front_end internal_deps public_url')
REPOS_DICT = {}
KNOWN_REPOS = []

def add(nickname, package_name, git_repo='', settings_module='', front_end='', internal_deps=[], public_url=''):
    if isinstance(internal_deps, str):
        internal_deps = internal_deps.split()
    t = Repo(nickname, package_name, git_repo, settings_module, front_end, internal_deps, public_url)
    KNOWN_REPOS.append(t)
    REPOS_DICT[t.nickname] = t
    if t.front_end:
        # add an alias because front ends are looked up using their full package name
        REPOS_DICT[t.front_end] = t

# tools to be installed with --clone because they are required for a complete contributor environment:
add("synodal", "synodal", "https://gitlab.com/lino-framework/synodal")

add("atelier", "atelier", "https://gitlab.com/lino-framework/atelier", public_url='https://atelier.lino-framework.org')
add("rstgen", "rstgen", "https://github.com/lino-framework/rstgen")
add("etgen", "etgen", "https://github.com/lino-framework/etgen")
add("eid", "eidreader", "https://github.com/lino-framework/eidreader")

add("cd", "commondata", "https://github.com/lsaffre/commondata")
add("be", "commondata.be", "https://github.com/lsaffre/commondata-be")
add("ee", "commondata.ee", "https://github.com/lsaffre/commondata-ee")
add("eg", "commondata.eg", "https://github.com/lsaffre/commondata-eg")

add("getlino", "getlino", "https://gitlab.com/lino-framework/getlino")
add("lino", "lino", "https://gitlab.com/lino-framework/lino", "", "lino.modlib.extjs")
add("xl", "lino-xl", "https://gitlab.com/lino-framework/xl")
add("welfare", "lino-welfare", "https://gitlab.com/lino-framework/welfare")

add("amici", "lino-amici", "https://gitlab.com/lino-framework/amici", "lino_amici.lib.amici.settings", internal_deps="lino xl")
add("avanti", "lino-avanti", "https://gitlab.com/lino-framework/avanti", "lino_avanti.lib.avanti.settings", internal_deps="lino xl")
add("cms", "lino-cms", "https://gitlab.com/lino-framework/cms", "lino_cms.lib.cms.settings", internal_deps="lino xl")
add("care", "lino-care", "https://gitlab.com/lino-framework/care", "lino_care.lib.care.settings", internal_deps="lino xl")
add("cosi", "lino-cosi", "https://gitlab.com/lino-framework/cosi", "lino_cosi.lib.cosi.settings", internal_deps="lino xl")
add("mentori", "lino-mentori", "https://gitlab.com/lino-framework/mentori", "lino_mentori.lib.mentori.settings", internal_deps="lino xl")
add("noi", "lino-noi", "https://gitlab.com/lino-framework/noi", "lino_noi.lib.noi.settings", internal_deps="lino xl")
add("presto", "lino-presto", "https://gitlab.com/lino-framework/presto", "lino_presto.lib.presto.settings", internal_deps="lino xl")
add("pronto", "lino-pronto", "https://gitlab.com/lino-framework/pronto", "lino_pronto.lib.pronto.settings", internal_deps="lino xl")
add("tera", "lino-tera", "https://gitlab.com/lino-framework/tera", "lino_tera.lib.tera.settings", internal_deps="lino xl")
add("shop", "lino-shop", "https://gitlab.com/lino-framework/shop", "lino_shop.lib.shop.settings", internal_deps="lino xl")
add("vilma", "lino-vilma", "https://gitlab.com/lino-framework/vilma", "lino_vilma.lib.vilma.settings", internal_deps="lino xl")
add("voga", "lino-voga", "https://gitlab.com/lino-framework/voga", "lino_voga.lib.voga.settings", internal_deps="lino xl")
add("weleup", "lino-weleup", "https://gitlab.com/lino-framework/weleup", "lino_weleup.settings", internal_deps="lino xl")
add("welcht", "lino-welcht", "https://gitlab.com/lino-framework/welcht", "lino_welcht.settings", internal_deps="lino xl")
# add("ciao", "lino-ciao", "https://github.com/lino-framework/ciao", "lino_ciao.lib.ciao.settings", internal_deps="lino xl")

add("react", "lino-react", "https://gitlab.com/lino-framework/react", "", "lino_react.react")
add("openui5", "lino-openui5", "https://gitlab.com/lino-framework/openui5", "", "lino_openui5.openui5")

add("book", "lino-book", "https://gitlab.com/lino-framework/book", public_url='https://dev.lino-framework.org/')
add("cg", "", "https://gitlab.com/lino-framework/cg", public_url='https://community.lino-framework.org/')
add("ug", "", "https://gitlab.com/lino-framework/ug", public_url='https://using.lino-framework.org/')
add("hg", "", "https://gitlab.com/lino-framework/hg", public_url='https://hosting.lino-framework.org/')
add("lf", "", "https://gitlab.com/lino-framework/lf", public_url='https://www.lino-framework.org/')
add("ss", "", "https://gitlab.com/synodalsoft/www", public_url='https://www.synodalsoft.net/')

add("algus", "", "https://gitlab.com/lino-framework/algus")

# experimental: applications that have no repo on their own
add("min1", "", "", "lino_book.projects.min1.settings")
add("min2", "", "", "lino_book.projects.min2.settings")
add("polls", "", "", "lino_book.projects.polls.mysite.settings")
add("cosi_ee", "", "", "lino_book.projects.cosi_ee.settings.demo")
add("lydia", "", "", "lino_book.projects.lydia.settings.demo")
add("noi1e", "", "", "lino_book.projects.noi1e.settings.demo")
add("chatter", "", "", "lino_book.projects.chatter.settings")
add("polly", "", "", "lino_book.projects.polly.settings")

# e.g. for installing a non-Lino site like mailman
add("std", "", "", "lino.projects.std.settings")

APPNAMES = [a.nickname for a in KNOWN_REPOS if a.settings_module]
FRONT_ENDS = [a for a in KNOWN_REPOS if a.front_end]
