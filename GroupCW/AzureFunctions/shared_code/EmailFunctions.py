# Azure Imports
from azure.communication.email import EmailClient
# Code Base Imports
import AzureData

async def sendEmail(userInfo, randomPassword, ref):

    client = EmailClient(AzureData.emailEndpoint, AzureData.emailCredential)    

    text = "Your password has been reset to: {}\n Please sign in and follow instructions".format(randomPassword)

    message = {
        "senderAddress": AzureData.emailDomainName,
        "recipients": {
            "to": [
                {
                    "address": userInfo.get("email"),
                    "displayName": userInfo.get("username")
                }
            ]
        },
        "content": {
            "subject": "Password Reset, Reference:{}".format(ref),
            "plainText": text
        }
    }

    #poller = EmailClient.begin_send(client, message)
    poller = client.begin_send(message)
    return poller.result()