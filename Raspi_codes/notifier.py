import boto3
from twilio.rest import Client

def alert_send():
    ACCESS_KEY = "<AWS ACCESS KEY>"
    SECRET_KEY = "<AWS SECRET KEY>"
    account_sid = "<TWILIO ACC SID>"
    auth_token = "<TEILIO ACC AUTH TOKEN>"
    
    #AWS
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    
    with open("/home/pi/Desktop/Raspi_codes/fire.mp4", "rb") as f:
        s3.upload_fileobj(f, "<AWS bucket name>", "fire.mp4",ExtraArgs={"ACL": "public-read","ContentType": "video/mp4"})
    
    #Twilio
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
                body="Fire Alert!! The Raspi has detected fire. Please check your WhatsApp to recieve a video clip of the event, recorded from Raspi camera",
                from_='<TWILIO WHATSAPP NUMBER>',
                to='<RECIEVER NUMBER>'
         )
    message = client.messages \
        .create(
                media_url=['https://<AWS bucket>.s3.<AWS region>.amazonaws.com/<file name>.mp4'],
                from_='whatsapp:<TWILIO WHATSAPP NUMBER>',
                to='whatsapp:<RECIEVER NUMBER>'
         )
        
