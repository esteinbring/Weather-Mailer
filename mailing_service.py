import logging
import os
import smtplib


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table


def send_email(recipient_email, content):

    logging.info(f'Connecting to Gmail SMTP server and sending an e-mail to "{recipient_email}"...')

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = content['subject']

    message.attach(MIMEText(content['body'], 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(message['From'], sender_password)
        server.sendmail(message['From'], message['To'], message.as_string())

    logging.info(f'Successfully send an e-mail to "{recipient_email}".')


def generate_email_content(dataframe, firstname, forecast_days, location):
        
        logging.info(f'Generating mail-content for "{firstname}"...')
        
        weather_table = build_table(dataframe, 'grey_dark')

        subject = str(forecast_days) + '-Day Weather Forecast For ' + location

        body = """\
                    <html>
                        <body>
                            <p> Hi {firstname},
                                <br>
                                <br>
                                here is a forecast for the weather in {location} over the next {forecast_days} days:
                            </p>
                            <br>
                            {weather_table}
                            <br>
                            <br>
                            <p> This is an automatically generated e-mail! 
                                <br>
                                Please do not respond to it.
                                <br>
                                <br>
                                If you encounter an error or have suggestions for improvement, please contact the developer:
                                <br>
                                Erik Steinbring
                                <br>steinbring.erik@gmail.com
                            </p>
                        </body>
                    </html>
                    """.format(firstname=firstname, location=location, forecast_days=forecast_days, weather_table=weather_table)
        
        content = {
            'subject': subject,
            'body': body,
        }

        logging.info(f'Successfully generated mail-content.')

        return content
