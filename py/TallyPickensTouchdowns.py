import json
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    # Get service
    dynamodb = boto3.client('dynamodb')
    
    touchdownsDave = 0
    touchdownsRex = 0
    touchdownsTim = 0
    
    # Get player
    player = dynamodb.get_item(
        TableName = 'Touchdowns',
        Key = {
            'PlayerId': {'S': 'George Pickens'}
        })
    
    for i in range(1,17):
        week = 'Week' + str(i)
        weekTouchdowns = (player["Item"][week]["N"])
        
        if (i == 1 or i == 4 or i == 8 or i == 11 or i == 14):
            touchdownsDave += int(weekTouchdowns)
        elif (i == 2 or i == 5 or i == 9 or i == 12 or i == 15):
            touchdownsRex += int(weekTouchdowns)
        elif (i == 3 or i == 7 or i == 10 or i == 13 or i == 16):
            touchdownsTim += int(weekTouchdowns)
    
    value = {
        "Dave": str(touchdownsDave),
        "Rex": str(touchdownsRex),
        "Tim": str(touchdownsTim)
    }
    
    return response(value, 200)
    
def response(value, statusCode):
    return {
        'statusCode': str(statusCode),
        'body': json.dumps(value),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*'
        },
    }