import requests, json
api_key = "369cf0dece4af158a73130d55460f8aa"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

city_name = "Portland"
current_url = base_url + "appid=" + api_key + "&q=" + city_name

response = requests.get(current_url)
x = response.json()
if x["cod"] != "404":
    y = x["main"]
    z = x["weather"]
    weather_description = z[0]["description"]

    # print following values
    print("The current weather in Portland, OR is " + str(weather_description) + ".")
    if("Rain" in str(weather_description) or "rain" in str(weather_description)):
      print("Yes, that means it is raining.")
    else:
      print("No rain currently.")
else:
    print(" City Not Found ")

new_url = "https://pro.openweathermap.org/data/2.5/forecast/hourly?"
next_url = new_url + "appid=" + api_key + "&q=" + city_name
#print(next_url)
response = requests.get(next_url)
x = response.json()
if x["cod"] != "404":
  rain = 0
  count = 0
  y = x["list"]
  for z in y:
    if(count <= 72):
      if("Rain" in str(z["weather"][0]["description"]) or "rain" in str(z["weather"][0]["description"])):
        rain = 1
    count = count + 1
  if(rain == 1):
    print("There is a forcast for rain in the next 3 days.")
  else:
    print("There is no signs of rain in the next 3 days")
else:
    print(" City Not Found ")
