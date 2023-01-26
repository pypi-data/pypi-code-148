'''
Command-line ACME client

Copyright: Copyright 2021-2023 AXY axy@declassed.art
License: BSD, see LICENSE for details.
'''

help = '''
Account management
==================

Create account
--------------

myacme create account ak=my-account-key.pem

Parameters:
* ak: account key filename. If the file does not exists,
      new account key will be generated.
* email: optional contact email
* acme: optional ACME directory URL or predefined constant, default is "le"
  Predefined URLs:
  * le: https://acme-v02.api.letsencrypt.org/directory
  * le-staging: https://acme-staging-v02.api.letsencrypt.org/directory

Update account
--------------

myacme update account ak=my-account-key.pem email=axy@declassed.art

Parameters: same as for create account.

Deactivate account
------------------

myacme deactivate account ak=my-account-key.pem

Certificate management
======================

Apply for certificate issuance
------------------------------

myacme certificate ak=my-account-key.pem \
    dom=declassed.art "dom=*.declassed.art" \
    private-key=declassed.art.key.pem cert=declassed.art.cert.pem

Parameters:
* ak: account key filename
* acme: optional ACME directory URL or predefined constant, default is "le"
* dom: domain names
* private-key: private key for the certificate. If the file does not exists,
    new key will be generated.
* csr: use existing CSR to obtain a certificate. Private key is unnecessary
    if this option is used.
* csr-field: additional CSR fields to include in the certificate.
    By default certificate contains only COMMON_NAME field and SAN extension
    if multiple domains are specified.
    Example:
    "csr-field=Country Name: US"
    "csr-field=State or Province Name: California"
* cert: certificate filename

Automatic certificate management
--------------------------------

myacme manage dir=~/.myacme

myacme deploy dir=~/.myacme

The latter command does deployment step of the former one.

Parameters:
* dir: managed directory, refer to the documentation for the layout
       and configuration.
'''

predefined_directory_urls = {
    'le':         'https://acme-v02.api.letsencrypt.org/directory',
    'le-staging': 'https://acme-staging-v02.api.letsencrypt.org/directory'
}

def main():
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    try:
        if len(kvgargs.group) == 0:
            print(help)
            sys.exit(0)

        action, args = kvgargs.group.popitem(last=False)

        # run action handler
        action_handlers = {
            ('create', 'account'): create_account,
            ('update', 'account'): update_account,
            ('deactivate', 'account'): deactivate_account,
            'certificate': obtain_certificate,
            'manage': manage_certificates,
            'deploy': deploy_certificates,
            'get': get_data_from_saved_state
        }
        if action not in action_handlers:
            print('Wrong action requested:', action if isinstance(action, str) else ' '.join(action), file=sys.stderr)
            sys.exit(1)

        handler = action_handlers[action]
        exit_code = handler(args)
        sys.exit(exit_code)

    except MyAcmeHttpError as e:
        print(e.status, e.error_type, e.detail, file=sys.stderr)
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)

#-----------------------------------------------------------------------------------
# Accounts

def create_account(args):

    acme = _create_acme_client(args)
    if acme is None:
        return 1

    if 'ak' not in args:
        print('Account key is required: ak=<filename>', file=sys.stderr)
        return None

    account_key_filename = os.path.expanduser(args['ak'])
    account_key = _load_or_generate_account_key(acme, account_key_filename)
    if account_key is None:
        return 1
    acme.account_key = account_key

    contacts = _prepare_contacts(args)

    acme.create_account(contacts)
    print('Account created')
    print(acme.account_url)
    return 0

def update_account(args):

    acme = _create_acme_client(args)
    if acme is None:
        return 1

    account_key = _load_account_key(args)
    if account_key is None:
        return 1
    acme.account_key = account_key

    options = ['new-ak', 'email']
    if not any(opt in args for opt in options):
        print(f'One of {", ".join(options[:-1])} or {options[-1]} is required', file=sys.stderr)
        return 1

    if 'new-ak' in args:
        # change account key
        new_account_key_filename = os.path.expanduser(args['new-ak'])
        new_account_key = _load_or_generate_account_key(acme, new_account_key_filename)
        acme.change_account_key(new_account_key)
        print('Account key changed')

    if 'email' in args:
        # change contacts
        contacts = _prepare_contacts(args)
        acme.update_account(contacts)
        print('Account contacts changed')

    return 0

def deactivate_account(args):
    acme = _create_acme_client(args)
    if acme is None:
        return 1
    account_key = _load_account_key(args)
    if account_key is None:
        return 1
    acme.account_key = account_key
    acme.deactivate_account()
    print('Account deactivated')
    return 0

#-----------------------------------------------------------------------------------
# Manual certificate issuance

def obtain_certificate(args):
    if 'cert' not in args:
        print('Certificate file name is required for output: cert=<filename>', file=sys.stderr)
        return 1

    acme = _create_acme_client(args)
    if acme is None:
        return 1

    account_key = _load_account_key(args)
    if account_key is None:
        return 1
    acme.account_key = account_key

    domains = []
    csr = None
    private_key = None

    if 'csr' in args:
        # load csr and get domain names from it
        csr_filename = args['csr']
        if not os.path.exists(csr_filename):
            print('CSR file does not exist:', csr_filename, file=sys.stderr)
            return 1

        if 'dom' in args:
            print('Reading domain names from provided CSR:', csr_filename, file=sys.stderr)
            print('Ignoring provided domin names:', ', '.join(args['dom']), file=sys.stderr)

        with open(csr_filename, 'rb') as f:
            csr = f.read()

        domains = acme.get_domains_from_csr(csr)

    else:
        if 'dom' not in args:
            print('Please provide domain name or names: dom=example.com', file=sys.stderr)
            return 1

        domains = args['dom']

        if 'private-key' not in args:
            print('Please private key file name: private-key=<filename>', file=sys.stderr)
            print('If <filename> already exists, private key will be loaded from that file.', file=sys.stderr)
            print('Otherwise, it will be generated and stored to that file.', file=sys.stderr)
            return 1

        private_key_filename = args['private-key']
        if os.path.exists(private_key_filename):
            with open(private_key_filename, 'rb') as f:
                private_key = f.read()

    csr_fields = _prepare_csr_fields(args)

    authenticator = MyAcmeAuthzManual()
    state = MyAcmeStateFS(domains, '.')  # XXX need state_dir?
    order = acme.process_order(domains, authenticator, state, private_key=private_key, csr=csr, csr_fields=csr_fields)
    if order is None:
        # XXX need to print the reason
        return 1

    if not private_key:
        private_key = order.get_private_key()
        with open(private_key_filename, 'wb') as f:
            f.write(private_key)

    certificate_filename = args['cert']
    certificate = order.get_certificate()
    with open(certificate_filename, 'wb') as f:
        f.write(certificate)

#-----------------------------------------------------------------------------------
# Managed certificate issuance

def manage_certificates(args):
    '''
    Automated certificate management.
    '''
    if 'dir' not in args:
        print('Directory is required: dir=<directory>', file=sys.stderr)
        return 1

    directory = os.path.expanduser(args['dir'])

    config = read_config(directory)
    if config is None:
        return 1

    certs_renewed = 0
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir():
                try:
                    # prepare local config
                    local_config = make_local_config(entry.path, config)
                    # check certificate
                    if is_certificate_expiring(entry.path, local_config):
                        # renew expiring certificate
                        if renew_certificate(entry.path, local_config):
                            certs_renewed += 1
                except Exception:
                    traceback.print_exc()

    if certs_renewed:
        finalization_commands = config.get('finalize', None) or []
        for command in finalization_commands:
            run_command(command)

def deploy_certificates(args):
    '''
    Deploy non-expiring certificates.
    '''
    if 'dir' not in args:
        print('Directory is required: dir=<directory>', file=sys.stderr)
        return 1

    directory = os.path.expanduser(args['dir'])

    config = read_config(directory)
    if config is None:
        return 1

    certs_deployed = 0
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir():
                try:
                    # prepare local config
                    local_config = make_local_config(entry.path, config)
                    # check certificate
                    if not is_certificate_expiring(entry.path, local_config):
                        # deploy certificate
                        deploy_certificate(entry.path, local_config)
                        certs_deployed += 1
                except Exception:
                    traceback.print_exc()

    if certs_deployed:
        for command in config['finalize']:
            run_command(command)

def read_config(directory):
    '''
    Read global configuration for managed `directory`.
    '''
    config_filename = os.path.join(directory, 'config.yaml')
    if not os.path.exists(config_filename):
        print(f'Configuration file is required: {config_filename}', file=sys.stderr)
        return None

    with open(config_filename) as f:
        config = yaml.safe_load(f)

    # set some defaults
    if 'acme' not in config:
        # use Let's Encrypt by default
        config['acme'] = 'le'

    if config['acme'] in predefined_directory_urls:
        config['acme'] = predefined_directory_urls[config['acme']]

    # make account key filename relative to `directory`
    # XXX if redefined in a local configuration, this won't work
    config['account_key'] = os.path.join(directory, config['account_key'])

    return config

def renew_certificate(directory, config):
    '''
    Renew certificate for specific domain.
    Return True on success, False on failure.
    '''
    # create acme client
    acme = MyAcmeClient(config['acme'])

    # check account key
    account_key_filename = config['account_key']
    if not os.path.exists(account_key_filename):
        print('Account key file does not exist:', account_key_filename, file=sys.stderr)
        return False

    # load and set account key
    with open(account_key_filename, 'rb') as f:
        acme.account_key = f.read()

    if len(glob(os.path.join(directory, '*.myacme.json'))) == 0:
        # if no state files exist, this means previous request was successful;
        # move existing files to `previous` subdirectory
        prev_dir = os.path.join(directory, 'previous')
        os.makedirs(prev_dir, exist_ok=True)
        exclude_filenames = set(['config.yaml'])
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file() and entry.name not in exclude_filenames:
                    os.rename(entry.path, os.path.join(prev_dir, entry.name))

    # request new certificate
    authenticator = MyAcmeAuthzScript(config=config['authz'])
    state = MyAcmeStateFS(config['cert_domains'], directory)
    order = acme.process_order(config['cert_domains'], authenticator, state, csr_fields=config['csr_fields'])
    if order is None:
        # XXX need to print the reason
        return False

    # save private key
    private_key = order.get_private_key()
    private_key_filename = os.path.join(directory, config['filenames']['key'])
    with open(private_key_filename, 'wb') as f:
        f.write(private_key)

    # save certificate
    certificate = order.get_certificate()
    certificate_filename = os.path.join(directory, config['filenames']['certificate'])
    with open(certificate_filename, 'wb') as f:
        f.write(certificate)

    # deployment
    deploy_certificate(directory, config)

    # drop state file(s) on success
    for filename in glob(os.path.join(directory, '*.myacme.json')):
        os.remove(filename)

    return True

def make_local_config(directory, global_config):
    '''
    Merge global_config with local configuration, if any.
    Set defaults, process substitutions for filenames and cert_domains.
    '''
    config = global_config.copy()
    config_filename = os.path.join(directory, 'config.yaml')
    if os.path.exists(config_filename):
        with open(config_filename) as f:
            config.update(yaml.safe_load(f))

    # set defaults
    defaults = {
        'filenames': {
            'certificate': '{domain}.cert.pem',
            'key':         '{domain}.key.pem'
        },
        'cert_domains': [
            '{domain}'
        ],
        'csr_fields': {
        },
        'expiring_days': 7,
        'deploy': []
    }
    for k, v in defaults.items():
        config.setdefault(k, v)
    # set defaults for some sub-dicts
    for key in ['filenames']:
        for k, v in defaults[key].items():
            config[key].setdefault(k, v)

    # prepare substitutions
    substitutions = dict(
        domain = os.path.basename(directory)
    )
    # process substitutions in dicts
    for key in ['filenames']:
        config[key] = dict((k, v.format_map(substitutions)) for k, v in config[key].items())
    # process substitutions in lists
    for key in ['cert_domains']:
        config[key] = [v.format_map(substitutions) for v in config[key]]

    return config

def is_certificate_expiring(directory, config):
    '''
    Check if the certificate is expiring.
    '''
    cert_filename = os.path.join(directory, config['filenames']['certificate'])
    if not os.path.exists(cert_filename):
        print(f'{cert_filename} does not exist and will be obtained')
        return True

    with open(cert_filename, 'rb') as f:
        start_date, end_date = get_certificate_validity_period(f.read())

    now = datetime.utcnow()
    if end_date < now + timedelta(days=config['expiring_days']):
        print(f'{cert_filename} is expiring, {max(0, (end_date - now).days)} days left')
        return True
    else:
        print(f'{cert_filename} is not expiring yet, {max(0, (end_date - now).days)} days left')
        return False

def deploy_certificate(directory, config):
    '''
    Prepare substitutions and deploy certificate.
    '''
    domain = os.path.basename(directory)
    substitutions = dict(
        domain = shlex.quote(domain),
        idna_domain = shlex.quote(idna_encode(domain)),
        directory = shlex.quote(directory),
        filenames = dict((k, shlex.quote(v)) for k, v in config['filenames'].items())
    )
    for command in config['deploy']:
        try:
            command = command.format_map(substitutions)
        except Exception:
            logger.error('Failed substitutions: %s', command)
            raise
        run_command(command)

#-----------------------------------------------------------------------------------
# Utilities

def get_data_from_saved_state(args):
    '''
    Extract CSR, private key and certificate from state file
    '''
    raise NotImplementedError('This command is not implemented yet')

#-----------------------------------------------------------------------------------
# Helpers

def _create_acme_client(args):
    '''
    Helper function to  create an ACME client.
    '''
    # get directory URL
    if 'acme' in args:
        directory_url = args['acme']
        if directory_url in predefined_directory_urls:
            directory_url = predefined_directory_urls[directory_url]
    else:
        # use Let's Encrypt by default
        directory_url = predefined_directory_urls['le']

    # create ACME client
    return MyAcmeClient(directory_url)

def _load_or_generate_account_key(acme, account_key_filename):
    '''
    Helper function to create account or change account key.
    '''
    if os.path.exists(account_key_filename):
        # load existing account key
        with open(account_key_filename, 'rb') as f:
            account_key = f.read()
    else:
        # generate account key
        account_key = acme.generate_account_key()
        with open(account_key_filename, 'wb') as f:
            f.write(account_key)
    return account_key

def _load_account_key(args):
    '''
    Helper function for account action handlers and certificate issuance.
    '''
    if 'ak' not in args:
        print('Account key is required: ak=<filename>', file=sys.stderr)
        return None
    # check account key
    account_key_filename = os.path.expanduser(args['ak'])
    if not os.path.exists(account_key_filename):
        print('Account key file does not exist:', account_key_filename, file=sys.stderr)
        return None
    # load account key
    with open(account_key_filename, 'rb') as f:
        return f.read()

def _prepare_contacts(args):
    '''
    Helper function for create account or change account contacts
    '''
    contacts = args.get('email', [])
    if not isinstance(contacts, list):
        contacts = [contacts]
    return ['mailto:' + email for email in contacts]

def _prepare_csr_fields(args):
    '''
    Helper function for manual certificate issuance.
    '''
    if 'csr-field' in args:
        result = dict()
        csr_fields = args['csr-field']
        if not isinstance(csr_fields, list):
            csr_fields = [csr_fields]
        for field in csr_fields:
            name, value = field.split(':', 1)
            result[name.strip()] = value.strip()
        return result
    else:
        return None

def run_command(command):
    logger.debug('Executing: %s', command)
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        raise Exception(f'Failed {command}: {result.stderr or result.stdout}')

#-----------------------------------------------------------------------------------
# Dependencies

from datetime import datetime, timedelta
from glob import glob
import logging
import os
import shlex
import subprocess
import sys
import traceback

import kvgargs
import yaml

from .client import (
    MyAcmeClient, MyAcmeStateFS, MyAcmeAuthzManual, MyAcmeAuthzScript, MyAcmeHttpError,
    get_certificate_validity_period, idna_encode, logger
)

#-----------------------------------------------------------------------------------
# Run main

if __name__ == '__main__':
    main()
