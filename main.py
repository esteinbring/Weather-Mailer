import logging
import mailing_service as ms
import weather_service as ws


def main():

    logging.basicConfig(filename='weathermail.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    encoding='utf-8',
                    level=logging.INFO)

    logging.info("Weather Mailing Service started")

    # Location of the Berliner Fernsehturm
    latitude = 52.52081
    longitude = 13.40941
    timezone = 'Europe/Berlin'
    city = 'Berlin'

    # Insert the information for the person who will receive the weather data here
    recipient_firstname = '<RECIPIENT FIRSTNAME>'
    recipient_email = '<RECIPIENT E-MAIL ADDRESS>'

    forecast_days = 14

    try:
        weather_forecast = ws.get_weather_forecast(latitude, longitude, timezone, forecast_days)

    except Exception as e:

        logging.error(f"Weather Mailing Service failed as the following error occured while trying to fetch the weather data: \n {e}")

        return

    try:
        content = ms.generate_email_content(weather_forecast, recipient_firstname, forecast_days, city)
        
        ms.send_email(recipient_email, content)

        logging.info("Weather Mailing Service finished")

    except Exception as e:

        logging.error(f"Weather Mailing Service failed as the following error occured while trying to send the e-mail: \n {e}")


if __name__ == "__main__":
    main()
