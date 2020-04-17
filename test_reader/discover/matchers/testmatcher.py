from test_reader.discover.matchers.matcher import Matcher
from test_reader.discover.matchers.matcher_result import MatcherResult
from test_reader.config.configurationtest import ConfigurationTest
import re

from test_reader.discover.matchers.matcher_result_type import MatcherResultType


class TestMatcher(Matcher):

    def matches(self, file_path: str) -> [MatcherResult]:
        types_by_test_name = {}
        for test_type in self.test_config.get_type_names():
            found_tests = self.__get_tests_by_type(file_path, test_type)
            self.__append_tests_to_dict(found_tests, test_type, types_by_test_name)

        return self.__build_results(types_by_test_name)

    @staticmethod
    def __append_tests_to_dict(found_tests, test_type, types_by_test_name):
        for test_name in found_tests:
            if test_name not in types_by_test_name.keys():
                types_by_test_name[test_name] = []
            types_by_test_name[test_name].append(test_type)

    def __get_tests_by_type(self, file_path, test_type) -> [str]:
        curr_test_config = self.test_config.get_type_by_name(test_type)
        with open(file_path) as file:
            if curr_test_config.test_rules.test_description_strategy == 'SAME_LINE':
                found_tests = self.__get_tests_by_same_line_strategy(curr_test_config, file)
            else:
                found_tests = self.__get_tests_by_next_line_strategy(curr_test_config, file)
        file.close()
        return found_tests

    def __get_tests_by_next_line_strategy(self, curr_test_config, file) -> [str]:
        has_test = False
        found_tests = []
        exclude_test = False
        for line in file:
            if curr_test_config.test_rules.test_description_strategy == 'NEXT_LINE' and has_test and line.strip() != '':
                found_tests.append(self.__get_test_description(curr_test_config, line.strip()))
                has_test = False
                continue

            if re.match(curr_test_config.test_rules.test_notation, line.strip()):
                if not exclude_test:
                    has_test = True
                else:
                    exclude_test = False
                continue
            exclude_test = self.__should_exclude_test(curr_test_config, line.strip())
        return found_tests

    def __should_exclude_test(self, curr_test_config, line):
        exclude_test = False
        if curr_test_config.test_rules.test_exclusion_regex and \
                curr_test_config.test_rules.test_exclusion_strategy == 'BEFORE_LINE':
            if re.match(curr_test_config.test_rules.test_exclusion_regex, line.strip()):
                exclude_test = True
        return exclude_test

    def __get_tests_by_same_line_strategy(self, curr_test_config: ConfigurationTest, file) -> [str]:
        found_tests = []
        exclude_test = False
        for line in file:
            if re.match(curr_test_config.test_rules.test_notation, line.strip()):
                if not exclude_test:
                    found_tests.append(self.__get_test_description(curr_test_config, line))
                else:
                    exclude_test = False
                    continue
            exclude_test = self.__should_exclude_test(curr_test_config, line.strip())
        return found_tests

    @staticmethod
    def __get_test_description(curr_test_config, line):
        result = re.search(curr_test_config.test_rules.test_description_regex, line)
        if result:
            return result.group(1)
        else:
            return line.strip()

    @staticmethod
    def __build_results(types_by_test_name) -> [MatcherResult]:
        results = []
        for test_name in types_by_test_name.keys():
            results.append(MatcherResult(test_name, types_by_test_name[test_name], MatcherResultType.test))

        return results
