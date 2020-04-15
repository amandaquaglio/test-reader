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
        for line in file:
            if curr_test_config.test_rules.test_description_strategy == 'NEXT_LINE' and has_test:
                found_tests.append(self.__get_test_description(curr_test_config, line))
                has_test = False

            if re.match(curr_test_config.test_rules.test_notation, line.strip()):
                has_test = True
        return found_tests

    def __get_tests_by_same_line_strategy(self, curr_test_config: ConfigurationTest, file) -> [str]:
        found_tests = []
        for line in file:
            if re.match(curr_test_config.test_rules.test_notation, line.strip()):
                found_tests.append(self.__get_test_description(curr_test_config, line))
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

    # def get_tests(self, test_config):
    #     with open(file_result.file) as file:
    #         for test_type_name in file_result.get_valid_types_for_tests():
    #             test_config = self.__root_test.get_type_by_name(test_type_name)
    #             test_rules = test_config.test_rules
    #             if test_rules.test_description_strategy == 'NEXT_LINE':
    #                 self.__get_tests_with_description_using_next_strategy(file, test_type_name, test_rules)
    #             if test_rules.test_description_strategy == 'SAME_LINE':
    #                 self.__get_tests_with_description_using_same_line_strategy(file, test_type_name, test_rules)
    #         file.close()
    #     return self.__struct_tests(file_result.file)
    #
    # def __get_tests_with_description_using_same_line_strategy(self, file, test_type_name, test_rules):
    #     for line in file:
    #         if re.match(test_rules.test_notation, line.strip()):
    #             self.__add_test(test_type_name, self.__get_test_description(line, test_rules))
    #
    # def __get_tests_with_description_using_next_strategy(self, file, test_type_name: str, test_rules: TestRules) -> []:
    #     has_test = False
    #     for line in file:
    #         if not has_test and re.match(test_rules.test_notation, line.strip()):
    #             has_test = True
    #             continue
    #         if has_test and line.strip() != '':
    #             self.__add_test(test_type_name, self.__get_test_description(line, test_rules))
    #             has_test = False
    #
    # @staticmethod
    # def __get_test_description(line: str, test_rules: TestRules) -> str:
    #     test_description = line
    #     if test_rules.test_description_regex is not None:
    #         m = re.search(test_rules.test_description_regex, line.strip())
    #         if m:
    #             test_description = m.group(1)
    #     return test_description
    #
    # def __add_test(self, test_type_name: str, test):
    #     selected_test_type = test_type_name
    #     if test in self.__tests_dict.keys():
    #         selected_test_type = self.__tiebreaker_test_type(self.__tests_dict[test], test_type_name)
    #     self.__tests_dict[test] = selected_test_type
    #
    # def __tiebreaker_test_type(self, test_type_name_1: str, test_type_name_2: str) -> str:
    #     type_weight_1 = self.__root_test.get_type_by_name(test_type_name_1).weight
    #     type_weight_2 = self.__root_test.get_type_by_name(test_type_name_2).weight
    #     selected_test_type = test_type_name_2
    #     if type_weight_1 > type_weight_2:
    #         selected_test_type = test_type_name_1
    #     return selected_test_type
    #
    # def __struct_tests(self, file_name):
    #     tests = []
    #     for test in self.__tests_dict:
    #         tests.append(Test(file_name, test, self.__tests_dict[test]))
    #     return tests
