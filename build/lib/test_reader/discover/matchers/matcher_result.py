from test_reader.discover.matchers.matcher_result_type import MatcherResultType


class MatcherResult:
    def __init__(self, name: str, test_types: [str], matcher_result_type: MatcherResultType):
        self.test_types = test_types
        self.name = name
        self.result_type = matcher_result_type
