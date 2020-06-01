from yaml import safe_load
from os import environ
from test_reader.config.configurationtest import ConfigurationTest


class TestConfigReader:

    def __init__(self):
        self.all_columns = []
        self.__config_tests = []
        self.__config_tests_by_name = {}
        self.__root_tests: [ConfigurationTest] = []

    """
        Class responsible to process test configuration from yaml
    """

    def read_config(self) -> [ConfigurationTest]:
        if len(self.__root_tests) == 0:
            self.__read_test_configurations()
            self.__process_test_dependencies()
            self.all_columns = self.__read_all_spreadsheet_columns()
            self.__compile_spreadsheet_columns()

        return self.__root_tests

    def __read_all_spreadsheet_columns(self) -> [str]:
        spreadsheet_columns = []
        for root_test in self.__root_tests:
            type_names = root_test.get_type_names()
            for type_name in type_names:
                test_config = root_test.get_type_by_name(type_name)
                self.append_columns_from_test_config(spreadsheet_columns, test_config)
        return spreadsheet_columns

    @staticmethod
    def append_columns_from_test_config(spreadsheet_columns, test_config):
        for column in test_config.spreadsheet_columns:
            if column not in spreadsheet_columns:
                spreadsheet_columns.append(column)

    """
        Read all tests from yaml
    """

    def __read_test_configurations(self):
        with open(environ.get("YAML_CONFIG_PATH")) as yaml_config:
            tests = safe_load(yaml_config)['tests']
            for test in tests:
                config_test = ConfigurationTest(test)
                config_test = self.__handle_root_test(config_test)
                self.__config_tests.append(config_test)
                self.__config_tests_by_name[config_test.name] = config_test
            yaml_config.close()

    def __handle_root_test(self, config_test: ConfigurationTest):
        if config_test.extends is None:
            self.__root_tests.append(config_test)
        return config_test

    """
        Process tests and extension. Only "root" tests would be returned. 
        The extensions will associated to their parent.
    """

    def __process_test_dependencies(self):
        for config_test in self.__config_tests:
            if config_test.extends is not None:
                parent = self.__config_tests_by_name[config_test.extends]
                parent.add_child(config_test)

    def __compile_spreadsheet_columns(self):
        for root_test in self.__root_tests:
            type_names = root_test.get_type_names()
            for type_name in type_names:
                test_config = root_test.get_type_by_name(type_name)
                test_config_columns = test_config.spreadsheet_columns
                for column in self.all_columns:
                    if column not in test_config_columns:
                        test_config.spreadsheet_columns[column] = None
