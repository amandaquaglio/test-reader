import os
from google.oauth2 import service_account
from apiclient import discovery


class SheetsPublisher:
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def publish(self, values):
        app_name = os.environ.get("APP_NAME")
        credentials = service_account.Credentials.from_service_account_file(
            os.environ.get("CREDENTIALS_PATH"), scopes=self.SCOPES)

        service = discovery.build('sheets', 'v4', credentials=credentials)
        spreadsheet_id = os.environ.get("SPREADSHEET_ID")
        batch_update_values_request_body = {
            'value_input_option': 'RAW',
            'data': [{
                'majorDimension': "ROWS",
                'range': f"{app_name}!A2:C{len(values) + 1}",
                'values': values
            }]
        }

        request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                              body=batch_update_values_request_body)
        response = request.execute()
