from test_reader.discover.matchers.matcher import Matcher
from test_reader.discover.matchers.matcher_result import MatcherResult
from test_reader.discover.matchers.matcher_result_type import MatcherResultType


class FileContentContainsMatcher(Matcher):

    def matches(self, file_path) -> [MatcherResult]:
        matched_types = []
        result = []
        for test_name in self.test_config.get_type_names():
            curr_test_config = self.test_config.get_type_by_name(test_name)
            if curr_test_config.file_content_contains:
                with open(file_path) as file:
                    for line in file:
                        if line.strip() == curr_test_config.file_content_contains:
                            matched_types.append(test_name)
                            break
                file.close()
            else:
                matched_types.append(test_name)
        if matched_types:
            result = [MatcherResult(file_path, matched_types, MatcherResultType.file)]
        return result
