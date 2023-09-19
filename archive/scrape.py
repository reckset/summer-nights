import json
import requests
from bs4 import BeautifulSoup
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, date

def lambda_handler(event, context):
    # URLs to scrape from
    # The stats tables on nfl.com have multiple pages, while each page has its own url there does not appear
    # to be any kind of pattern. Therefore, manually managing these urls
    # urls = [ ]
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/reg/all/receivingreceptions/desc')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAGQAAABVAJgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhNU0lzSWpNeU1EQTBPRFJtTFRVd01UWXRNVFV3TUMxaVptSmxMV000TjJJeU9USmlOak01WXlJc0lqSXdNak1pWFgwPQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAMgAAACRAIgAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STVJaXdpTXpJd01EVTNOREV0TkdNMU1DMDVNRFF3TFRZM1pEWXRNRFF5TmpreFptSTFNelZoSWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAASwAAAEBAHAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STNJaXdpTXpJd01EVTNORGd0TkRrek9TMHpNVEV3TFRrd00yVXRObUkyWXpnMk9HUmtNMkZpSWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAZAAAAE1AGAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STJJaXdpTXpJd01EVTNORGt0TkdNME1TMDFNelU1TFRnd09XSXRZMkZsWVdFeFpHSTROR1F3SWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAfQAAAGVAFAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STFJaXdpTXpJd01EVXlORGt0TkRNeE5TMHlPVEUyTFdObE56UXRPV0UyT1dVME5qbG1PVFF3SWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAlgAAAIVAEAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5STBJaXdpTXpJd01EVXdOREV0TkdNME5TMHhOakkxTFdWaU9UTXRZekpqT1dJeE1XTTBNREEySWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAArwAAAJ1ACAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXpJaXdpTXpJd01EUmtOR1l0TkdZeU55MDVOekl6TFROak56VXRNR1V3T0RKaVl6SXdNR001SWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAAyAAAAL5AAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EUTBOVFV0TkdNeU5pMDVOamd4TFRZNVpEQXRPVE5sTXpCaFlqWXpPRE01SWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAA4QAAAL5AAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXlJaXdpTXpJd01EVTNORFV0TkdNek5pMHhNRFE0TFdSaE9UQXRNbVl4WVdVeU56TXpPR0ptSWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAAA-gAAAOY_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EUTROREV0TlRJd05pMDVOVEl3TFRsbE56QXRaRFUxT1Rjek9URmtPR013SWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAABEwAAAOY_8AAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXhJaXdpTXpJd01EVXlOR1l0TlRNMk1TMDJORGMyTFdZMFptSXROVEJtTURsbE5ETTNNRGM1SWl3aU1qQXlNeUpkZlE9PQ==')
    # urls.append('https://www.nfl.com/stats/player-stats/category/receiving/2023/REG/all/receivingreceptions/DESC?aftercursor=AAABLAAAAR4AAAAAAAAAADFleUp6WldGeVkyaEJablJsY2lJNld5SXdJaXdpTXpJd01EUmlORGt0TlRJM01DMDJOekE1TFdVME1HTXRPRE14WkdRNU9UZGlPRGRqSWl3aU1qQXlNeUpkZlE9PQ==')
    # # Determine which NFL week we are in
    # today = datetime.today()
    # seasonStart = date(year = 2023, month = 9, day = 7)
    # seasonCurrent = date(year = today.year, month = today.month, day = today.day)
    
    # dateDelta = seasonCurrent - seasonStart
    # numberOfDays = dateDelta.days
    
    # if (numberOfDays < 7):
    #     weekCount = 1
    # elif (numberOfDays < 14):
    #     weekCount = 2
    # elif (numberOfDays < 21):
    #     weekCount = 3
    # elif (numberOfDays < 28):
    #     weekCount = 4
    # elif (numberOfDays < 35):
    #     weekCount = 5
    # elif (numberOfDays < 42):
    #     weekCount = 6
    # elif (numberOfDays < 49):
    #     weekCount = 7
    # elif (numberOfDays < 56):
    #     weekCount = 8
    # elif (numberOfDays < 63):
    #     weekCount = 9
    # elif (numberOfDays < 70):
    #     weekCount = 10
    # elif (numberOfDays < 77):
    #     weekCount = 11
    # elif (numberOfDays < 84):
    #     weekCount = 12
    # elif (numberOfDays < 91):
    #     weekCount = 13
    # elif (numberOfDays < 98):
    #     weekCount = 14
    # elif (numberOfDays < 105):
    #     weekCount = 15
    # elif (numberOfDays < 112):
    #     weekCount = 16
    # else:
    #     weekCount = 0

    # currentWeek = "Week" + str(weekCount)
    
    # #Send an HTTP GET request to the url
    # for url in urls:
    #     foundGeorge = False
    #     response = requests.get(url)
    
    #     #Validate response
    #     if response.status_code == 200:
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         #Find table containing receiver statistics
    #         table = soup.find('table', {'class': 'd3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable'})
            
    #         #Initialize lists to store data
    #         player_names = [ ]
    #         touchdowns = [ ]
            
    #         #Iterate rows in table
    #         for row in table.find_all('tr')[1:]:
    #             columns = row.find_all('td')
    #             player_names.append(columns[0].text.strip())
    #             touchdowns.append(columns[3].text.strip())
    
    #         for i in range(len(player_names)):
    #             if player_names[i] == 'George Pickens':
    #                 receiverName = player_names[i]
    #                 receiverTDs = touchdowns[i]
    #                 # Get service
    #                 dynamodb = boto3.client('dynamodb')
                    
    #                 # Get player
    #                 player = dynamodb.get_item(
    #                     TableName = 'Touchdowns',
    #                     Key = {
    #                         'PlayerId': {'S': receiverName}
    #                     })
                    
    #                 # Determine how many touchdowns from previous weeks
    #                 previousTouchdowns = 0
    #                 for i in range(1, weekCount):
    #                     previousWeek = "Week" + str(i)
    #                     previousTouchdowns += int((player["Item"][previousWeek]["N"]))
                    
    #                 newTouchdowns = int(receiverTDs) - previousTouchdowns
                    
    #                 response = dynamodb.update_item(
    #                     TableName = 'Touchdowns',
    #                     Key={
    #                         'PlayerId': {'S': receiverName}
    #                     },
    #                     AttributeUpdates={
    #                         currentWeek: {
    #                             "Action": "PUT", "Value": {'N': str(newTouchdowns)}
    #                         }
    #                     }
    #                 )
                    
    #                 value = {
    #                     "player": str(receiverName),
    #                     "week": str(weekCount),
    #                     "totalTouchdowns": str(receiverTDs),
    #                     "previousTouchdowns": str(previousTouchdowns),
    #                     "newTouchdowns": str(newTouchdowns)
    #                 }
                    
    #                 return {
    #                     'statusCode': str(200),
    #                     'body': json.dumps(value),
    #                     'headers': {
    #                         'Content-Type': 'application/json',
    #                         'Access-Control-Allow-Headers': 'Content-Type',
    #                         'Access-Control-Allow-Origin': '*'
    #                     },
    #                 }
    
    #     else:
    #         print("Failed to retrieve webpage")
    
    
    url = 'https://www.nfl.com/players/george-pickens/stats/logs/2023/'
    receiverName = 'George Pickens'
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        #Find table containing receiver statistics
        tables = soup.find_all('table', {'class': 'd3-o-table d3-o-standings--detailed d3-o-table--sortable {sortlist: [[0,1]]}'})
        
        #Iterate rows in table
        for row in tables[1].find_all('tr')[1:]:
            columns = row.find_all('td')
            
            currentWeek = 'Week' + columns[0].text.strip()
            
            # Get service
            dynamodb = boto3.client('dynamodb')
            
            dbResponse = dynamodb.update_item(
                TableName = 'Touchdowns',
                Key={
                    'PlayerId': {'S': receiverName}
                },
                AttributeUpdates={
                    currentWeek: {
                        "Action": "PUT", "Value": {'N': str(columns[8].text.strip())}
                    }
                }
            )
        
        value = {
            "player": str(receiverName),
        }
        
        return {
            'statusCode': str(200),
            'body': json.dumps(value),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*'
            },
        }