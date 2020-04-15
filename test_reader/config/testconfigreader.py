from yaml import load
from os import environ
from test_reader.config.configurationtest import ConfigurationTest


class TestConfigReader:

    def __init__(self):
        self.__config_tests = []
        self.__config_tests_by_name = {}
        self.__root_tests = []

    """
        Class responsible to process test configuration from yaml
    """

    def read_config(self) -> [ConfigurationTest]:
        self.__read_test_configurations()
        self.__process_test_dependencies()
        return self.__root_tests

    """
        Read all tests from yaml
    """

    def __read_test_configurations(self):
        with open(environ.get("YAML_CONFIG_PATH")) as yaml_config:
            tests = load(yaml_config)['tests']
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
