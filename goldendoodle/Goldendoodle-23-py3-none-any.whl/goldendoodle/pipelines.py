# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# Typical uses of item pipelines are:
#     cleansing HTML data
#     validating scraped data (checking that the items contain certain fields)
#     checking for duplicates (and dropping them)
#     storing the scraped item in a database


from datetime import datetime

from pickle import NONE

import regex
from genericpath import exists
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from goldendoodle.spiders import items
from goldendoodle.spiders.utils.gldnddl_utils import Gldnddl
import logging

logger = logging.getLogger(__name__)

class GoldendoodlePipeline:
    def process_item(self, item, spider):
        """The final touches are made here.

        Args:
            item (Any): the harvest
            spider (Any): the spider

        Raises:
            DropItem: When the harvest is poor.

        Returns:
            Any: the harvest item

        Example of option=email without gldnddlSearchString:
        ====================================================

        >>> import os
        >>> file = 'reports/findings_50.json'
        >>> if os.path.exists(file):
        ...     os.remove(file)
        >>> url = 'https://model-enact-analyze-manage.de/souverain/index.php/2022/10/29/bang-now-goldendoodle-supports-regular-expressions/'
        >>> os.system(f'''scrapy crawl recherchedechaîne_gldnddl -O {file} -a option=email -a start_urls={url}''')
        0
        >>> import json
        >>> with open(file) as findingsreport:
        ...     for finding in json.load(findingsreport):
        ...         if finding["currentURL"] == url:
        ...             print(str(str(finding['regex_finding']).split(',')[2]).split("'")[1])
        ...             break
        Golden[dot]Doodle[at]chien[dot]fr
                
        """

        adapter = ItemAdapter(item)
        # FUTUREFEATURE supprimer les enregistrements en double (https://doc.scrapy.org/en/latest/topics/item-pipeline.html#duplicates-filter)
        if adapter.get('regex_finding') != 'None' or adapter.get('webdriver_finding') != 'None' or adapter.get('cleared_webdriver_finding') != 'None':
            logger.debug(f"item['currentURL']:{item['currentURL']}:adapter.get('regex_finding'):{adapter.get('regex_finding')}:adapter.get('webdriver_finding'):{adapter.get('webdriver_finding')}:adapter.get('cleared_webdriver_finding'):{adapter.get('cleared_webdriver_finding')}:")
            return item
        else:
            logger.info(
                f"{item['currentURL']} does not include search string:{Gldnddl.search_expression}:")
            raise DropItem(str(datetime.now()) + "I gldnddl ")
