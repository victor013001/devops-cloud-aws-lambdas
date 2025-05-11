const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");

const {
  DynamoDBDocumentClient,
  PutCommand,
} = require("@aws-sdk/lib-dynamodb");

const express = require("express");
const serverless = require("serverless-http");
const { v4: uuidv4 } = require('uuid');
const User = require('./model/User');

const app = express();

const TABLE_NAME = process.env.TABLE_NAME;
const client = new DynamoDBClient();
const docClient = DynamoDBDocumentClient.from(client);

app.use(express.json());

app.post("/user", async (req, res) => {
  const { name, email } = req.body;
  if (!name || !email) {
    return res.status(400)
      .json({
        error: "Can't create user with provided data"
      });
  }

  const uuid = uuidv4();
  const user = new User(uuid, name, email);
  const params = {
    TableName: TABLE_NAME,
    Item: user.toJSON(),
  };

  try {
    await docClient.send(new PutCommand(params));
    return res.status(201)
      .json({
        data: user,
      });
  } catch (error) {
    console.error(TABLE_NAME);
    res.status(500).json({ error: "Could not create user" });
  }
});

app.use((req, res, next) => {
  return res.status(404).json({
    error: "Not Found",
  });
});

exports.handler = serverless(app);
