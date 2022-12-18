import requests
from datetime import datetime
import smtplib
from time import sleep

MY_EMAIL = "naraeshwarraj2@gmail.com"
MY_PASSWORD = "qmmddalfgmerpwrc"

MY_LAT = 17.385044
# Your latitude
MY_LONG = 78.486671
# Your longitude


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = (int(data["results"]["sunrise"].split("T")[1].split(":")[0]) + 6)
    sunset = (int(data["results"]["sunset"].split("T")[1].split(":")[0]) + 6)

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="eshwarraj.eshu@gmail.com",
                msg="Subject:Look Up\n\nThe ISS is above you in the sky."
            )
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="jahnavi95@gmail.com",
                msg="Subject:Look Up Sweetie....\n\nThe ISS is above you in the sky."
            )
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="javeedjd7866@gmail.com",
                msg="Subject:Look Up Sher!!\n\nThe ISS is above you in the sky."
            )

    time = datetime.now()
    hour = (time.hour % 12)
    minutes = time.minute
    print(hour)
    print(minutes)
    if hour == 5 and 0 >= minutes >= 3:
        parameter = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }
        response2 = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
        response2 = response2.json()
        sunset_hour = ((int(response2["results"]["sunset"].split("T")[1].split(":")[0]) + 5) % 12)
        sunset_minutes = (int(response2["results"]["sunset"].split("T")[1].split(":")[1]) + 30)

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection2:
            connection2.starttls()
            connection2.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection2.sendmail(from_addr=MY_EMAIL,
                                 to_addrs="eshwarraj.eshu@gmail.com",
                                 msg=f"Subject:Today's Sunset Time\n\nToday sun will set at "
                                     f"{sunset_hour}:{sunset_minutes} PM")

