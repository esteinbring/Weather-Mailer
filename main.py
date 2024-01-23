import logging

import config
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

    

    try:
        weather_forecast = ws.get_weather_forecast(config.latitude, config.longitude, config.timezone, config.forecast_days)

    except Exception as e:

        logging.error(f"Weather Mailing Service failed as the following error occured while trying to fetch the weather data: \n {e}")

        return

    try:
        content = ms.generate_email_content(weather_forecast, config.recipient_firstname, config.forecast_days, config.city)
        
        ms.send_email(config.recipient_email, content)

        logging.info("Weather Mailing Service finished")

    except Exception as e:

        logging.error(f"Weather Mailing Service failed as the following error occured while trying to send the e-mail: \n {e}")


if __name__ == "__main__":
    main()
