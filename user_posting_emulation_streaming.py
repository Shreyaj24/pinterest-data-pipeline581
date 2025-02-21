import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)

#pin_invoke_url = "https://8marlud1ff.execute-api.us-east-1.amazonaws.com/test/topics/0ac1babf620d.pin"
#geo_invoke_url =  "https://8marlud1ff.execute-api.us-east-1.amazonaws.com/test/topics/0ac1babf620d.geo"
#user_invoke_url = "https://8marlud1ff.execute-api.us-east-1.amazonaws.com/test/topics/0ac1babf620d.user"  
invoke_url = "https://p1490bzg76.execute-api.us-east-1.amazonaws.com/dev/streams/Kinesis-Prod-Stream/record"
                
class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()

def send_to_kafka(api_invoke_url, payload):
                headers = {'Content-Type': 'application/json'}
                response = requests.put(api_invoke_url , headers=headers, data=payload)
                print(f'response code: {response.status_code}')
                print(response.content)


                

def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            
            #To send JSON messages we need to follow this structure
            payload_pin = json.dumps({
                "StreamName": "Kinesis-Prod-Stream",
                "Data":  
                    #Data should be send as pairs of column_name:value, with different columns separated by commas    
                    pin_result,
                "PartitionKey": "293c4352b869.pin"
            })
            payload_geo =json.dumps({
                "StreamName": "Kinesis-Prod-Stream",
                "Data":
                    {"ind": geo_result["ind"],"timestamp": str(geo_result["timestamp"]),"latitude"
            : geo_result["latitude"],"longitude":geo_result["longitude"],"country":geo_result["country"]},
                "PartitionKey": "293c4352b869.geo"
            })
            payload_user = json.dumps({
                "StreamName": "Kinesis-Prod-Stream",
                "Data":
                    {"ind": user_result["ind"],"first_name":user_result["first_name"],"last_name"
            : user_result["last_name"],"age": user_result["age"],"date_joined": str(user_result["date_joined"])},
                "PartitionKey": "293c4352b869.user"
            })

            send_to_kafka(invoke_url, payload_pin)
            send_to_kafka(invoke_url, payload_geo)
            send_to_kafka(invoke_url, payload_user)
            
            

            # print(pin_result)
            # print(geo_result)
            # print(user_result)
        #break

if __name__ == "__main__":
    run_infinite_post_data_loop()
    #print('Working')
    
    


