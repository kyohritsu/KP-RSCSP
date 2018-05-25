# KP-RSCSP サンプルアプリケーション《センサーラボ》

## 概要

**センサーラボ**は、「センサーコミュニケーション基板」(KP-RSCSP) を搭載したRaspberry Piにセンサーや出力装置のGroveモジュールを接続し、Google Assistant対応機器上から制御するための簡易的なサンプルアプリケーションです。

### ご注意

本文書で説明するアプリケーションは説明のために作成された簡易的なものであり、設計仕様上、個人1名がFirebaseサービスの無償プランの範囲内で、実験・学習目的に利用することのみを想定しています。不特定多数のユーザーが利用する状況等での運用は、セキュリティや転送量の問題により適しません。データ構造の見直しおよび認証方式の導入等、さらなる改良が必須となることをご留意ください。

## 仕様

### 対応モジュール

次の5種類のGroveモジュールに対応します。

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

### アプリとの会話例

「Ok Google、センサーラボ※につないで」と話してアプリを呼び出した後、下記に例示する会話が可能となります。

  - 一定間隔ごとに計測を行うセンサーに関する会話例  
    **ユーザー**「温湿度を教えて」  
    **アプリ**「現在の温度は23度、湿度は65%です。」  
    **ユーザー**「水分量を教えて」  
    **アプリ**「現在の水分量の指示値は243です。」
  - 常時監視センサーに関する会話例  
    **ユーザー**「人感センサーの状態」  
    **アプリ**「人感センサーは、最近7分前に反応しました。」  
    **ユーザー**「加速度センサーの状態」  
    **アプリ**「加速度センサーは2時間以上Z軸の変化を検出していません。」
  - リレー操作に関する会話例  
    **ユーザー**「リレーをオンにして」  
    **アプリ**「リレーをオンにしました。」

※アプリ名は任意です。Actions on Google コンソール内でアプリを作成する際に登録するアプリ名は、既に使われている名前は使用できないため、再現される際は適宜名前を決めてください。

## アプリの構成

Google アシスタントアプリは、センサーや出力装置を直接操作することはできません。そのため、下記の構成要素を組み合わせてアプリを開発します。

次のソフトウェア群を、お使いのGoogleアカウントで作成した1つのプロジェクト上に作成します。

  1. **アシスタントアプリ**  
     Google Assistant対応機器を使って自然言語による会話を行うアプリを、[Actions on Google](https://console.actions.google.com/) で作成します。
      - **[会話](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/dialogflow)** `dialogflow/`  
       [Dialogflow](https://console.dialogflow.com/) を利用して構築します。
      - **[フルフィルメント](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/fulfillment)** `fulfillment/`  
        センサー状態確認や出力の操作に関わる会話がトリガーされた時に呼び出され、データベースにアクセスし、応答を生成するための外部配置プログラムです。  
        Googleの提供する [Firebase](https://console.firebase.google.com/?hl=ja) サービス群のひとつである、Firebase Functions を使用します。  
  1. **[ローカルスクリプト](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/local_script)** `local_script/`  
     手持ちのRaspberry Pi + KP-RSCSP基板 + Groveモジュールで動作し、計測した各種センサー状態のデータベースへの送信や、出力装置の現在状態が変化した際に装置の制御を行うスクリプトです。Pythonで記述します。
  1. **[データベース](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab/database)** `database/`  
    アシスタントアプリの会話とローカル環境下の入出力モジュールを連動させるために、現在状態をデータベースにて管理し、両者から参照・更新します。  
    使用するデータベースは、同じくFirebaseサービス群より Firebase Realtime Database を使用します。

上記ソフトウェアの関係を図示すると次のようになります。

![《センサーラボ》の構成図](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig000.png)

それぞれの詳細については当リポジトリ内の各サブディレクトリを参照してください。
