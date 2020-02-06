# KP-RSCSP：IoTスマートスピーカーモジュール 関連ソフトウェア

## 概要

共立電子産業株式会社が製造、販売するRaspberry Pi用拡張ボード「**IoTスマートスピーカーモジュール**」(型番：**KP-RSCSP**) に関連するソフトウェア集です。

![基板写真](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/board.jpg)

## 当リポジトリに含まれる内容
  - MEMSマイクの使用方法
    - [Raspbian Busterでの手順](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/microphones.md)
    - [Raspbian Stretchでの手順](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/microphones_stretch.md)
  - [赤外線リモコンインターフェースの使用方法](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/ir_transceiver.md)
  - 応用事例説明文書：アシスタントアプリの開発
    1. [はじめに](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/doc01_introduction.md)
    2. [アプリの設計方針](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/doc02_specification.md)
    3. [アシスタントアプリの作成](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/doc03_actions.md)
    4. [Dialogflowエージェントの作成](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/doc04_dialogflow.md)
    5. [フルフィルメントの作成](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/doc05_fulfillment.md)
    6. [ローカルスクリプトの作成](https://github.com/kyohritsu/KP-RSCSP/blob/master/docs/doc06_local_script.md)
  - [応用事例サンプル：アシスタントアプリ《センサーラボ》](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab)
  - [基板上デバイス制御用Pythonモジュール](https://github.com/kyohritsu/KP-RSCSP/tree/master/onboard)
  - [常駐型ランチャーsystemdサービス](https://github.com/kyohritsu/KP-RSCSP/tree/master/service)

## インストール方法

Raspbian の場合

Git がまだインストールされていない場合、最初にインストールしてください。

```sh
  ~$ sudo apt install git
```

続いて、当リポジトリをクローンします。

```sh
  ~$ git clone https://github.com/kyohritsu/KP-RSCSP
```

「基板上デバイス制御用Pythonモジュール」および「常駐型ランチャー」のシステムへのインストール/アンインストール方法については、それぞれ上記リンクより個別のページを参照してください。

### アンインストール方法

```sh
  ~$ rm -fr ~/KP-RSCSP
```

## ライセンス

MIT License  
詳細は、`LICENSE.txt` をご覧ください。

## 外部情報

当ソフトウェアは、下記のオープンソースソフトウェア プロジェクトを参照しています。
  - GrovePi - https://github.com/DexterInd/GrovePi
  - Pyrebase - https://github.com/thisbejim/Pyrebase

製品ページ

  - [共立プロダクツ事業所 - IoTスマートスピーカーモジュール/KP-RSCSP](http://prod.kyohritsu.com/KP-RSCSP.html)

## サポートに関して

本製品のサポートはハードウェアのみとなります。  
ソフトウェアの設定は簡単に記載していますが、バージョン変更などにより、設定変更になる可能性があります。その際はお手数ですが、ご自身でインターネットや書籍などでお調べ頂くようお願いします。  
(ソフトウェアの設定方法などは電話・メールなどでのサポートは一切行っておりません)
