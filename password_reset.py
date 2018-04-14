from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os


def set_up_google_api(json_keys):
    '''
    INPUT: File name of Google API JSON keys
    OUTPUT: Service object to pull in data with Google API
    '''
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(json_keys, SCOPES)
        creds = tools.run_flow(flow, store)
    return build('sheets', 'v4', http=creds.authorize(Http()))


def get_email(service_obj, spreadsheet_id, sheet_cell):
    '''
    INPUT: Google API object, string of Google sheet ID, cell of email
    OUTPUT: Email for password reset
    '''
    SPREADSHEET_ID = spreadsheet_id
    RANGE_NAME = sheet_cell
    result = service_obj.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')

    return values[0][0]


def password_reset(email_adr, URL_str, element_name):
    '''
    INPUT: String of email, string of URL to access, name of element to access
    OUTPUT: None. (Browser launched, email submitted to password reset )
    '''

    # get the path of ChromeDriverServer
    dir_str = os.getcwd()
    chrome_driver_path = dir_str + "/chromedriver 3"

    # create a new Chrome session
    driver = webdriver.Chrome(chrome_driver_path)

    # navigate to the application home page
    driver.get(URL_str)

    # get the search textbox
    search_field = driver.find_element_by_name(element_name)
    search_field.clear()

    # enter search keyword and submit
    search_field.send_keys(email_adr)
    search_field.send_keys(Keys.RETURN)


if __name__ == "__main__":
    api_obj = set_up_google_api('client_secret.json')
    email = get_email(api_obj, '<GoogleSheetID>', 'Sheet1!C2')
    password_reset(email, "https://myaccount.nytimes.com/seg/forgot-password",
                                                                        "email")
