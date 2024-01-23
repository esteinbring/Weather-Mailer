# Weather-Mailer

This project uses Open-Meteo's API to get a weather forecast for the next 14 days.  The default location is Berlin (Mitte), but can be freely defined using longitude and latitude. \
The weather data returned includes the minimum and maximum temperature in degrees Celsius, as well as the probability of precipitation in percent and wind speed in km/h. \
The data is formatted in a HTML table and sent using Google's SMTP Gmail server to a freely definable e-mail recipient with a personal salutation.

## Email
This is how an e-mail to Lisa would like:

![Bildschirmfoto 2024-01-22 um 10 30 58](https://github.com/esteinbring/Weather-Mailer/assets/157313872/a8825ce7-4dcc-4d4c-ad23-763d6208a348)

## Setup 
1. Follow [Google's tutorial](https://support.google.com/mail/answer/185833?hl=en) to generate an App-Password for the gmail account that will send the weather-e-mails. 
2. Configure 2 environment variables which contain the credentials. \
   ```export SENDER_EMAIL="<GMAIL ADDRESS>"``` \
   ```export SENDER_PASSWORD="<GMAIL APP PASSWORD>"```
3. Configure the recipient email & firstname in the config.py file. \
   ```recipient_firstname = '<RECIPIENT MAIL ADDRESS>``` \
   ```recipient_email = '<RECIPIENT FIRSTNAME>'``` \
4. Schedule the Weather-Mailer with crontab. The following cronjob will run the python script every 2 Mondays at 12 a.m. \
```0 0 1-7,15-21 * * . path/to/profile-with-env-variables/.profile && [ `date +\%a` = Mon ] -eq 1 ] && cd /path/to/directory && python3 main.py```
