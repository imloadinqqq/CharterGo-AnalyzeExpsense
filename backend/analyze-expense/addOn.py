

import sys
import io
import json
import traceback
import pandas as pd


# function to handle process format errors
def process_error():
    ex_type, ex_value, ex_traceback = sys.exc_info()
    traceback_string = traceback.format_exception(ex_type, ex_value, ex_traceback)
    error_msg = json.dumps(
        {
            "errorType": ex_type.__name__,
            "errorMessage": str(ex_value),
            "stackTrace": traceback_string,
        }
    )
    return error_msg


# function that uploads the data to the s3 bucket
def upload_to_s3(s3_client, csv_buffer, BUCKET_NAME, key):
    s3_client.put_object(Body=csv_buffer.getvalue(), Bucket=BUCKET_NAME, Key=key)


# function that extracts each line item in the recipt
def extract_lineitems(lineitemgroups, s3_client, BUCKET_NAME, key):
    items, price, row, qty = [], [], [], [] 
    t_items, t_price, t_row, t_qty = [], [], [], []
    t_items, t_price, t_row, t_qty = None, None, None, None
    for lines in lineitemgroups: # going through each line item group
        for item in lines["LineItems"]:
            for line in item["LineItemExpenseFields"]: # iterating through each line item's expense fields
                if line.get("Type").get("Text") == "ITEM": # if the type is ITEM... then
                    # t_items.append(line.get("ValueDetection").get("Text", ""))
                    t_items = line.get("ValueDetection").get("Text", "") # get the text value of the item

                if line.get("Type").get("Text") == "PRICE":
                    # t_price.append(line.get("ValueDetection").get("Text", ""))
                    t_price = line.get("ValueDetection").get("Text", "")

                if line.get("Type").get("Text") == "QUANTITY":
                    # t_qty.append(line.get("ValueDetection").get("Text", ""))
                    t_qty = line.get("ValueDetection").get("Text", "")

                if line.get("Type").get("Text") == "EXPENSE_ROW":
                    # t_row.append(line.get("ValueDetection").get("Text", ""))
                    t_row = line.get("ValueDetection").get("Text", "")

            if t_items: # if it isn't empty / NONE
                items.append(t_items) # add the items to the item list
            else:
                items.append("")
            if t_price:
                price.append(t_price)
            else:
                price.append("")
            if t_row:
                row.append(t_row)
            else:
                row.append("")
            if t_qty:
                qty.append(t_qty)
            else:
                qty.append("")
            t_items, t_price, t_row, t_qty = None, None, None, None

    df = pd.DataFrame() # creating dataFrame using pandas (kinda like a table or a two dimensionial array)
    df["items"] = items # adding "items" list to the dataFrame
    df["price"] = price
    df["quantity"] = qty
    df["row"] = row
    csv_buffer = io.StringIO() 
    df.to_csv(csv_buffer) # writing the dataFrame to the CSV
    upload_to_s3(s3_client, csv_buffer, BUCKET_NAME, key) # upload the csv to s3


# function that extracts key value pairs
def extract_kv(summaryfields, s3_client, BUCKET_NAME, key):
    field_type, label, value = [], [], []
    for item in summaryfields:
        try:
            field_type.append(item.get("Type").get("Text", ""))
        except:
            field_type.append("")
        try:
            label.append(item.get("LabelDetection", "").get("Text", ""))
        except:
            label.append("")
        try:
            value.append(item.get("ValueDetection", "").get("Text", ""))
        except:
            value.append("")

    df = pd.DataFrame()
    df["Type"] = field_type
    df["Key"] = label
    df["Value"] = value
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer)
    upload_to_s3(s3_client, csv_buffer, BUCKET_NAME, key)
