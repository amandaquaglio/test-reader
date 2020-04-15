from test_reader.config.configurationtest import ConfigurationTest
from test_reader.discover.matchers.matcher_result import MatcherResult


class Matcher:

    def __init__(self, test_config: ConfigurationTest):
        self.test_config = test_config

    def matches(self, file_path: str) -> [MatcherResult]:
        pass
