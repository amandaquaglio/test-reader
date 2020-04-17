from unittest import TestCase, mock
from unittest.mock import MagicMock
from test_reader.discover.matchers.filenamematcher import FileNameMatcher


class TestFileNameMatcher(TestCase):

    def test_given_a_test_config_without_matcher_then_it_should_be_returned(self):
        # Arrange
        test_name = 'Test'
        file_path = '/class/DEFTest.kt'

        test_config = MagicMock()
        test_config.file_name_regex = None
        test_config.name = test_name
        test_config.get_type_names.return_value = [test_name]
        test_config.get_type_by_name.side_effect = [test_config]

        # Act
        result = FileNameMatcher(test_config).matches(file_path)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(file_path, result[0].name)
        self.assertEqual([test_name], result[0].test_types)

    def test_given_a_test_config_with_matcher_that_matches_file_then_it_should_be_returned(self):
        test_name = 'Test'
        file_path = '/class/ABCTest.kt'

        # Arrange
        test_config = MagicMock()
        test_config.file_name_regex = '.*ABCTest\.kt$'
        test_config.name = test_name
        test_config.get_type_names.return_value = [test_name]
        test_config.get_type_by_name.side_effect = [test_config]

        # Act
        result = FileNameMatcher(test_config).matches(file_path)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(file_path, result[0].name)
        self.assertEqual([test_name], result[0].test_types)

    def test_given_a_test_config_with_matcher_that_does_not_matcher_file_then_it_should_not_be_returned(self):
        test_name = 'Test'
        file_path = '/class/DEFTest.kt'

        # Arrange
        test_config = MagicMock()
        test_config.file_name_regex = '.*ABCTest\.kt$'
        test_config.name = test_name
        test_config.get_type_names.return_value = [test_name]
        test_config.get_type_by_name.side_effect = [test_config]

        # Act
        result = FileNameMatcher(test_config).matches(file_path)

        # Assert
        self.assertEqual(0, len(result))

    def test_given_test_configs_without_matchers_then_they_should_be_returned(self):
        child_test_name = 'Child'
        parent_test_name = 'Parent'
        file_path = '/class/DEFTest.kt'

        # Arrange
        parent, child = MagicMock(), MagicMock()
        child.name = child_test_name
        child.file_name_regex = None

        parent.file_name_regex = None
        parent.name = parent_test_name
        parent.get_type_names.return_value = [parent_test_name, child_test_name]
        parent.get_type_by_name.side_effect = [parent, child]

        # Act
        result = FileNameMatcher(parent).matches(file_path)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(file_path, result[0].name)
        self.assertEqual([parent_test_name, child_test_name], result[0].test_types)

    def test_given_test_config_with_matcher_that_matches_file_and_other_without_matcher_then_all_should_be_returned(self):
        child_test_name = 'Child'
        parent_test_name = 'Parent'
        file_path = '/class/ABCTest.kt'

        # Arrange
        parent, child = MagicMock(), MagicMock()
        child.file_name_regex = None
        child.name = child_test_name

        parent.file_name_regex = '.*ABCTest\.kt$'
        parent.name = parent_test_name
        parent.get_type_names.return_value = [parent_test_name, child_test_name]
        parent.get_type_by_name.side_effect = [parent, child]

        # Act
        result = FileNameMatcher(parent).matches(file_path)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(file_path, result[0].name)
        self.assertEqual([parent_test_name, child_test_name], result[0].test_types)

    def test_given_test_config_with_matchers_that_matches_file_then_all_should_be_returned(self):
        child_test_name = 'Child'
        parent_test_name = 'Parent'
        file_path = '/class/DEFTest.kt'

        # Arrange
        parent, child = MagicMock(), MagicMock()
        child.file_name_regex = '.*DEFTest\.kt$'
        child.name = child_test_name

        parent.file_name_regex = '.*Test\.kt$'
        parent.name = parent_test_name
        parent.get_type_names.return_value = [parent_test_name, child_test_name]
        parent.get_type_by_name.side_effect = [parent, child]

        # Act
        result = FileNameMatcher(parent).matches(file_path)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(file_path, result[0].name)
        self.assertEqual([parent_test_name, child_test_name], result[0].test_types)

    def test_given_test_config_with_matchers_where_one_matches_and_other_does_not_then_only_first_should_be_returned(self):
        child_test_name = 'Child'
        parent_test_name = 'Parent'
        file_path = '/class/DEFTest.kt'

        # Arrange
        parent, child = MagicMock(), MagicMock()
        child.file_name_regex = '.*DEFTest\.kt$'
        child.name = child_test_name

        parent.file_name_regex = '.*ABCTest\.kt$'
        parent.name = parent_test_name
        parent.get_type_names.return_value = [parent_test_name, child_test_name]
        parent.get_type_by_name.side_effect = [parent, child]

        # Act
        result = FileNameMatcher(parent).matches(file_path)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual(file_path, result[0].name)
        self.assertEqual([child_test_name], result[0].test_types)
