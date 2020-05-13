from unittest import TestCase, mock
from test_reader.config.configurationtest import ConfigurationTest


class TestConfigurationTest(TestCase):

    def test_get_type_names_from_config_without_extension(self):
        config = ConfigurationTest({'name': 'Unit'})
        self.assertEqual(['Unit'], config.get_type_names())

    def test_get_type_names_from_config_with_extensions(self):
        parent_config = ConfigurationTest({'name': 'Unit'})
        parent_config.add_child(ConfigurationTest({'name': 'Integration'}))
        parent_config.add_child(ConfigurationTest({'name': 'Component'}))
        self.assertEqual(['Unit', 'Integration', 'Component'], parent_config.get_type_names())

    def test_get_type_by_name_from_config_without_extension(self):
        configuration = {'name': 'Unit'}
        config = ConfigurationTest(configuration).get_type_by_name('Unit')
        self.assertEqual('Unit', config.name)

    def test_get_type_by_name_from_child_type(self):
        parent = ConfigurationTest({'name': 'Unit'})
        parent.add_child(ConfigurationTest({'name': 'Child'}))
        result = parent.get_type_by_name('Child')
        self.assertEqual('Child', result.name)

    def test_get_type_by_name_from_child_type_from_root_with_more_than_one_child(self):
        parent = ConfigurationTest({'name': 'Unit'})
        parent.add_child(ConfigurationTest({'name': 'Child1'}))
        parent.add_child(ConfigurationTest({'name': 'Child2'}))
        result = parent.get_type_by_name('Child2')
        self.assertEqual('Child2', result.name)

    def test_given_child_without_file_name_regex_when_add_child_then_it_should_have_this_attr_from_parent(self):
        parent = ConfigurationTest({'name': 'Unit', 'file_name_regex': 'Teste'})
        parent.add_child(ConfigurationTest({'name': 'Child'}))
        child = parent.get_type_by_name('Child')
        self.assertEqual('Teste', child.file_name_regex)

    def test_given_child_with_file_name_regex_when_add_child_then_it_should_keep_the_attr_value(self):
        parent = ConfigurationTest({'name': 'Unit', 'file_name_regex': 'Teste'})
        parent.add_child(ConfigurationTest({'name': 'Child', 'file_name_regex': 'ChildTeste'}))
        child = parent.get_type_by_name('Child')
        self.assertEqual('ChildTeste', child.file_name_regex)

    def test_given_child_without_file_content_contains_when_add_child_then_it_should_have_this_attr_from_parent(self):
        parent = ConfigurationTest({'name': 'Unit', 'file_content_contains': 'Teste'})
        parent.add_child(ConfigurationTest({'name': 'Child'}))
        child = parent.get_type_by_name('Child')
        self.assertEqual('Teste', child.file_content_contains)

    def test_given_child_with_file_content_contains_when_add_child_then_it_should_keep_the_attr_value(self):
        parent = ConfigurationTest({'name': 'Unit', 'file_content_contains': 'Teste'})
        parent.add_child(ConfigurationTest({'name': 'Child', 'file_content_contains': 'ChildTeste'}))
        child = parent.get_type_by_name('Child')
        self.assertEqual('ChildTeste', child.file_content_contains)

    def test_given_child_without_test_rules_when_add_child_then_it_should_have_this_attr_from_parent(self):
        parent = ConfigurationTest({'name': 'Unit', 'test_rules': {}})
        parent.add_child(ConfigurationTest({'name': 'Child'}))
        child = parent.get_type_by_name('Child')
        self.assertIsNotNone(child.test_rules)

    def test_given_child_with_test_rules_when_add_child_then_it_should_keep_the_attr_value(self):
        parent = ConfigurationTest({'name': 'Unit', 'test_rules': {}})
        parent.add_child(ConfigurationTest({'name': 'Child', 'test_rules': {'test_description_regex': 'ChildTeste'}}))
        child = parent.get_type_by_name('Child')
        self.assertEqual('ChildTeste', child.test_rules.test_description_regex)

    def test_given_child_without_spreadsheet_columns_when_add_child_then_it_should_have_this_attr_from_parent(self):
        parent = ConfigurationTest({'name': 'Unit', 'spreadsheet_columns': {'column1': 'value1', 'column2': 'value2'}})
        parent.add_child(ConfigurationTest({'name': 'Child'}))
        child = parent.get_type_by_name('Child')
        self.assertEqual('value1', child.spreadsheet_columns['column1'])
        self.assertEqual('value2', child.spreadsheet_columns['column2'])

    def test_given_child_with_spreadsheet_columns_when_add_child_then_it_should_keep_the_attr_value(self):
        parent = ConfigurationTest({'name': 'Unit', 'spreadsheet_columns': {'column1': 'value1', 'column2': 'value2'}})
        parent.add_child(ConfigurationTest({'name': 'Child',
                                            'spreadsheet_columns': {'column1': 'childvalue1', 'column3': 'value3',
                                                                    'column4': 'value4'}}))
        child = parent.get_type_by_name('Child')
        self.assertEqual('childvalue1', child.spreadsheet_columns['column1'])
        self.assertEqual('value2', child.spreadsheet_columns['column2'])
        self.assertEqual('value3', child.spreadsheet_columns['column3'])
        self.assertEqual('value4', child.spreadsheet_columns['column4'])

    @mock.patch.dict('os.environ', {"ROOT_FILE_PATH": "/home/dir"})
    def test_given_configuration_file_with_root_file_path_and_path_without_slash_then_it_should_be_concatenated_to_path(self):
        config = ConfigurationTest({'name': 'Unit', 'path': 'teste'})
        self.assertEqual('/home/dir/teste', config.path)

    @mock.patch.dict('os.environ', {"ROOT_FILE_PATH": "/home/dir/"})
    def test_given_configuration_file_with_root_file_path_with_slash_then_it_should_be_concatenated_to_path(
            self):
        config = ConfigurationTest({'name': 'Unit', 'path': 'teste'})
        self.assertEqual('/home/dir/teste', config.path)

    @mock.patch.dict('os.environ', {"ROOT_FILE_PATH": "/home/dir/"})
    def test_given_configuration_file_with_root_file_path_and_path_with_slash_then_it_should_be_concatenated_to_path(
            self):
        config = ConfigurationTest({'name': 'Unit', 'path': '/teste'})
        self.assertEqual('/home/dir/teste', config.path)