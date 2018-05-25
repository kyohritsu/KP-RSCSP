# KP-RSCSP サンプルアプリケーション《センサーラボ》Dialogflowエージェント

## 概要

本文書では、Dialogflow Consoleで、《センサーラボ》用のエージェントを作成する際の手順を説明します。

当ディレクトリ内のファイルは、Dialogflow Consoleからエクスポートされたエージェントデータです。あらかじめDialogflowエージェントの新規作成を行ったうえで、ファイル一式をZIP形式で圧縮し、Dialogflowエージェント上にインポートすることで、入力作業を簡略化できます。ただし、フルフィルメントURLについては、個人のプロジェクトに合わせたものに変更する必要があります。

## エージェント作成手順

### エンティティ (Entities) の作成

下記6個のエンティティを新規作成します。

#### moisture  
☑Define synonyms  
☐Allow Automated expansion  

| Value | Synonyms |
| :- | :- |
| moisture | 水分; 水分量; 土; 土の水分; 土の水分量; 土壌; 土壌の水分; 土壌の水分量; ドジョウ; ドジョウの水分; ドジョウの水分量 |

#### humitemp  
☑Define synonyms  
☐Allow Automated expansion  

| Value | Synonyms |
| :- | :- |
| humitemp | 温湿度センサー; 温湿度IC; 温湿度; 温度センサー; 温度IC; 温度; 音頭センサー; 音頭IC; 音頭; 湿度センサー; 湿度IC; 湿度 |

#### pir
☑Define synonyms  
☐Allow Automated expansion  

| Value | Synonyms |
| :- | :- |
| pir | 人感センサー; 人感; 動きセンサー; 動き; モーションセンサー; モーション; PIRセンサー; PIR; ピーアイアール |

#### accel  
☑Define synonyms  
☐Allow Automated expansion  

| Value | Synonyms |
| :- | :- |
| accel | 加速度センサー; 加速度IC; 加速度; 重力センサー; 重力 |

#### outdevice
☑Define synonyms  
☐Allow Automated expansion  

| Value | Synonyms |
| :- | :- |
| relay | リレー; 電磁リレー; 継電器; 接点 |

#### outcommand  
☑Define synonyms  
☐Allow Automated expansion  

| Value | Synonyms |
| :- | :- |
| off | オフ; オフに; オフにして; 消灯; 消灯して; 消して; 切って; 切手; OFF; OFFに; OFFにして |
| on | オン; オンに; オンにして; 点灯; 点灯して; 店頭; 店頭して; 転倒; 転倒して; つけて; 付けて; 入れて; ON; ONに; ONにして |
| toggle | トグル; トグルして; 逆; 逆にして; 反対; 反対にして; 切り替え; 切替; 切り替えて |

### インテント (Intents) の編集と追加

初期登録済みのインテントを編集し、さらに6個のインテントを新規作成します。

#### Default Welcome Intent

Responses  
DEFAULT > Text response  の1行目を変更  
  - センサーラボの実験プログラムです。

#### Default Fallback Intent

このインテントは初期状態のままにします。

#### Get Soil Moisture

Training phrases
  - *水分センサー*
  - *水分センサー*をおしえて
  - *水分センサー*の状態
  - *水分センサー*の記録
  - 土は乾いてない？

Actions and parameters

**action.accel**

| REQUIRED | PARAMETER NAME | ENTITY | VALUE | IS LIST |
| :- | :- | :- | :- | :- |
| ☐ | moisture | @moisture | $moisture | ☐ |

Fulfillment  
「Enable webhook call for this intent」をオンにする

#### Get Accelerometer Event

Training phrases
  - *加速度センサー*
  - *加速度センサー*をおしえて
  - *加速度センサー*の状態
  - *加速度センサー*の記録

Actions and parameters

**action.accel**

| REQUIRED | PARAMETER NAME | ENTITY | VALUE | IS LIST |
| :- | :- | :- | :- | :- |
| ☐ | accel | @accel | $accel | ☐ |

Fulfillment  
「Enable webhook call for this intent」をオンにする

#### Get Humidity and Temperature

Training phrases
  - *温湿度センサー*
  - *温湿度センサー*をおしえて
  - *温湿度センサー*の状態
  - *温湿度センサー*の記録

Actions and parameters

**action.humitemp**

| REQUIRED | PARAMETER NAME | ENTITY | VALUE | IS LIST |
| :- | :- | :- | :- | :- |
| ☐ | humitemp | @humitemp | $humitemp | ☐ |

Fulfillment  
Enable webhook call for this intent をオンにする

#### Get PIR Sensor event

Training phrases
  - *人感センサー*
  - *人感センサー*をおしえて
  - *人感センサー*の状態
  - *人感センサー*の記録
  - あやしい人を見なかった？

Actions and parameters

**action.pir**

| REQUIRED | PARAMETER NAME | ENTITY | VALUE | IS LIST |
| :- | :- | :- | :- | :- |
| ☐ | pir | @pir | $pir | ☐ |

Fulfillment  
Enable webhook call for this intent をオンにする

#### Set output

Training phrases
  - *リレーオンにして*
  - *リレー*を*オンにして*

Actions and parameters

**action.output**

| REQUIRED | PARAMETER NAME | ENTITY | VALUE | IS LIST | PROMPTS |
| :- | :- | :- | :- | :- | :- |
| ☑ | outdevice | @outdevice | $outdevice | ☐ | どの出力を操作しますか？ |
| ☑ | outcommand | @outcommand | $outcommand | ☐ | 出力をどのように操作しますか？ |

Fulfillment  
Enable webhook call for this intent をオンにする

#### Quit

Training phrases
  - 終了
  - おわり
  - さよなら

Responses  
DEFAULT > Text response の1行目に入力  
  - アプリを終了します。

Set this intent as end of conversation をオンにする

### フルフィルメント (Fulfillment) の指定

先にFirebase Functionsで同一プロジェクトにフルフィルメントをデプロイしておきます。

メニューからFulfillmentを選択し、下記の通りに内容を変更して［SAVE］をクリックします。

  - **Webhook**  ☑ (ENABLED)
      - **URL**: (デプロイしたフルフィルメント関数の URL)
      - **Basic Auth**: (空欄)
      - **Headers**: (空欄)
      - **Domains**: Enable webhook for all domains
  - **Inline Editor (Powered by Cloud Functions for Firebase)**  □ (DISABLED)
