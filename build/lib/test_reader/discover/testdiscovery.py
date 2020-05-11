from test_reader.config.configurationtest import ConfigurationTest
from test_reader.discover.matchers.filecontentcontainsmatcher import FileContentContainsMatcher
from test_reader.discover.matchers.filenamematcher import FileNameMatcher
from test_reader.discover.matchers.matcher_result import MatcherResult
from test_reader.discover.matchers.matcher_result_type import MatcherResultType
from test_reader.discover.matchers.testmatcher import TestMatcher
import os

from test_reader.discover.test import Test


class TestDiscovery:

    def __init__(self, test_config: ConfigurationTest):
        self.__test_config = test_config
        self.__matchers = [FileNameMatcher(test_config), FileContentContainsMatcher(test_config),
                           TestMatcher(test_config)]
        self.__results = []

    def discover_tests(self) -> [Test]:
        os.chdir(self.__test_config.path)
        for root, dirs, files in os.walk(".", topdown=False):
            for file in files:
                file_path = str(os.path.join(root, file))
                self.__get_tests_from_file(file_path)

        return self.__results

    def __get_tests_from_file(self, file_name):
        file_results: [MatcherResult] = []
        test_results: [MatcherResult] = []
        for matcher in self.__matchers:
            matcher_result = matcher.matches(file_name)
            if not matcher_result:
                break
            else:
                matcher_file_result, matcher_test_result = self.__classify_results(matcher_result)
                file_results = file_results + matcher_file_result
                test_results = test_results + matcher_test_result
        if file_results and test_results:
            self.__get_tests_from_result(file_name, file_results, test_results)

    def __get_tests_from_result(self, file_name, file_results, test_results):
        file_type_candidates = self.__get_file_type_candidates(file_results)
        for test_result in test_results:
            test_type_candidates = set(file_type_candidates).intersection(test_result.test_types)
            if test_type_candidates:
                selected_test_type = self.__select_test_type(test_type_candidates)
                self.__results.append(Test(file_name, test_result.name, selected_test_type))

    @staticmethod
    def __get_file_type_candidates(file_results):
        file_type_candidates = file_results[0].test_types
        for file_result in file_results:
            file_type_candidates = set(file_type_candidates).intersection(file_result.test_types)
        return file_type_candidates

    def __get_test_weight(self, test_type):
        return self.__test_config.get_type_by_name(test_type).weight

    @staticmethod
    def __classify_results(results):
        file_results: [MatcherResult] = []
        test_results: [MatcherResult] = []
        for result in results:
            if result.result_type == MatcherResultType.file:
                file_results.append(result)
            else:
                test_results.append(result)
        return file_results, test_results

    def __select_test_type(self, test_type_candidates):
        selected_test_type = next(iter(test_type_candidates))
        if len(test_type_candidates) > 1:
            for test_type in test_type_candidates:
                if self.__get_test_weight(test_type) >= self.__get_test_weight(selected_test_type):
                    selected_test_type = test_type
        return selected_test_type
