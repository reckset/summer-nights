import json
import requests
from bs4 import BeautifulSoup
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # Stats location and player name
    url = 'https://www.nfl.com/players/george-pickens/stats/logs/2023/'
    receiverName = 'George Pickens'
    
    # Get html page
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # There are 2 tables on the page, pre-season and regular season. Get all tables and use 2nd instance
        tables = soup.find_all('table', {'class': 'd3-o-table d3-o-standings--detailed d3-o-table--sortable {sortlist: [[0,1]]}'})
        
        # Iterate rows in table which represent each week. Store TDs for that week in DynamoDB
        for row in tables[1].find_all('tr')[1:]:
            columns = row.find_all('td')
            
            # Set current week so we can map to DynamoDB table
            currentWeek = 'Week' + columns[0].text.strip()
            
            # Get DynamoDB service
            dynamodb = boto3.client('dynamodb')
            
            # Update attribute value for current week
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