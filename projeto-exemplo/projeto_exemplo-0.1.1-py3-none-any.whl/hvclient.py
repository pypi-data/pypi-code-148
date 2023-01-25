import os
import hvac
from hvac.exceptions import InvalidPath
from requests.exceptions import ConnectionError
import traceback


class Hvclient():
    """ Classe para conectar o Vault e obter os dados
    para execução do robô
    """

    def __init__(self):
        self.client = self.__client()

    def get_credentials(self, secrets_path):
        """ Obtem as credenciais do Vault

        :param secrets_path: Especifica os dados do vault
        que serão utilizados
        :type secrets_path: [type]
        :return: Retorna os dados da secrets
        :rtype: [type]
        """
        return self.__get_secrets(secrets_path)

    def __client(self):
        """ Obtem o cliente conectado no Vault

        :return: Retorna o cliente conectado no Vault
        :rtype: [type]
        """
        try:
            client = hvac.Client(
                token=os.environ.get('HCV_TOKEN')
            )
            assert client.is_authenticated(), Exception(
                'Verifique o token configurado na variável de ambiente')
            return client
        except ConnectionError:
            msg = 'Verifique se o Vault está em execução e se as variáveis de'\
                'ambiente, descritas na documentação dessa'\
                'Lib, estão configuradas.'
            raise f'{traceback.format_exc()} \n\n{msg}'

    def __get_secrets(self, path):
        """ Obtem as secrets do Vault

        :param path: Específica o caminho do token
        :type path: [type]
        :raises e: Lança uma exeção caso o Path for inválido ou a chave
        esteja incorreta
        :return: Retorna o Json com as informações do Vault
        :rtype: [type]
        """
        try:
            hvreponse = \
                self.client.secrets.kv.read_secret_version(path=path)
            return hvreponse['data']['data']
        except InvalidPath:
            raise f'{traceback.format_exc()}'
        except KeyError:
            raise f'{traceback.format_exc()}'