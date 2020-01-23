import os
import geoip2.database
import re as ree
import time
import IP2Proxy
import custom_
from threading import Thread
from audio import WeebGen, WeebDel
from flask import Flask, request, render_template, jsonify
from config import home_dir, allowed_requests, clear_ban, error_emotes

db = IP2Proxy.IP2Proxy()
db.open(home_dir+"DB/IP2PROXY-LITE-PX.BIN")
reader = geoip2.database.Reader(home_dir+'DB/GeoLite2-City.mmdb')
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

dedasn = custom_.dedasn()
Data = {}
IP_bans = []
IP_Regex = r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$'


def ip_audio(IP):
    IPfile = str(IP).replace('.', '-')
    if not os.path.exists(home_dir+'static/generated/'+IPfile+'.mp3'):
        WeebGen(IP)
        thread = Thread(target=WeebDel, args=(IP,))
        thread.daemon = True
        thread.start()
    return '/static/generated/'+IPfile+'.mp3'


def clear_bans():
    while True:
        time.sleep(clear_ban)
        IP_bans.clear()


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
@app.route("/basic", methods=['GET'])
def home():
    IP_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    Data = {
        'title': 'Home',
        'IP': IP_addr,
        'audio': ip_audio(IP_addr),
    }
    return render_template('home.html', data=Data)


@app.route("/", methods=['POST'])
@app.route("/home", methods=['POST'])
@app.route("/basic", methods=['POST'])
def home_post():
    IP = request.form['ip']
    IP_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    Data = {
        'title': 'Home',
        'IP': IP,
    }
    if ree.match(IP_Regex, IP):
        if IP_bans.count(IP_addr) < allowed_requests:
            Data['audio'] = ip_audio(IP)
            IP_bans.append(IP_addr)
        else:
            Data['audio'] = 'static/crab/crabrave.mp3'
            Data['error'] = 'Your IP Gone, You\'re on cooldown'
            Data['emote'] = error_emotes['cooldown']
    else:
        Data['IP'] = ''
        Data['audio'] = 'static/crab/baka.mp3'
        Data['error'] = 'Invalid IP address'
        Data['emote'] = error_emotes['invalid']
    return render_template('home.html', data=Data)


@app.route("/advanced", methods=['GET'])
def advanced():
    IP_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    UA = request.headers.get('User-Agent')
    Data = {
        'title': 'Advanced',
        'IP': IP_addr,
        'user_agent': UA,
        'audio': ip_audio(IP_addr),
        'proxy_type': db.get_proxy_type(IP_addr),
        'self_ip': IP_addr,
    }
    try:
        response = reader.city(IP_addr)
        re = dedasn.isp(IP_addr)
        Data['country_name'] = response.country.name
        Data['country_iso_code'] = response.country.iso_code
        Data['subdiv'] = response.subdivisions.most_specific.name
        Data['subdiv_iso_code'] = response.subdivisions.most_specific.iso_code
        Data['city'] = response.city.name
        Data['postal_code'] = response.postal.code
        Data['latitude'] = response.location.latitude
        Data['longitude'] = response.location.longitude
        Data['ISP'] = re['isp']
        Data['ASN'] = re['asn']
        Data['proxy_type'] = db.get_proxy_type(IP_addr)
        
    except Exception:
        Data['error'] = 'IP address not in database'
        Data['emote'] = error_emotes['database']
    return render_template('advanced.html', data=Data)


@app.route("/advanced", methods=['POST'])
def advanced_post():
    IP = request.form['ip']
    UA = request.headers.get('User-Agent')
    IP_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    Data = {
        'title': 'Advanced',
        'IP': IP,
        'user_agent': UA,
        'proxy_type': db.get_proxy_type(IP),
        'self_ip': IP_addr,
    }
    if ree.match(IP_Regex, IP):
        if IP_bans.count(IP_addr) < allowed_requests:
            try:
                response = reader.city(IP)
                re = dedasn.isp(IP)
                Data['audio'] = ip_audio(IP)
                Data['country_name'] = response.country.name
                Data['country_iso_code'] = response.country.iso_code
                Data['subdiv'] = response.subdivisions.most_specific.name
                Data['subdiv_iso_code'] = response.subdivisions.most_specific.iso_code
                Data['city'] = response.city.name
                Data['postal_code'] = response.postal.code
                Data['latitude'] = response.location.latitude
                Data['longitude'] = response.location.longitude
                Data['ISP'] = re['isp']
                Data['ASN'] = re['asn']
                IP_bans.append(IP_addr)
            except Exception:
                Data['audio'] = ip_audio(IP)
                Data['error'] = 'IP address not in database'
                Data['emote'] = error_emotes['database']
        else:
            Data['audio'] = 'static/crab/crabrave.mp3'
            Data['error'] = 'Your IP Gone, You\'re on cooldown'
            Data['emote'] = error_emotes['cooldown']
    else:
        Data['IP'] = ''
        Data['audio'] = 'static/crab/baka.mp3'
        Data['error'] = 'Invalid IP address'
        Data['emote'] = error_emotes['invalid']
    return render_template('advanced.html', data=Data)


@app.route("/api", methods=['GET', 'POST'])
def API():
    Data = {'title': 'API'}
    return render_template('api.html', data=Data)


@app.route("/about", methods=['GET', 'POST'])
def about():
    Data = {'title': 'About'}
    return render_template('about.html', data=Data)


@app.route("/api/v1", methods=['GET', 'POST'])
def api():
    IP = str(request.args.get('ip'))
    IP_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    Type = str(request.args.get('data'))
    error_ = {'status': 'error', 'message': 'error message'}
    if IP == '127.0.0.1' or IP.lower() == 'localhost':
        error_['message'] = 'localhost: your peepee is smoll'
        return jsonify(error_)
    elif ree.match(IP_Regex, IP):
        if IP_bans.count(IP_addr) < allowed_requests:
            Data = {}
            try:
                response = reader.city(IP)
                resp = dedasn.isp(IP)
                Data = {
                    'status': 'true',
                    'IP': IP,
                    'audio': ip_audio(IP),
                    'country_name': response.country.name,
                    'country_iso_code': response.country.iso_code,
                    'subdiv': response.subdivisions.most_specific.name,
                    'subdiv_iso_code': response.subdivisions.most_specific.iso_code,
                    'city': response.city.name,
                    'postal_code': response.postal.code,
                    'latitude': response.location.latitude,
                    'longitude': response.location.longitude,
                    'isp': resp['isp'],
                    'asn': resp['asn'],
                    'proxy_type': db.get_proxy_type(IP),
                }
                IP_bans.append(IP_addr)
                if Type == 'all' or Type == 'None':
                    return jsonify(Data)
                else:
                    new_Data = {}
                    Type = Type.split(',')
                    for i in Type:
                        new_Data[i] = Data[i]
                    return jsonify(new_Data)
            except Exception:
                error_['message'] = 'IP not in database or wrong data type'
                return jsonify(error_)
        else:
            error_['message'] = 'You\'ve achieved your limit, fucc off sir'
            return jsonify(error_)
    else:
        error_['message'] = 'Invalid IP Address'
        return jsonify(error_)


if __name__ == "__main__":
    thread1 = Thread(target=clear_bans)
    thread1.daemon = True
    thread1.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
