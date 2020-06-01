import os
from google.oauth2 import service_account
from apiclient import discovery
import logging

class SheetsPublisher:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def publish(self, values):
        app_name = os.environ.get("APP_NAME")
        credentials = service_account.Credentials.from_service_account_file(
            os.environ.get("CREDENTIALS_PATH"), scopes=self.SCOPES)

        service = discovery.build('sheets', 'v4', credentials=credentials, cache_discovery=False)
        spreadsheet_id = os.environ.get("SPREADSHEET_ID")
        self.setup_sheet(app_name, service, spreadsheet_id)
        self.update_sheet(app_name, service, spreadsheet_id, values)

    def setup_sheet(self, app_name, service, spreadsheet_id):
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_exists = self.__sheet_exists(app_name, sheet_metadata)
        if not sheet_exists:
            logging.info(f"Sheet {app_name} not found")
            self.__create_sheet(app_name, service, spreadsheet_id)
        else:
            range = '{0}!A1:Z'.format(app_name)
            resultClear = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range,
                                                                body={}).execute()

    def update_sheet(self, app_name, service, spreadsheet_id, values):
        last_column = chr(64 + len(values[0]))
        batch_update_values_request_body = {
            'value_input_option': 'RAW',
            'data': [{
                'majorDimension': "ROWS",
                'range': f"{app_name}!A1:{last_column}{len(values) + 1}",
                'values': values
            }]
        }
        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                              body=batch_update_values_request_body)
        request.execute()

    @staticmethod
    def __create_sheet(app_name, service, spreadsheet_id):
        request_create = {
                'requests': [
                    {
                        'addSheet': {
                            'properties': {
                                'title': app_name
                            }
                        }
                    }
                ]
            }
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request_create).execute()
        logging.info(f"Creating sheet")
        logging.info(f"Creating sheet response: {response} ")

    @staticmethod
    def __sheet_exists(app_name, sheet_metadata):
        sheet_exists = False
        sheets = sheet_metadata.get('sheets', '')
        for sheet in sheets:
            if sheet['properties']['title'] == app_name:
                sheet_exists = True
                break
        return sheet_exists
