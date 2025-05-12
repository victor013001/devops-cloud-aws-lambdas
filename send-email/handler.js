const { SNSClient, PublishCommand } = require("@aws-sdk/client-sns")

const snsClient = new SNSClient();
const TOPIC_ARN = "arn:aws:sns:us-east-1:842676005902:SendEmail";

exports.sendEmail = async (event) => {
  for (const record of event.Records) {
    const message = record.body;
    if (message) {
      const commandInput = {
        Subject: "Created user",
        TopicArn: TOPIC_ARN,
        Message: message,
      };

      try {
        await snsClient.send(new PublishCommand(commandInput))
        console.log("Messaje send to SNS", message);
      } catch (error) {
        console.error("Could not publish on SNS", error);
        throw error;
      }
    }
  }
};
