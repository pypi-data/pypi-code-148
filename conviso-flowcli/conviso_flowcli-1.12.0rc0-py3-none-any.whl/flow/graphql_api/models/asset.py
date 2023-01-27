from convisoappsec.common.git_data_parser import GitDataParser

INITIAL_VALUE = None


class Asset():

    def __init__(
        self,
        repository_dir,
        company_id,
        name=INITIAL_VALUE,
        scan_type=INITIAL_VALUE

    ):
        self._repository_dir = repository_dir
        self.company_id = company_id
        self.name = self.__setup_asset_name(name)
        self.scan_type = scan_type

    def __setup_asset_name(self, name):
        has_user_input = name != INITIAL_VALUE
        if has_user_input:
            return name

        return GitDataParser(self._repository_dir).parse_name()
