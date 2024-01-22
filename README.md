# Weather-Mailer

This project uses Open-Meteo's API to get a weather forecast for the next 14 days.
It then formats the data and forwards it via SMTP over Google's Gmail Server to an e-mail address of your choice.

## Email
This is how an e-mail to Theresa would like:

![Bildschirmfoto 2024-01-22 um 09 19 13](https://github.com/esteinbring/Weather-Mailer/assets/157313872/eea907cc-ae38-470b-9da6-64ce90c19b97)

## Setup 
1. Follow [Google's tutorial](https://support.google.com/mail/answer/185833?hl=en) to generate an App-Password for the gmail account that will send the weather-e-mails. 
2. Configure 2 environment variables which contain the credentials. \
   ```export SENDER_EMAIL="<GMAIL ADDRESS>"``` \
   ```export SENDER_PASSWORD="<GMAIL APP PASSWORD>"```
3. Configure the recipient email & firstname in the main.py file. \
   ```recipient_firstname = '<RECIPIENT MAIL ADDRESS>``` \
   ```recipient_email = '<RECIPIENT FIRSTNAME>'``` \
4. Schedule the Weather-Mailer with crontab. The following cronjob will run the python script every 2 Mondays at 12 a.m. \
```0 0 1-7,15-21 * * . path/to/profile-with-env-variables/.profile && [ `date +\%a` = Mon ] -eq 1 ] && cd /path/to/directory && python3 main.py```
