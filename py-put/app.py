import os

import boto3
from flask import Flask, jsonify, make_response, request
from botocore.exceptions import ClientError
import logging
from model.user import User

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


dynamodb_client = boto3.client("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]


@app.route("/user/<uuid>", methods=["PUT"])
def update_user(uuid):
    body = request.get_json(silent=True)
    if not body:
        return make_response(
            jsonify({"error": "Can't update user with provided data"}), 400
        )

    update_expression = []
    expression_attribute_values = {}
    expression_attribute_names = {}

    if "name" in body:
        update_expression.append("#n = :name")
        expression_attribute_values[":name"] = {"S": body["name"]}
        expression_attribute_names["#n"] = "name"

    if "email" in body:
        update_expression.append("#e = :email")
        expression_attribute_values[":email"] = {"S": body["email"]}
        expression_attribute_names["#e"] = "email"

    if not update_expression:
        return make_response(
            jsonify({"error": "Can't update user with provided data"}), 400
        )

    try:
        response = dynamodb_client.update_item(
            TableName=TABLE_NAME,
            Key={"id": {"S": uuid}},
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ConditionExpression="attribute_exists(id)",
            ReturnValues="ALL_NEW",
        )
        updated_attributes = response.get("Attributes", {})
        user = User.from_dynamodb(updated_attributes)
        return make_response(jsonify({"data": user.to_dict()}), 200)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return make_response(jsonify({"error": "User not found"}), 404)
        else:
            logger.error(f"Unexpected error updating user {uuid}: {e}", exc_info=True)
            return make_response(jsonify({"error": "Server error"}), 500)


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error="Not found!"), 404)
