class TestRules:
    def __init__(self, test_rules):
        self.test_description_regex = self.read_property(test_rules, 'test_description_regex')
        self.test_description_strategy = self.read_property(test_rules, 'test_description_strategy')
        self.test_notation = self.read_property(test_rules, 'test_notation')
        self.test_exclusion_regex = self.read_property(test_rules, 'test_exclusion_regex')
        self.test_exclusion_strategy = self.read_property(test_rules, 'test_exclusion_strategy')

    @staticmethod
    def read_property(test_config, property):
        try:
            return test_config[property]
        except KeyError:
            return None

    def from_parent(self, parent):
        if self.test_description_regex is None and parent.test_description_regex is not None:
            self.test_description_regex = parent.test_description_regex

        if self.test_description_strategy is None and parent.test_description_strategy is not None:
            self.test_description_strategy = parent.test_description_strategy

        if self.test_notation is None and parent.test_notation is not None:
            self.test_notation = parent.test_notation

        if self.test_exclusion_regex is None and parent.test_exclusion_regex is not None:
            self.test_exclusion_regex = parent.test_exclusion_regex

        if self.test_exclusion_strategy is None and parent.test_exclusion_strategy is not None:
            self.test_exclusion_strategy = parent.test_exclusion_strategy