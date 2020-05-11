from __future__ import annotations
from .testrules import TestRules


class ConfigurationTest(object):

    def __init__(self, test_config: {}):
        self.name = self.read_property(test_config, 'name')
        self.extends = self.read_property(test_config, 'extends')
        self.file_name_regex = self.read_property(test_config, 'file_name_regex')
        self.path = self.read_property(test_config, 'path')
        self.file_content_contains = self.read_property(test_config, 'file_content_contains')
        self.children = []
        self.weight = 1
        test_rules = self.read_property(test_config, 'test_rules')
        if test_rules is not None:
            self.test_rules = TestRules(test_rules)
        else:
            self.test_rules = TestRules({})

    def add_child(self, child: ConfigurationTest):
        child.weight = self.weight + 1
        if self.file_name_regex is not None and child.file_name_regex is None:
            child.file_name_regex = self.file_name_regex

        if self.file_content_contains is not None and child.file_content_contains is None:
            child.file_content_contains = self.file_content_contains

        if self.test_rules is not None:
            if child.test_rules is None:
                child.test_rules = self.test_rules
            else:
                child.test_rules.from_parent(self.test_rules)

        self.children.append(child)

    def get_type_names(self):
        return self.__get_type_names(self)

    def __get_type_names(self, config: ConfigurationTest):
        type_names = [config.name]
        if config.children:
            for child in config.children:
                type_names = type_names + self.__get_type_names(child)
        return type_names

    def get_type_by_name(self, name: str) -> ConfigurationTest:
        return self.__get_type_by_name(self, name)

    def __get_type_by_name(self, config: ConfigurationTest, name: str) -> ConfigurationTest:
        if config.name == name:
            return config
        for child in config.children:
            result = self.__get_type_by_name(child, name)
            if result:
                return result

        return None

    @staticmethod
    def read_property(test_config: {}, property: str):
        try:
            return test_config[property]
        except KeyError:
            return None
