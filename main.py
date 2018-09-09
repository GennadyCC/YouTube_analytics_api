# -*- coding: utf-8 -*-

import sys
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import webbrowser as wb
import json

# credentials
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret.json'

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # credentials = flow.run_console()
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

# request
def execute_api_request(client_library_function, **kwargs):
    response = client_library_function(**kwargs).execute()
    return response

# main
if __name__ == '__main__':
    dat = []
    # reading txt file
    with open('./report_setup.json') as f:
        data = json.load(f)
    
    # request
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    youtubeAnalytics = get_service()
    data = execute_api_request(
        youtubeAnalytics.reports().query,
        ids=data['Id'],
        startDate=data['Start'],
        endDate=data['End'],
        metrics=data['Metrics'],
        dimensions=data['Dimensions'],
        sort='',
        # filters='video==DW7P1dsFWB8'
        # filters='isCurated==1;playlist==PL98Ww2k89IYRyw26898KJUG4AEmH-oYpP'   
        filters=data['Filters'] 
    )

    # data parsing, create csv file
    columns = data['columnHeaders']
    rows = data['rows']

    with open('output_file.csv', 'w') as csv_file:
        for i in range(len(columns)):
            csv_file.write(columns[i]['name'])
            if i < len(columns)-1:
                csv_file.write(',')
        csv_file.write('\n')

        for a in range(len(rows)):

            for b in range(len(rows[a])):
                csv_file.write(str(rows[a][b]))
                if b < len(rows[a])-1:
                    csv_file.write(',')
            csv_file.write('\n')




