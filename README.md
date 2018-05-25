# KP-RSCSP：センサーコミュニケーション基板 関連ソフトウェア

## 概要

共立電子産業株式会社が製造、販売するRaspberry Pi用拡張ボード「**センサーコミュニケーション基板**」(型番：**KP-RSCSP**) に関連するソフトウェア集です。

![基板写真](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/board.jpg)

## 当リポジトリに含まれる内容
  - [応用事例サンプル：アシスタントアプリ《センサーラボ》](https://github.com/kyohritsu/KP-RSCSP/tree/master/sensorlab)
  - [応用事例説明文書：アシスタントアプリの開発](https://github.com/kyohritsu/KP-RSCSP/tree/master/docs)
  - [基板上デバイス制御用Pythonモジュール](https://github.com/kyohritsu/KP-RSCSP/tree/master/onboard)
  - [常駐型ランチャーsystemdサービス](https://github.com/kyohritsu/KP-RSCSP/tree/master/service)

## インストール方法

Raspbian の場合

`git` がまだインストールされていない場合、最初にインストールしてください。

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

  - [共立プロダクツ事業所 - センサーコミュニケーション基板/KP-RSCSP](http://prod.kyohritsu.com/KP-RSCSP.html)

## サポートに関して

本製品のサポートはハードウェアのみとなります。  
ソフトウェアの設定は簡単に記載していますが、バージョン変更などにより、設定変更になる可能性があります。その際はお手数ですが、ご自身でインターネットや書籍などでお調べ頂くようお願いします。  
(ソフトウェアの設定方法などは電話・メールなどでのサポートは一切行っておりません)
