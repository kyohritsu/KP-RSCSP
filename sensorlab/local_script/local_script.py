#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import time, sleep
from datetime import datetime
from math import nan, isnan, fabs
import sys
import signal
import threading
import pyrebase
import smbus
import grovepi

# -----------------------------------------------------------------------------
# Firebase Console (https://console.firebase.google.com/) にアクセスして
# あなたのプロジェクトで Admin SDK でアクセスするための認証情報を
# 以下の変数に記入してください。

# ウェブ API キー
WEB_API_KEY = 'AIzaSyAUD7maqXOG-e99JqCgr3lXyBFyUqYqQfg'
# プロジェクト ID
PROJECT_ID = 'yourproject-1e84f'
# 秘密鍵 JSON ファイルへのパス
PATH_TO_CREDENTIAL_JSON = '/path/to/credential.json'
# -----------------------------------------------------------------------------

# 基板上のGroveモジュール接続先ピン番号を定義
GROVE_MOISTURE_PIN = 0  # 水分センサー (Moisture Sensor) → A0
GROVE_PIR_PIN = 16      # PIR モーションセンサー (PIR Motion Sensor) → A2(16)
GROVE_DHT_PIN = 0       # 温湿度センサー (Temperature & Humidity Sensor) → D0
GROVE_RELAY_PIN = 2     # リレー (Relay) → D2

# 定時出力の実行間隔 (秒)
OUTPUT_TASK_INTERVAL = 60.0

# 当アプリが使用するデータベース内のルート位置
DB_ROOT_PATH = 'sensorlab'

# 認証情報
config = {
    # ウェブ API キー
    'apiKey': WEB_API_KEY,
    # 認証先ドメイン
    'authDomain': PROJECT_ID + '.firebaseapp.com',
    # データベースの URL
    'databaseURL': 'https://' + PROJECT_ID + '.firebaseio.com',
    # ストレージ (今回はクラウドストレージを使わないので無記入)
    'storageBucket': '',
    # サービス アカウント
    'serviceAccount': PATH_TO_CREDENTIAL_JSON
}

def setup_gpio():
    '''GPIO で使用するピンをセットアップ'''
    grovepi.pinMode(GROVE_RELAY_PIN, 1)  # 出力
    grovepi.pinMode(GROVE_PIR_PIN, 0)    # 入力

def setup_accel(bus):
    '''加速度センサーをセットアップ'''
    # 加速度センサー MMA7660 (I2Cアドレス＝0x4c)
    # MODEレジスタ (0x07) に0x01をセットし、アクティブモードにする
    try:
        bus.write_byte_data(0x4c, 0x07, 0x01)
    except OSError:
        pass

def read_accel(bus):
    '''加速度センサーから XYZ 軸を読み取り、重力単位 (G) に変換'''
    try:
        # 受信データは3バイトで、[X軸, Y軸, Z軸] の順
        [x, y, z] = bus.read_i2c_block_data(0x4c, 0x00, 3)
    except OSError:
        return [nan, nan, nan]
    else:
        # 各軸の値は6ビットの“2の補数表現”
        #   (0～31)(32～63) → (0～+31)(-32～-1)
        # 数値32が1.5Gを表すため、1当たりは 1.5/32＝0.046875G
        u = 32 / 1.5
        gx = x / u if x <= 31 else (x - 64) / u if x <= 63 else nan
        gy = y / u if y <= 31 else (y - 64) / u if y <= 63 else nan
        gz = z / u if z <= 31 else (z - 64) / u if z <= 63 else nan
        return [gx, gy, gz]

def relay_state_changed(message):
    '''./relay/state が変更された際のコールバック関数'''
    # 新しい値が0であればリレーをオフに、0以外であればオンにする
    if message['event'] == 'put':
        if message['data'] == 0:
            print('relay: off')
            grovepi.digitalWrite(GROVE_RELAY_PIN, 0)
        else:
            print('relay: on')
            grovepi.digitalWrite(GROVE_RELAY_PIN, 1)

def generate_timestamp():
    '''データベース送信用のタイムスタンプ文字列を作成'''
    return datetime.utcfromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S.%f')

def get_moisture(pin):
    '''水分量を取得し、タイムスタンプを付加して辞書形式で返す'''
    data = {'timestamp': generate_timestamp()}
    value = None
    try:
        value = grovepi.analogRead(pin)
    except IOError:
        print('error: failed to read analog pin')
        return {}
    else:
        if 0 <= value <= 1023:
            data['value'] = value
            return data
        else:
            print('error: bad analog result')
            return {}

def get_dht(pin):
    '''温度・湿度を取得し、タイムスタンプを付加して辞書形式で返す'''
    data = {'timestamp': generate_timestamp()}
    temp = None
    humi = None
    try:
        [temp, humi] = grovepi.dht(pin, 0)
    except IOError:
        print('error: failed to communicate to dht sensor')
        return {}
    else:
        if isnan(temp) or isnan(humi):
            print('error: bad dht sensor result, sensor may be absent')
            return {}
        else:
            data['temperature'] = temp
            data['humidity'] = humi
            return data

def upload_worker(path, value):
    '''データベース送信本体'''
    if value != {}:
        print('upload: /' + path + ' <= ' + str(value))
        try:
            db.child(path).set(value)
        except HTTPError:
            print('error: failed to write database /' + path)

def upload(path, value):
    '''データベース送信処理の子スレッドをフォークして実行'''
    t = threading.Thread(target=upload_worker, args=(path, value,))
    t.start()

def scheduled_sensing_worker():
    '''
    各センサーデバイスからの計測データを収集し、タイムスタンプとともに
    データベースへ送信
    '''
    content = {}
    # 各センサーの読み取り
    content['moisture'] = get_moisture(GROVE_MOISTURE_PIN)
    content['dht'] = get_dht(GROVE_DHT_PIN)
    # データベースに送信
    for k, v in content.items():
        upload(DB_ROOT_PATH + '/' + k, v)

def scheduled_sensing(signum, frame):
    '''
    インターバルタイマーの発生するシグナルにより起動されるコールバック関数。
    定時計測するセンサーの子スレッドをフォークして実行
    '''
    if signum == signal.SIGALRM:
        # 新しいスレッドをフォークして実行
        t = threading.Thread(target=scheduled_sensing_worker, args=())
        t.start()

if __name__ == '__main__':
    # 設定したAdmin SDK認証情報を使用して、Firebaseアプリを初期化
    firebase = pyrebase.initialize_app(config)
    # データベースインスタンスの作成
    try:
        db = firebase.database()
    except:
        # 失敗時は、エラーコードを返して終了
        print('error: failed to open database')
        sys.exit(1)
    else:
        print('database successfully opened')

    # GPIOピンのセットアップ
    setup_gpio()
    # I2Cバスおよび加速度センサーのセットアップ
    bus = smbus.SMBus(1)
    setup_accel(bus)

    # 初回に温湿度センサーがゼロを返す場合があるため、空読みを実行
    get_dht(GROVE_DHT_PIN)

    # リレーに関するキーが未作成の場合、0で初期化
    if db.child(DB_ROOT_PATH + '/relay').get().val() is None:
        upload(DB_ROOT_PATH + '/relay', {'state': 0})

    # データベース更新の際のコールバック関数を指定
    db.child(DB_ROOT_PATH + '/relay/state').stream(relay_state_changed)

    # 定時出力関数をインターバルタイマーで起動するよう設定
    signal.signal(signal.SIGALRM, scheduled_sensing)
    signal.setitimer(signal.ITIMER_REAL, 2.0, OUTPUT_TASK_INTERVAL)

    # 永久ループによるセンサーの反応検出
    pir_last = 1
    acc_last = [nan, nan, nan]
    try:
        while True:
            # PIR モーションセンサー
            # 0→1 に変化した場合、データベースのタイムスタンプを更新
            pir = grovepi.digitalRead(GROVE_PIR_PIN)
            if pir == 1 and pir_last == 0:
                upload(DB_ROOT_PATH + '/pir',
                       {'timestamp': generate_timestamp()})
            pir_last = pir

            # 加速度センサー
            # Z軸が1.0G以上変化した場合、データベースのタイムスタンプを更新
            acc = read_accel(bus)
            if fabs(acc[2] - acc_last[2]) >= 1.0:
                upload(DB_ROOT_PATH + '/accel',
                       {'timestamp': generate_timestamp()})
            acc_last = acc

            # 待ち時間を空ける
            # ※短くしすぎると転送量や負荷が増大しますのでご注意ください。
            sleep(2)
    # Ctrl+C の入力でループから脱出
    except KeyboardInterrupt:
        pass
    sys.exit(0)
