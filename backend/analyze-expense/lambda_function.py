import json
import uuid
import logging
from urllib.parse import unquote_plus
import boto3
import os
from addOn import process_error, extract_kv, extract_lineitems
import datetime
import socket
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('expenseTable')

bucketname = os.environ.get('bucketname')

# function will help create the json object needed
def extract_jsonText(response, extract_by="LINE"):
   
    # getting the current time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    # creating python object to hold json info
    extracted_data = {
        "supplierId": "",
        "reportType": "ORDER",
        "reportKey": "",
        "reportSubKey": "",
        "expenses": [
            {
                "name": "",
                "type": "Airport Fees",
                "media": [],
                "phone": {
                    "number": "",
                    "extnStr": "",
                    "areaCode": "",
                    "numberStr": "",
                    "countryCode": "",
                    "countryCodeStr": ""
                },
                "change": "N",
                "status": "PENDING",
                "address": {
                    "city": "",
                    "addr1": "",
                    "pcode": "",
                    "state": "",
                    "country": "United States of America"
                },
                "comment": "",
                "subType": "securityFee",
                "cardType": "",
                "currency": "USD",
                "lineItem": [
                    {
                        "id": 0,
                        "name": "",
                        "unit": "",
                        "count": 0,
                        "taxes": 0,
                        "baseCost": 0,
                        "refundable": "N",
                        "description": "",
                        "chargeObject": []
                    }
                ],
                "updatedBy": "3458",
                "updatedIp": IPAddr,
                "createdBy": "3458",
                "expenseId": 1,
                "newExpense": "N",
                "description": "",
                "paymentType": "",
                "totalCharge": "",
                "updatedDateTime": current_time,
                "chargedDateTime": current_time,
                "createdDateTime": current_time
            }
        ]
    }
    # do for loop through each line of the recipte
   
    for i in response["ExpenseDocuments"]: 
        for line in i["SummaryFields"]:
           
            # checking each line to find the text type
            #using a map
            type_to_key_map = {
                "NAME": ("expenses", 0, "name"),
                "VENDOR_PHONE": ("expenses", 0, "phone", "number"),
                "CITY": ("expenses", 0, "address", "city"),
                "ADDRESS": ("expenses", 0, "address", "addr1"),
                "ZIP_CODE": ("expenses", 0, "address", "pcode"),
                "STATE": ("expenses", 0, "address", "state"),
                "COUNTRY": ("expenses", 0, "address", "country"),
                "VISA": ("expenses", 0, "cardType", "paymentType")
            }

            for line_type, keys in type_to_key_map.items():
                if line.get("Type").get("Text") == line_type:
                    value = line.get("ValueDetection").get("Text")
                    if len(keys) == 3:
                        extracted_data[keys[0]][keys[1]][keys[2]] = value
                    elif len(keys) == 4:
                        extracted_data[keys[0]][keys[1]][keys[2]][keys[3]] = value
                    else:
                        print("end") # debug print statement
                        
    return extracted_data
    

def lambda_handler(event, context):
    textract = boto3.client("textract")
    s3_client = boto3.client("s3")
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj["s3"]["bucket"]["name"])
        filename = unquote_plus(str(file_obj["s3"]["object"]["key"]))
        filename.split("/")[-1].split(".")[0]
        key = f"analyze-expense-output/{filename.split('/')[-1].split('.')[0]}_{uuid.uuid4().hex}"
       
        print("bucketname: ", bucketname)
        print("filename: ", filename)
        print("Above the first try block")
        try:
            print("Running response")
            response = textract.analyze_expense(
                Document={
                    "S3Object": {
                        "Bucket": bucketname,
                        "Name": filename,
                    }
                }
            )
            print(json.dumps(response))
            extracted_data_list = []  # List to store extracted data from all ExpenseDocuments
            for i in response["ExpenseDocuments"]:
                print("above 2nd try block")
                try:
                    extract_kv(
                        i["SummaryFields"],
                        s3_client,
                        bucketname,
                        f"{key}/key_value.csv",
                    )
                except Exception as e:
                    error_msg = process_error()
                    logging.error(error_msg)
                try:
                    extract_lineitems(
                        i["LineItemGroups"],
                        s3_client,
                        bucketname,
                        f"{key}/lineitems.csv",
                    )
                    extracted_data = extract_jsonText(response)
                    extracted_data_list.append(extracted_data)  # Append extracted data to the list
                except Exception as e:
                    error_msg = process_error()
                    logging.error(error_msg)
            
            # After extracting data from all ExpenseDocuments, call put_data_to_dynamodb once
            for extracted_data in extracted_data_list:
                put_data_to_dynamodb(extracted_data, 'expenseTable')

        except Exception as e:
            logging.error(e)

    return {"statusCode": 200, "body": json.dumps("test")}

   
def put_data_to_dynamodb(extracted_data, table_name):
    try:
        # Scan the table and find the maximum id
        response = table.scan(ProjectionExpression='id')
        current_id = max(item['id'] for item in response['Items']) if response['Items'] else 0

        # Convert extracted_data to DynamoDB item format
        dynamodb_item = {
            'id': current_id + 1,  # increment id
            'supplierId': extracted_data['supplierId'],
            'reportType': extracted_data['reportType'],
            'reportKey': extracted_data['reportKey'],
            'reportSubKey': extracted_data['reportSubKey'],
            'expenses': extracted_data['expenses']
        }

        # Write data to DynamoDB table
        response = table.put_item(
            Item=dynamodb_item,
        )
        print("PutItem succeeded:", response)
    except Exception as e:
        print("Database Error:", e)
        logging.error(e)
        raise e
