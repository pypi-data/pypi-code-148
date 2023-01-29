from selenium.common.exceptions import NoSuchElementException
import logging

target_cache = {}


def find_element( driver, target, targets = None ):
    """find an element in the page"""

    if target in target_cache:
        target = target_cache[ target ]

    if target.startswith( 'link=' ):
        try:
            return driver.find_element_by_link_text( target[ 5 : ] )

        except NoSuchElementException:
            # try lowercase version of link, work around text-transform bug
            result = driver.find_element_by_link_text(target[5:].lower())
            target_cache[target] = 'link=' + target[5:].lower()
            msg = '   label %s is being cached as %s'
            logging.info( msg, target, target_cache[ target ] )
            return result

    elif target.startswith( 'linkText=' ):
        try:
            return driver.find_element_by_link_text( target[ 9 : ] )

        except NoSuchElementException:
            # try lowercase version of link, work around text-transform bug
            result = driver.find_element_by_link_text(target[5:].lower())
            target_cache[target] = 'link=' + target[5:].lower()
            msg = '   label %s is being cached as %s'
            logging.info( msg, target, target_cache[ target ] )
            return result

    elif target.startswith( '//' ):
        return driver.find_element_by_xpath(target)

    elif target.startswith( 'xpath=' ):
        return driver.find_element_by_xpath(target[6:])

    elif target.startswith( 'css=' ):
        return driver.find_element_by_css_selector(target[4:])

    elif target.startswith( 'id=' ):
        return driver.find_element_by_id(target[3:])

    elif target.startswith( 'name=' ):
        return driver.find_element_by_name(target[5:])

    direct = (
            driver.find_element_by_name( target ) or
            driver.find_element_by_id( target ) or
            driver.find_element_by_link_text( target )
    )
    if not direct:
        raise Exception('Don\'t know how to find %s' % target)

    return direct
