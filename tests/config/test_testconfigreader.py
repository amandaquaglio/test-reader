from unittest import TestCase, mock
from unittest.mock import mock_open
from test_reader.config.testconfigreader import TestConfigReader
from yaml import dump
from test_reader.config.configurationtest import ConfigurationTest

class TestTestConfigReader(TestCase):

    @mock.patch.dict('os.environ', {"YAML_CONFIG_PATH": "path"})
    def test_validate_that_config_reader_uses_correct_yaml_path(self):
        with mock.patch('builtins.open', mock_open(read_data="tests: []")) as mock_open_file:
            TestConfigReader().read_config()
            mock_open_file.assert_called_once_with("path")

    @mock.patch.dict('os.environ', {"YAML_CONFIG_PATH": "path"})
    def test_validate_that_root_tests_is_returned_as_empty_when_there_is_no_test(self):
        with mock.patch('builtins.open', mock_open(read_data="tests: []")) as mock_open_file:
            self.assertEqual([], TestConfigReader().read_config())

    @mock.patch.dict('os.environ', {"YAML_CONFIG_PATH": "path"})
    def test_validate_that_a_test_with_no_extends_is_returned_as_root(self):
        yaml_dict = {"tests": [{"name": "Unit"}]}
        with mock.patch('builtins.open', mock_open(read_data=dump(yaml_dict))) as mock_open_file:
            root_tests = TestConfigReader().read_config()
            self.assertEqual("Unit", root_tests[0].name)
            self.assertEqual(0, len(root_tests[0].children))

    @mock.patch.dict('os.environ', {"YAML_CONFIG_PATH": "path"})
    def test_validate_that_a_test_with_extends_is_not_returned_as_root(self):
        yaml_dict = {"tests": [{"name": "Unit"}, {"name": "Child", "extends": "Unit"}]}
        with mock.patch('builtins.open', mock_open(read_data=dump(yaml_dict))) as mock_open_file:
            root_tests = TestConfigReader().read_config()
            self.assertEqual("Unit", root_tests[0].name)
            self.assertEqual(1, len(root_tests[0].children))

    @mock.patch.dict('os.environ', {"YAML_CONFIG_PATH": "path"})
    def test_validate_that_spreadsheet_columns_are_returned_correctly_when_it_is_configured(self):
        yaml_dict = {"tests": [{"name": "Unit", "spreadsheet_columns": {'column1': 'value1', 'column2': 'value2'}}, {"name": "Child", "extends": "Unit", 'spreadsheet_columns': {'column1': 'value1', 'column3': 'value2'}}, {"name": "Integration", "spreadsheet_columns": {'column5': 'value1'}}]}
        with mock.patch('builtins.open', mock_open(read_data=dump(yaml_dict))) as mock_open_file:
            configs : [ConfigurationTest] = TestConfigReader().read_config()
            self.assertEqual(2, len(configs))
            self.assertEqual(4, len(configs[0].spreadsheet_columns))
            self.assertEqual(4, len(configs[0].children[0].spreadsheet_columns))
            self.assertEqual(4, len(configs[1].spreadsheet_columns))
            self.assertIn('column1', configs[0].spreadsheet_columns)
            self.assertIn('column2', configs[0].spreadsheet_columns)
            self.assertIn('column3', configs[0].spreadsheet_columns)
            self.assertIn('column5', configs[0].spreadsheet_columns)

            self.assertIsNone(configs[0].spreadsheet_columns['column5'])
            self.assertIsNotNone(configs[0].spreadsheet_columns['column1'])
            self.assertIsNone(configs[0].children[0].spreadsheet_columns['column5'])
            self.assertIsNotNone(configs[0].children[0].spreadsheet_columns['column1'])

            self.assertIsNotNone(configs[1].spreadsheet_columns['column5'])
            self.assertIsNone(configs[1].spreadsheet_columns['column1'])
