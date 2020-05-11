import re

from test_reader.discover.matchers.matcher import Matcher
from test_reader.discover.matchers.matcher_result import MatcherResult
from test_reader.discover.matchers.matcher_result_type import MatcherResultType


class FileNameMatcher(Matcher):

    def matches(self, file_path: str) -> [MatcherResult]:
        config_names = self.test_config.get_type_names()
        matched_types = []
        result = []
        for config_name in config_names:
            test_config = self.test_config.get_type_by_name(config_name)
            if not test_config.file_name_regex:
                matched_types.append(test_config.name)
            else:
                if re.match(test_config.file_name_regex, file_path):
                    matched_types.append(test_config.name)
        if matched_types:
            result = [MatcherResult(file_path, matched_types, MatcherResultType.file)]
        return result

