from unittest import TestCase, mock
from unittest.mock import MagicMock, mock_open
from test_reader.discover.matchers.filecontentcontainsmatcher import FileContentContainsMatcher
from test_reader.config.configurationtest import ConfigurationTest
from test_reader.discover.matchers.matcher_result import MatcherResult


class TestFileContentContainsMatcher(TestCase):

    def test_given_a_test_config_without_matcher_then_it_should_be_returned(self):
        # Arrange
        test_config: ConfigurationTest = MagicMock()
        test_config.get_type_names.return_value = ['Test']
        test_config.file_content_contains = None
        test_config.get_type_by_name.return_value = test_config

        # Act
        result: [MatcherResult] = FileContentContainsMatcher(test_config).matches('path')

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual('path', result[0].name)
        self.assertEqual(['Test'], result[0].test_types)

    def test_given_a_test_config_with_matcher_that_matches_file_then_it_should_be_returned(self):
        # Arrange
        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.get_type_names.return_value = ['Test']
        test_config.get_type_by_name.return_value = test_config
        test_config.file_content_contains = '@RunWith(RobolectricTestRunner::class)'

        file_content = 'Titulo \n@RunWith(RobolectricTestRunner::class) \nFim'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = FileContentContainsMatcher(test_config).matches('path')

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('path', result[0].name)
            self.assertEqual(['Test'], result[0].test_types)

    def test_given_a_test_config_with_matcher_that_does_not_match_file_then_it_should_not_be_returned(self):
        # Arrange
        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.get_type_names.return_value = ['Test']
        test_config.get_type_by_name.return_value = test_config
        test_config.file_content_contains = '@RunWith(RobolectricTestRunner::class)'

        file_content = 'Titulo \nFim'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = FileContentContainsMatcher(test_config).matches('path')

            # Assert
            self.assertEqual(0, len(result))

    def test_given_test_configs_without_matchers_then_they_should_be_returned(self):
        child_test_name = 'Child'
        parent_test_name = 'Parent'
        file_path = '/class/DEFTest.kt'

        # Arrange
        parent_config_mock, child_config_mock = MagicMock(), MagicMock()
        child_config_mock.name = child_test_name
        child_config_mock.file_content_contains = None

        parent_config_mock.name = parent_test_name
        parent_config_mock.file_content_contains = None
        parent_config_mock.get_type_names.return_value = [parent_test_name, child_test_name]
        parent_config_mock.get_type_by_name.side_effect = [parent_config_mock, child_config_mock]

        # Act
        result: [MatcherResult] = FileContentContainsMatcher(parent_config_mock).matches('path')

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual('path', result[0].name)
        self.assertEqual(['Parent', 'Child'], result[0].test_types)

    def test_given_test_config_with_matcher_that_matches_file_and_other_without_matcher_then_all_should_be_returned(
            self):
        # Arrange
        child_config_mock = MagicMock()
        child_config_mock.name = 'Child'
        child_config_mock.file_content_contains = None

        parent_config_mock = MagicMock()
        parent_config_mock.name = 'Test'
        parent_config_mock.get_type_names.return_value = ['Test', 'Child']
        parent_config_mock.get_type_by_name.side_effect = [parent_config_mock, child_config_mock]
        parent_config_mock.file_content_contains = '@RunWith(RobolectricTestRunner::class)'

        file_content = 'Titulo \n@RunWith(RobolectricTestRunner::class) \nFim'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = FileContentContainsMatcher(parent_config_mock).matches('path')

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('path', result[0].name)
            self.assertEqual(['Test', 'Child'], result[0].test_types)

    def test_given_test_config_with_matchers_that_matches_file_then_all_should_be_returned(
            self):
        # Arrange
        child_config_mock = MagicMock()
        child_config_mock.name = 'Child'
        child_config_mock.file_content_contains = 'Begin'

        parent_config_mock = MagicMock()
        parent_config_mock.name = 'Test'
        parent_config_mock.get_type_names.return_value = ['Test', 'Child']
        parent_config_mock.get_type_by_name.side_effect = [parent_config_mock, child_config_mock]
        parent_config_mock.file_content_contains = '@RunWith(RobolectricTestRunner::class)'

        file_content = 'Begin \n@RunWith(RobolectricTestRunner::class) \nEnd'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = FileContentContainsMatcher(parent_config_mock).matches('path')

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('path', result[0].name)
            self.assertEqual(['Test', 'Child'], result[0].test_types)

    def test_given_test_config_with_matchers_where_one_matches_and_other_does_not_then_only_first_should_be_returned(
            self):
        # Arrange
        child_config_mock = MagicMock()
        child_config_mock.name = 'Child'
        child_config_mock.file_content_contains = 'OtherText'

        parent_config_mock = MagicMock()
        parent_config_mock.name = 'Test'
        parent_config_mock.get_type_names.return_value = ['Test', 'Child']
        parent_config_mock.get_type_by_name.side_effect = [parent_config_mock, child_config_mock]
        parent_config_mock.file_content_contains = '@RunWith(RobolectricTestRunner::class)'

        file_content = 'Begin \n@RunWith(RobolectricTestRunner::class) \nEnd'
        with mock.patch('builtins.open', mock_open(read_data=file_content)):
            # Act
            result = FileContentContainsMatcher(parent_config_mock).matches('path')

            # Assert
            self.assertEqual(1, len(result))
            self.assertEqual('path', result[0].name)
            self.assertEqual(['Test'], result[0].test_types)