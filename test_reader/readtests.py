from test_reader.config.testconfigreader import TestConfigReader
from test_reader.discover.testdiscovery import TestDiscovery
from test_reader.publish.sheetspublisher import SheetsPublisher
from test_reader.discover.test import Test


class ReadTests:

    def __init__(self):
        self.tests: [Test] = []
        self.sheet_tests = []
        self.all_columns = []

    def read(self):
        reader = TestConfigReader()
        test_configs = reader.read_config()
        self.all_columns = reader.all_columns
        for test_config in test_configs:
            self.tests = self.tests + TestDiscovery(test_config).discover_tests()

        header = ['FileName', 'TestCaseName', 'TestType']
        header = header + self.all_columns
        self.sheet_tests.append(header)

        for test in self.tests:
            sheet_test = [test.file_name, test.description, test.type_name]
            for column in self.all_columns:
                sheet_test.append(test.extra_columns[column])
            self.sheet_tests.append(sheet_test)
        SheetsPublisher().publish(self.sheet_tests)






