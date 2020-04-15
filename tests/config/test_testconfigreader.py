from unittest import TestCase, mock
from unittest.mock import mock_open
from test_reader.config.testconfigreader import TestConfigReader
from yaml import dump


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
