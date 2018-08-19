'''
This script does the following:
- Go to Gmal inbox
- Find and read all the unread messages
- Extract details (Date, Sender, Subject, Snippet, Body) and export them to a .csv file / DB
- Mark the messages as Read - so that they are not read again
'''

'''
Before running this script, the user should get the authentication by following 
the link: https://developers.google.com/gmail/api/quickstart/python
Also, client_secret.json should be saved in the same directory as this file
'''

# Importing required libraries
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from bs4 import BeautifulSoup
import requests
import time
#import dateutil.parser as parser
from datetime import datetime
import datetime
import csv
import urllib2

# Creating a storage.JSON file with authentication details
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'  # we are using modify and not readonly, as we will be marking the messages Read
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'

# Getting all the unread messages from Inbox
# labelIds can be changed accordingly
unread_msgs = GMAIL.users().messages().list(userId='me', labelIds=['CATEGORY_PROMOTIONS']).execute()

# We get a dictonary. Now reading values for the key 'messages'
mssg_list = unread_msgs['messages']

#print "Total unread messages in inbox: "+str(len(mssg_list))

final_list = []
i = 1

for mssg in mssg_list:
    temp_dict = {}
    m_id = mssg['id']  # get id of individual message
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
    payld = message['payload']  # get payload of the message
    headr = payld['headers']  # get header of the payload

    # for one in headr:  # getting the Subject
    #     if one['name'] == 'Subject':
    #         msg_subject = one['value']
    #         if 'STUDENT COUPONS' in msg_subject:
    #             temp_dict['Subject'] = msg_subject
    #     else:
    #         pass
    #
    dateflag = False
    senderflag = False
    subjectflag = False
    for h in headr:  # getting the date
        if h['name'] == 'Date':
            msg_date = h['value']
            if 'Aug' in msg_date:
                dateflag = True
        if h['name'] == 'From':
            msg_from = h['value']
            temp_dict['Sender'] = msg_from
            if 'Best Buy Student Deals' in msg_from:
                senderflag = True
        if h['name'] == 'Subject':
            msg_subject = h['value']
            if 'Check out these STUDENT COUPONS' in msg_subject:
                subjectflag = True
        else:
            pass

    if dateflag and senderflag and subjectflag:
        # Fetching message body
        #mssg_parts = payld['parts']  # fetching the message parts
        #part_one = mssg_parts[0]  # fetching first element of the part
        part_body = payld['body']  # fetching body of the message
        part_data = part_body['data']  # fetching data from the body
        clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one))  # decoding from Base64 to UTF-8
        print clean_two
        splitone = clean_two.split('==================================================')
        splittwo = splitone[0].split('\r\n')
        splitthree = splitone[2].split('\r\n')
        if splittwo[1] == splitthree[4]:
            #print i
            i = i + 1
            weburl = splittwo[1]
            content = urllib2.urlopen(weburl)
            soup = BeautifulSoup(content, "html.parser")
            t1 = soup.find_all('a')
            for t2 in t1:
                t3 = t2.get('href')
                if 'https://click.emailinfo2.bestbuy.com/?qs=' in t3:
                    r = requests.get(t3)
                    if 'https://pages.emailinfo2.bestbuy.com/page.aspx?' in r.url:
                        #print r.url
                        if r.url not in final_list:
                            final_list.append(r.url)
                        break

            #print soup
        # mssg_body is a readible form of message body
        # depending on the end user's requirements, it can be further cleaned
        # using regex, beautiful soup, or any other method
    else:
        pass
for final in final_list:
    print final
print len(final_list)
#     final_list.append(temp_dict)  # This will create a dictonary item in the final list
#
#     # This will mark the messagea as read
#     GMAIL.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()
#
# print ("Total messaged retrived: ", str(len(final_list)))
#
# '''
# The final_list will have dictionary in the following format:
# {	'Sender': '"email.com" <name@email.com>',
# 	'Subject': 'Lorem ipsum dolor sit ametLorem ipsum dolor sit amet',
# 	'Date': 'yyyy-mm-dd',
# 	'Snippet': 'Lorem ipsum dolor sit amet'
# 	'Message_body': 'Lorem ipsum dolor sit amet'}
# The dictionary can be exported as a .csv or into a databse
# '''
#
# exporting the values as .csv
