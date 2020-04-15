from test_reader.config.testconfigreader import TestConfigReader
from test_reader.discover.testdiscovery import TestDiscovery
from test_reader.publish.sheetspublisher import SheetsPublisher


class ReadTests:

    def __init__(self):
        self.tests = []
        self.sheet_tests = []

    def read(self):
        test_configs = TestConfigReader().read_config()
        for test_config in test_configs:
            self.tests = self.tests + TestDiscovery(test_config).discover_tests()

        for test in self.tests:
            sheet_test = [test.file_name, test.description, test.type]
            self.sheet_tests.append(sheet_test)
        SheetsPublisher().publish(self.sheet_tests)






