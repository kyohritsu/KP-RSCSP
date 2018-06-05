# サンプルアプリケーション《センサーラボ》ローカルスクリプト

## 概要

ローカルスクリプトは、Raspberry Pi上で動作させてセンサーや出力装置のモジュールを制御し、データベース上に入出力を行うためのプログラムです。センサーの指示値や出力装置の状態を最新状態に保つためには、このプログラムを常時実行しておく必要があります。

## 運用手順

### 認証情報の変更

スクリプト内の下記の認証情報を格納する変数を、個人のプロジェクトにあわせた値に変更してください。

```python
# ウェブ API キー
WEB_API_KEY = 'AIza***********************************'
# プロジェクト ID
PROJECT_ID = 'yourproject-1e84f'
# 秘密鍵 JSON ファイルへのパス
PATH_TO_CREDENTIAL_JSON = '/path/to/credential.json'
```

秘密鍵JSONへのパス `PATH_TO_CREDENTIAL_JSON` には、先程転送した秘密鍵JSONファイルへのパスを入力します。

## Groveモジュールの接続

本製品基板の**モジュール接続コネクタ** (CN3 - CN8) に下記のGroveモジュールを接続します。モジュールは5つ全て揃える必要はありません。一部のみでもかまいません。

| 部品番号 | コネクタ名 | モジュール |
| :--: | :--: | :-- |
| CN3 | I2C0 | *接続なし* |
| CN4 | I2C1 | 3軸加速度センサー ([Grove - 3-Axis Digital Accelerometer(±1.5g)](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-1.5g/)) |
| CN5 | A0 | 水分センサー ([Grove - Moisture Sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/)) |
| CN6 | A2 | PIRモーションセンサー ([Grove - PIR Motion Sensor](http://wiki.seeedstudio.com/Grove-PIR_Motion_Sensor/)) |
| CN7 | D0 | デジタル温湿度センサー ([Grove - Temperature & Humidity Sensor](http://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)) |
| CN8 | D2 | リレー ([Grove - Relay](http://wiki.seeedstudio.com/Grove-Relay/)) |

![モジュール接続図](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/modules.jpg)

## ローカルスクリプトの実行

Groveモジュールを上記通りのコネクタに接続し、認証情報を個人の内容に置き換えた後は、ローカルスクリプトを実行します。

```sh
  ~/KP-RSCSP/sensorlab/local_script$ python3 local_script.py
```

スクリプトは、データベースへの接続に成功すると、下記に示す一連の動作を並行して行います。
  - 定期的な温湿度と水分データの送信
  - PIRモーションセンサーと加速度センサーは、検知したタイミングで随時送信
  - リレー状態を監視し、変化があれば出力の変更

このスクリプトが動作している間は、以上の動作によってアプリとの連動が保たれます。終了するには、`^C` ([Ctrl]+[C]) を2度続けて入力してください。
