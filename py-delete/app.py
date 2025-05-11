import os

import boto3
from flask import Flask, jsonify, make_response, request
from botocore.exceptions import ClientError
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dynamodb_client = boto3.client("dynamodb")


TABLE_NAME = os.environ["TABLE_NAME"]


@app.route("/user/<uuid>", methods=["DELETE"])
def delete_user(uuid):
    try:
        dynamodb_client.delete_item(
            TableName=TABLE_NAME,
            Key={"id": {"S": uuid}},
            ConditionExpression="attribute_exists(id)",
        )
        return make_response("", 204)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return make_response(jsonify({"error": "User not found"}), 404)
        else:
            logger.error(f"Unexpected error deleting user {uuid}: {e}", exc_info=True)
            return make_response(jsonify({"error": "Server error"}), 500)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
