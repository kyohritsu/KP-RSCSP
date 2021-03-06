# アシスタントアプリの開発 (2) アプリの設計方針

ここでは、例として作成するサンプル アプリケーションの設計方針および、仕様について説明を行います。

## ご注意

本文書で説明するアプリケーションは説明のために作成された簡易的なものであり、設計仕様上、個人1名がFirebaseサービスの無償プランの範囲内で、実験・学習目的に利用することのみを想定しています。不特定多数のユーザーが利用する状況等での運用は、セキュリティや転送量の問題により適しません。データ構造の見直しおよび認証方式の導入等、さらなる改良が必須となることをご留意ください。

## 概要

センサーラボは、「IoTスマートスピーカーモジュール」(KP-RSCSP) を搭載したRaspberry Piにセンサーや出力装置のGroveモジュールを接続し、Google Assistant対応機器上から制御するための簡易的なサンプルアプリケーションです。

## アプリ名

「**センサーラボ**」(`SensorLab`)

アプリ名はアシスタントから呼び出す際に使うので、なるべく言いやすく認識しやすい単語にします。アプリを公開する際には他社の名前との競合を避けたり、固有の特徴を表すアプリ名を付ける必要がありますが、ここでは考えないことにします。

※アシスタントアプリの作成時に登録する名前は、既存アプリとの競合が許されません。登録の際は適宜名前を考え、説明を読み換えてください。

## 対象とする接続モジュール

次の5種類のGroveモジュールに対応します。これらを本製品基板のモジュール用コネクタに接続し、Raspberry Pi システムからの操作を行います。

※再現する際は、これら5つのモジュールをすべて揃える必要はありません。一部のみ使用することが可能です。

  - 一定間隔ごとに計測を行うセンサーモジュール
    - **水分センサー**  
      [Grove - Moisture Sensor](http://wiki.seeedstudio.com/Grove-Moisture_Sensor/)
    - **デジタル温湿度センサー**  
      [Grove - Temperature & Humidity Sensor](http://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)
  - 常時監視し、反応した際に時刻を記録するセンサーモジュール
    - **PIRモーションセンサー**  
      [Grove - PIR Motion Sensor](http://wiki.seeedstudio.com/Grove-PIR_Motion_Sensor/)
    - **3軸デジタル加速度センサー**  
      [Grove - 3-Axis Digital Accelerometer (±1.5g)](http://wiki.seeedstudio.com/Grove-3-Axis_Digital_Accelerometer-1.5g/)
  - 出力モジュール
    - **リレー**  
      [Grove - Relay](http://wiki.seeedstudio.com/Grove-Relay/)

## 主要機能

「Ok Google、**センサーラボ**につないで」と話して呼び出します。アプリ内では、下記のことができるように機能を実装します。

  - 一定間隔ごとに計測を行うセンサー (水分・温湿度) に関する応答
    質問すると、最後に計測したデータを返答する。
    水分センサーと温湿度センサーの計測は、一定間隔で定期的に行われる。
  - 常時監視センサー (PIR・加速度) 関する応答
    最後に反応したタイミングがいつであるか返答する。
    各センサーの状態は常に監視され、反応が起こる度に随時更新が行われる。
  - リレー操作
    「オンにして」「オフにして」「トグルして」の操作ができる。

※アプリ名は任意です。Actions on Google コンソール内でアプリを作成する際に登録するアプリ名は、既に使われている名前は使用できないため、再現する際は適宜名前を決めてください。

### アプリとの会話例

  - 一定間隔ごとに計測を行うセンサー (水分・温湿度) に関する会話例  
    **ユーザー**「温湿度を教えて」  
    **アプリ**「現在の温度は23度、湿度は65%です。」  
    **ユーザー**「水分量を教えて」  
    **アプリ**「現在の水分量の指示値は243です。」
  - 常時監視センサー (PIR・加速度) に関する会話例  
    **ユーザー**「人感センサーの状態」  
    **アプリ**「人感センサーは、最近7分前に反応しました。」  
    **ユーザー**「加速度センサーの状態」  
    **アプリ**「加速度センサーは2時間以上Z軸の変化を検出していません。」
  - リレー操作に関する会話例  
    **ユーザー**「リレーをオンにして」  
    **アプリ**「リレーをオンにしました。」

## アプリの構成

Google アシスタントアプリでは、音声入力を認識してコマンドとなる質問文に変換し、対応する応答文を返却する一連の操作を作成することができますが、そのままではハードウェアによる各センサーへのアクセスを行うことができません。

センサー状態の取得やリレー出力の操作は、ユーザーの手元で動作する Raspberry Pi システムが担当しています。Raspberry Pi が位置するローカルネットワーク上の計測データをアシスタントアプリに連携させるには、クラウド上で動作するサービスプログラムと、情報を格納するデータベースが必要となります。

### Google Firebase

上記のクラウド プログラムとデータベースは自前で用意することもできますが、個人の評価や学習目的ではやや煩雑です。そこで今回は、Google が提供するクラウドサービス“Firebase”を使用することにします。
Firebase は、Google アシスタントプログラムと連携可能なサービス実行用関数のホスティングと、リアルタイムの読み書きに適したデータベースの両方を提供しており、2018年4月現在、評価目的で利用可能な無償プランがあります。

### 設計するもの

次のソフトウェア群を、お使いのGoogleアカウントで作成した1つのプロジェクト上に作成します。

  1. **アシスタントアプリ**  
     Google Assistant対応機器を使って自然言語による会話を行うアプリを、[Actions on Google](https://console.actions.google.com/) で作成します。
      - **[会話](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/dialogflow)** `sensorlab/dialogflow/`  
       [Dialogflow](https://console.dialogflow.com/) を利用して構築します。
      - **[フルフィルメント](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/fulfillment)** `sensorlab/fulfillment/`  
        センサー状態確認や出力の操作に関わる会話がトリガーされた時に呼び出され、データベースにアクセスし、応答を生成するための外部配置プログラムです。  
        Googleの提供する [Firebase](https://console.firebase.google.com/?hl=ja) サービス群のひとつである、Firebase Functions を使用します。  
  1. **[ローカルスクリプト](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/local_script)** `sensorlab/local_script/`  
     手持ちのRaspberry Pi + KP-RSCSP基板 + Groveモジュールで動作し、計測した各種センサー状態のデータベースへの送信や、出力装置の現在状態が変化した際に装置の制御を行うスクリプトです。今回は、Pythonで記述します。
  1. **[データベース](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/database)** `sensorlab/database/`  
    アシスタントアプリの会話とローカル環境下の入出力モジュールを連動させるために、現在状態をデータベースにて管理し、フルフィルメント・ローカルスクリプト両者から参照と更新をします。  
    使用するデータベースは、同じくFirebaseサービス群より Firebase Realtime Database を使用します。

上記ソフトウェアの関係を図示すると次のようになります。

![《センサーラボ》の構成図](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig000.png)

### データベースの使用方法

Firebaseの提供するRealtime Databaseは、階層を持ったデータ構造となっており、読み書きは、参照する位置をファイルパスのように指定することができます。

《センサーラボ》では、アシスタントと Raspberry Pi間のデータは全てデータベース経由で行うため、双方のデータベース構造を事前に設計しておく必要があります。

今回は、次の要素名を持つデータ構造とします。(値は一例です)

```
<データベースのルート>
  +-- sensorlab
       |-- moisture                                        水分センサー
       |    |-- value:        243                             水分量の指示値
       |    +-- timestamp:   "2018-04-01 00:08:00.583000"     データの取得時刻
       |-- dht                                             温湿度センサー
       |    |-- temperature:  23                              温度の指示値 (℃)
       |    |-- humidity:     65                              湿度の指示値 (%)
       |    +-- timestamp:   "2018-04-01 00:08:00.576000"     データの取得時刻
       |-- pir                                             モーションセンサー
       |    +-- timestamp:   "2018-04-01 00:00:27.077580"     最終反応時刻
       |-- accel                                           加速度センサー
       |    +-- timestamp:   "2018-04-01 00:01:16.411251"     最終反応時刻
       +-- relay                                           リレー
            +-- state:        1                               現在の出力値
```

4種のセンサーに関する計測値および検知イベントは、新しいものが発生するたびに、ローカルスクリプトが上書きをします (蓄積はされません)。アプリは、値とともに記録されたタイムスタンプを確認し、何分前に記録されたデータであるか判別します。
リレー出力の値は、フルフィルメントが音声コマンドの内容に応じて書き込みを行います。

## 事前準備

アプリの開発に使用するGoogleアカウントを1つ用意してください。
Googleアシスタント機能を利用するためには、アクティビティ履歴などを有効化する必要があります。
