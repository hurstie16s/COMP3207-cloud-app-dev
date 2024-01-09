# Code Base Imports
import AzureData

async def sendEmail(userInfo, text, ref):   

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
    poller = AzureData.emailClient.begin_send(message)
    return poller.result()