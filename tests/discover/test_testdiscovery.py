from unittest import TestCase, mock
from unittest.mock import MagicMock

from test_reader.discover.matchers.matcher_result import MatcherResult
from test_reader.discover.matchers.matcher_result_type import MatcherResultType
from test_reader.discover.testdiscovery import TestDiscovery


def get_type_side_effect(*args, **kwargs):
    mock = MagicMock()
    mock.weight = 2
    if args[0] == 'Abc':
        mock.weight = 1
    return mock


class TestTestDiscovery(TestCase):
    @mock.patch('test_reader.discover.matchers.filecontentcontainsmatcher.FileContentContainsMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filenamematcher.FileNameMatcher.matches')
    @mock.patch('os.walk')
    def test_given_test_file_that_does_not_match_file_name_then_no_tests_should_be_returned(self,
                                                                                            mock_walk,
                                                                                            mock_filenamematcher,
                                                                                            mock_filecontentcontains):
        mock_walk.return_value = [('/tests', (), ('test_file',))]
        mock_filenamematcher.return_value = []
        mock_filecontentcontains.return_value = [MatcherResult('/tests/test_file', ['Test'], MatcherResultType.file)]
        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.path = '/'
        tests = TestDiscovery(test_config).discover_tests()
        self.assertEqual([], tests)
        mock_filenamematcher.assert_called_once_with('/tests/test_file')
        mock_filecontentcontains.matches.assert_not_called()

    @mock.patch('test_reader.discover.matchers.testmatcher.TestMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filecontentcontainsmatcher.FileContentContainsMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filenamematcher.FileNameMatcher.matches')
    @mock.patch('os.walk')
    def test_given_test_file_that_does_not_match_file_content_contains_then_no_tests_should_be_returned(self,
                                                                                                        mock_walk,
                                                                                                        mock_filenamematcher,
                                                                                                        mock_filecontentcontains,
                                                                                                        mock_test_matcher):
        mock_walk.return_value = [('/tests', (), ('test_file',))]
        mock_filenamematcher.return_value = [MatcherResult('/tests/test_file', ['Test'], MatcherResultType.file)]
        mock_filecontentcontains.return_value = []
        mock_test_matcher.return_value = [MatcherResult('test_case', ['Test'], MatcherResultType.test)]

        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.path = '/'
        tests = TestDiscovery(test_config).discover_tests()
        self.assertEqual([], tests)
        mock_filenamematcher.assert_called_once_with('/tests/test_file')
        mock_filecontentcontains.assert_called_once_with('/tests/test_file')
        mock_test_matcher.assert_not_called

    @mock.patch('test_reader.discover.matchers.testmatcher.TestMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filecontentcontainsmatcher.FileContentContainsMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filenamematcher.FileNameMatcher.matches')
    @mock.patch('os.walk')
    def test_given_test_file_that_does_not_have_tests_then_no_tests_should_be_returned(self, mock_walk,
                                                                                       mock_filenamematcher,
                                                                                       mock_filecontentcontains,
                                                                                       mock_test_matcher):
        mock_walk.return_value = [('/tests', (), ('test_file',))]
        mock_filenamematcher.return_value = [MatcherResult('/tests/test_file', ['Test'], MatcherResultType.file)]
        mock_filecontentcontains.return_value = [MatcherResult('/tests/test_file', ['Test'], MatcherResultType.file)]
        mock_test_matcher.return_value = []

        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.path = '/'
        tests = TestDiscovery(test_config).discover_tests()
        self.assertEqual([], tests)

    @mock.patch('test_reader.discover.matchers.testmatcher.TestMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filecontentcontainsmatcher.FileContentContainsMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filenamematcher.FileNameMatcher.matches')
    @mock.patch('os.walk')
    def test_given_test_file_when_file_name_has_no_types_in_common_to_file_content_then_no_tests_should_be_returned(
            self,
            mock_walk,
            mock_filenamematcher,
            mock_filecontentcontains,
            mock_test_matcher):
        mock_walk.return_value = [('/tests', (), ('test_file',))]
        mock_filenamematcher.return_value = [MatcherResult('/tests/test_file', ['Test'], MatcherResultType.file)]
        mock_filecontentcontains.return_value = [
            MatcherResult('/tests/test_file', ['OtherTest'], MatcherResultType.file)]
        mock_test_matcher.return_value = [MatcherResult('test_case', ['Test'], MatcherResultType.test)]

        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.path = '/'
        tests = TestDiscovery(test_config).discover_tests()
        self.assertEqual([], tests)

    @mock.patch('test_reader.discover.matchers.testmatcher.TestMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filecontentcontainsmatcher.FileContentContainsMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filenamematcher.FileNameMatcher.matches')
    @mock.patch('os.walk')
    def test_given_test_file_when_test_type_has_no_types_in_common_to_file_types_then_no_tests_should_be_returned(
            self,
            mock_walk,
            mock_filenamematcher,
            mock_filecontentcontains,
            mock_test_matcher):
        mock_walk.return_value = [('/tests', (), ('test_file',))]
        mock_filenamematcher.return_value = [MatcherResult('/tests/test_file', ['Test'], MatcherResultType.file)]
        mock_filecontentcontains.return_value = [
            MatcherResult('/tests/test_file', ['Test'], MatcherResultType.file)]
        mock_test_matcher.return_value = [MatcherResult('test_case', ['OtherTest'], MatcherResultType.test)]

        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.path = '/'
        tests = TestDiscovery(test_config).discover_tests()
        self.assertEqual([], tests)

    @mock.patch('test_reader.discover.matchers.testmatcher.TestMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filecontentcontainsmatcher.FileContentContainsMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filenamematcher.FileNameMatcher.matches')
    @mock.patch('os.walk')
    def test_given_test_file_when_test_type_has_one_type_in_common_to_file_types_then_tests_should_be_returned(
            self,
            mock_walk,
            mock_filenamematcher,
            mock_filecontentcontains,
            mock_test_matcher):
        mock_walk.return_value = [('/tests', (), ('test_file',))]
        mock_filenamematcher.return_value = [MatcherResult('/tests/test_file', ['Test', 'Abc'], MatcherResultType.file)]
        mock_filecontentcontains.return_value = [
            MatcherResult('/tests/test_file', ['Def', 'Test'], MatcherResultType.file)]
        mock_test_matcher.return_value = [MatcherResult('test_case', ['Test', 'OtherTest'], MatcherResultType.test)]

        test_config = MagicMock()
        test_config.name = 'Test'
        test_config.path = '/'
        tests = TestDiscovery(test_config).discover_tests()
        self.assertEqual(1, len(tests))
        self.assertEqual('/tests/test_file', tests[0].file_name)
        self.assertEqual('test_case', tests[0].description)
        self.assertEqual('Test', tests[0].type)

    @mock.patch('test_reader.discover.matchers.testmatcher.TestMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filecontentcontainsmatcher.FileContentContainsMatcher.matches')
    @mock.patch('test_reader.discover.matchers.filenamematcher.FileNameMatcher.matches')
    @mock.patch('os.walk')
    def test_given_test_file_when_test_type_has_two_types_in_common_to_file_then_most_weighted_type_should_be_returned(
            self,
            mock_walk,
            mock_filenamematcher,
            mock_filecontentcontains,
            mock_test_matcher):
        mock_walk.return_value = [('/tests', (), ('test_file',))]
        mock_filenamematcher.return_value = [MatcherResult('/tests/test_file', ['Test', 'Abc'], MatcherResultType.file)]
        mock_filecontentcontains.return_value = [
            MatcherResult('/tests/test_file', ['Abc', 'Test'], MatcherResultType.file)]
        mock_test_matcher.return_value = [MatcherResult('test_case', ['Test', 'Abc'], MatcherResultType.test)]

        child_config_mock = MagicMock()
        child_config_mock.name = 'Test'
        child_config_mock.weight = 2

        parent_config_mock = MagicMock()
        parent_config_mock.name = 'Abc'
        parent_config_mock.path = '/'
        parent_config_mock.get_type_names.return_value = ['Abc', 'Test']
        parent_config_mock.get_type_by_name.side_effect = get_type_side_effect
        parent_config_mock.weight = 1

        tests = TestDiscovery(parent_config_mock).discover_tests()
        self.assertEqual(1, len(tests))
        self.assertEqual('/tests/test_file', tests[0].file_name)
        self.assertEqual('test_case', tests[0].description)
        self.assertEqual('Test', tests[0].type)
