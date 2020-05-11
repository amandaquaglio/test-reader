from test_reader.config.configurationtest import ConfigurationTest


class Test:

    def __init__(self, file_name: str, description: str, test_config: ConfigurationTest):
        self.file_name = file_name
        self.description = description
        self.type_name = test_config.name
        self.extra_columns = test_config.spreadsheet_columns
