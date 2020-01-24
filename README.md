<h1 align="center">
  <br>
  <a href="https://github.com/luxunator/weebmyip"><img src="https://i.ibb.co/vcSzLbq/weebmyip.png" alt="logo"></a>
</h1>
<p align="center">
  <a href="https://github.com/luxunator/weebmyip/releases">
    <img src="https://img.shields.io/github/release/luxunator/weebmyip.svg">
  </a>
  <a href="https://github.com/pallets/flask">
    <img src="https://img.shields.io/badge/flask-1.0.2-orange">
  </a>
  <a href="https://github.com/luxunator/weebmyip">
      <img src="https://img.shields.io/github/stars/luxunator/weebmyip">
  </a>
</p>
<h4 align="center">flask app with a rest api to get information on IP addresses, and of course an anime girl to read you it</h4>

### Features
- Loli voice
- Web API
- Playing Crabrave when you get banned

### Technologies Used
- [MaxMind](https://dev.maxmind.com/)
- [IP2Proxy](https://www.ip2location.com)
- [APNIC](http://thyme.apnic.net/)

### API
<h4>curl usage:</h4>

``` 
curl https://[domain]/api/v1?ip=8.8.8.8&data=all"

{
  "status": "true", 
  "IP": "8.8.8.8", 
  "audio": "/static/generated/8-8-8-8.mp3", 
  "country_name": "United States", 
  "country_iso_code": "US", 
  "subdiv": "California", 
  "subdiv_iso_code": "CA", 
  "city": "Mountain View", 
  "postal_code": "94035", 
  "latitude": 37.751, 
  "longitude": -97.822, 
  "isp": "GOOGLE - Google LLC, US", 
  "asn": 15169, 
  "proxy_type": "DCH"
}
```

<h4>multiple values:</h4>

``` 
curl https://[domain]/api/v1?ip=8.8.8.8&data=audio,isp,asn"

{
  "audio": "/static/generated/8-8-8-8.mp3", 
  "isp": "GOOGLE - Google LLC, US", 
  "asn": 15169
}
```


### Demo
[weebmyip.pythonanywhere.com](https://weebmyip.pythonanywhere.com)

