# import statements
import boto3
import decimal
import json
from pprint import pprint

# open file, we use json.load because the file is an object
with open('usgs_api.json') as access_json:
    quakes = json.load(access_json, parse_float=decimal.Decimal)

# create a variable for the earthquake features
quake_features = quakes['features']
# create a empty dictionary
dynamo_list = []
i = 0
while i < len(quake_features):
    for items in quake_features:
        quake_dic = {}
        quake_dic['quake_mag'] = quake_features[i]['properties']['mag']
        quake_dic['quake_time'] = quake_features[i]['properties']['time']
        quake_dic['quake_updated'] = quake_features[i]['properties']['updated']
        quake_dic['quake_long'] = quake_features[i]['geometry']['coordinates'][0]
        quake_dic['quake_lat'] = quake_features[i]['geometry']['coordinates'][1]
        quake_dic['quake_focaldepth'] = quake_features[i]['geometry']['coordinates'][2]
        quake_dic['id'] = quake_features[i]['id']
        dynamo_list.append(quake_dic)
        i += 1
# pprint(dynamo_list)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('earthquakedb03')
for i in range(0, len(dynamo_list)):
    table.put_item(Item=dynamo_list[i])