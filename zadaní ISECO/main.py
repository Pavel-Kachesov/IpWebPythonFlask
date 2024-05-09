from flask import Flask, render_template, request
import requests
import geoip2.webservice

app = Flask(__name__)

public_ip = requests.get('http://ip-api.com/json').json()


@app.route('/')
def home():
    public_ip = requests.get('http://ip-api.com/json').json()
    return render_template('index.html', public=public_ip)


def yes_or_no(i):
    if i:
        return "Yes"
    else:
        return "No"


@app.route('/lookup', methods=["GET", "POST"])
def lookup():
    ipData = ''
    ipAddress = ''
    if request.method == "POST":
        ipAddress = request.form.get("ipAddress")
        if ipAddress:
            with geoip2.webservice.Client(1006704, '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',
                                          'geolite.info') as client:
                ipData = client.city(ipAddress)

                eu = yes_or_no(ipData.country.is_in_european_union)
                flag = str.lower(ipData.country.iso_code)
                flag = f"https://flagcdn.com/w80/{flag}.png"
                flag = f"{flag}"

    return render_template('result.html', data=ipData, ipAddress=ipAddress, eu=eu, flag=flag)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
