const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");

const {
  DynamoDBDocumentClient,
  GetCommand,
} = require("@aws-sdk/lib-dynamodb");

const express = require("express");
const serverless = require("serverless-http");
const User = require('./model/User');

const app = express();

const TABLE_NAME = process.env.TABLE_NAME;
const client = new DynamoDBClient();
const docClient = DynamoDBDocumentClient.from(client);

app.use(express.json());

app.get("/user/:uuid", async (req, res) => {
  const params = {
    TableName: TABLE_NAME,
    Key: {
      id: req.params.uuid,
    },
  };

  try {
    const { Item } = await docClient.send(new GetCommand(params));
    return Item
      ? res.json({ data: User.fromItem(Item) })
      : res.status(404).json({ error: "User not found" });
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: "Could not retrieve user" });
  }
});


app.use((req, res, next) => {
  return res.status(404).json({
    error: "Not Found",
  });
});

exports.handler = serverless(app);
