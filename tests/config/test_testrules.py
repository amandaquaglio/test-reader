from unittest import TestCase, mock
from test_reader.config.testrules import TestRules


class TestTestRules(TestCase):

    def test_given_child_without_test_description_regex_when_from_parent_then_it_should_have_this_attr_from_parent(
            self):
        child = TestRules({})
        child.from_parent(TestRules({'test_description_regex': 'ParentTeste'}))
        self.assertEqual('ParentTeste', child.test_description_regex)

    def test_given_child_with_test_description_regex_when_from_parent_then_it_should_keep_its_attribute(
            self):
        child = TestRules({'test_description_regex': 'ChildTeste'})
        child.from_parent(TestRules({'test_description_regex': 'ParentTeste'}))
        self.assertEqual('ChildTeste', child.test_description_regex)

    def test_given_child_without_test_description_strategy_when_from_parent_then_it_should_have_this_attr_from_parent(
            self):
        child = TestRules({})
        child.from_parent(TestRules({'test_description_strategy': 'ParentTeste'}))
        self.assertEqual('ParentTeste', child.test_description_strategy)

    def test_given_child_with_test_description_strategy_when_from_parent_then_it_should_keep_its_attribute(
            self):
        child = TestRules({'test_description_strategy': 'ChildTeste'})
        child.from_parent(TestRules({'test_description_strategy': 'ParentTeste'}))
        self.assertEqual('ChildTeste', child.test_description_strategy)

    def test_given_child_without_test_notation_when_from_parent_then_it_should_have_this_attr_from_parent(self):
        child = TestRules({})
        child.from_parent(TestRules({'test_notation': 'ParentTeste'}))
        self.assertEqual('ParentTeste', child.test_notation)

    def test_given_child_with_test_notation_when_from_parent_then_it_should_keep_its_attribute(
            self):
        child = TestRules({'test_notation': 'ChildTeste'})
        child.from_parent(TestRules({'test_notation': 'ParentTeste'}))
        self.assertEqual('ChildTeste', child.test_notation)

    def test_given_child_without_test_exclusion_strategy_when_from_parent_then_it_should_have_this_attr_from_parent(
            self):
        child = TestRules({})
        child.from_parent(TestRules({'test_exclusion_strategy': 'ParentTeste'}))
        self.assertEqual('ParentTeste', child.test_exclusion_strategy)

    def test_given_child_with_test_exclusion_strategy_when_from_parent_then_it_should_keep_its_attribute(
            self):
        child = TestRules({'test_exclusion_strategy': 'ChildTeste'})
        child.from_parent(TestRules({'test_exclusion_strategy': 'ParentTeste'}))
        self.assertEqual('ChildTeste', child.test_exclusion_strategy)

    def test_given_child_without_test_exclusion_regex_when_from_parent_then_it_should_have_this_attr_from_parent(
            self):
        child = TestRules({})
        child.from_parent(TestRules({'test_exclusion_regex': 'ParentTeste'}))
        self.assertEqual('ParentTeste', child.test_exclusion_regex)

    def test_given_child_with_test_exclusion_regex_when_from_parent_then_it_should_keep_its_attribute(
            self):
        child = TestRules({'test_exclusion_regex': 'ChildTeste'})
        child.from_parent(TestRules({'test_exclusion_regex': 'ParentTeste'}))
        self.assertEqual('ChildTeste', child.test_exclusion_regex)