# アシスタントアプリの開発 (4) Dialogflowエージェントの作成

Dialogflow を用いて、ユーザーとアプリの会話と、それに伴う関連動作を構築していきます。

## Dialogflow へアクセス

前節のActions on Googleのアクション管理画面から移動するか、PCのブラウザから下記 URLでDiglogflowコンソールにアクセスします。
  - https://console.dialogflow.com/

Dialogflow をお使いのアカウントに始めてリンクした際、地域の設定およびサービス規約への同意が求められます。
  - Country or territory に Japan を選択
  - サービス規約 (Terms of Service) を確認し、
    “Yes, I have read and accept...”にチェックを付け、［ACCEPT］(同意する) をクリックします。

![Dialogflow利用規約への同意](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig008.png)

## 新規エージェントの作成

Dialogflow では、対話文や各種動作一式のことをエージェント (agent) と呼びます。
［CREATE AGENT］をクリックし、新しいエージェントを作成します。

表示された初期設定画面を下記の通り変更します。
  - **Agent name**：SensorLab  
    SensorLab と入力されているか確認し、そうでなければ入力してください。
  - **Default Language**：Japanese ― ja  
    作成するエージェントのメイン言語を選択します。この設定は後で変更することはできません。
  - **Default Time Zone**：(GMT+9:00) Asia/Tokyo
  - **Google Project**  
    先程Actions on Googleで作成したプロジェクトIDが指定されていることを確認し、もしそうでなければ手動で選択してください。
  - **API Version**  
    □ Dialogflow V2 API：スイッチをクリックして、オフにします。  
    リクエストAPIには **V1** と **V2** の2種類のバージョンが存在します。今回はV1を使用します。

![新規エージェントの作成](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig009.png)

## エンティティ (Entities) の作成

この後すぐにインテント (Intents) の管理ページが表示されますが、先にエンティティの作成を行います。画面左のメニューから Entities を選択します。(ブラウザウィンドウが狭い場合、メニューは画面左上の［≡］をクリックすることで表示されます)

エンティティとは、同一のものを指す表現を同義語としてまとめたり、文脈上で置き換えが可能な共通性をもつ主語や述語を登録し、会話のパターンマッチングを補助するための仕組みです。
例えば、「`オフにして`」(Turn off) と表す際に、表記の揺れを許容するのであれば、エンティティとして次のような同義語を登録しておきます。

  > オフ; オフに; オフにして; 消灯; 消灯して; 消して; 切って; 切手; OFF;
  OFFに; OFFにして

「切手」のように、音声認識による誤変換が発生しやすい結果もあわせて登録すると認識率が改善します。
また、1 つのエンティティには複数の同義語を登録可能です。例えば「`リレーをオフにして`」の他、「`リレーをオンにして`」「`リレーをトグルして`」という表現について「`リレーを○○○`」で共通化される一連の操作をパラメータにして一括でマッチングさせることもできます。

### 《センサーラボ》で作成するエンティティ

こちらを参照してください。→ [`example_sensorlab/assistant_app/dialogflow/`](https://github.com/kyohritsu/KP-RSCSP/tree/master/example_sensorlab/assistant_app/dialogflow)

![エンティティの登録例](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig010.png)

## インテント (Intents) の作成

インテントは、「ユーザーからの質問文パターン」「ユーザーへの応答文」「応答とともに実行する外部サービスやプログラムの指定」などをまとめた、アクションの構成を定義するものです。

各項目の簡単な説明は下記の通りです。実際の使い方は、サンプルアプリの設定例をご確認ください。
  - **Contexts**  
    アクション内にある他のインテント間で文脈関係を構成する際に使用します。
      - Input context  
        このインテントが発生するための条件を指定します。
      - Output context  
        このインテントが発生した際に満たされる条件を指定します。
  - **Events**  
    インテントを他アプリや特殊なトリガー条件で発生する際に指定します。  
    ![Events](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig011.png)
  - **Training phrases**  
    このインテントを発生するための、ユーザーからの質問文パターンを指定します。エンティティで指定した同義語やパラメータの指定に対応しています。  
    内容の一部が作成済みのエンティティにマッチする場合は、自動で関連付けが行われて次項のパラメータ欄に登録されます。関連付けされたパラメータの箇所には背景色が付きます。
  - **Action and parameters**  
    インテントが実行された際に、フルフィルメント (外部プログラム：後述) に送られるデータを指定します。
      - action (アクション)  
        処理の種類を識別するための識別名です。
      - parameter (パラメータ)  
        ユーザーの質問文から抽出される引数です。それぞれの引数ごとに、外部関数の動作に必須または省略可であるか指定でき、必須パラメータが揃わなかった際にユーザーへたずね直すための確認文の登録も行います。
    ![アクションとパラメータの設定例](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig012.png)
  - **Responses**  
    このインテントがユーザーへ返す応答を指定します。  
    ※フルフィルメントを使用する場合は、その呼び出し先の関数内で応答を確実に返すようにしていれば、この項目は空白のままでもかまいません。
      - Default
          - Text response  
          テキストのみの応答に使用される固定文字列を入力します。複数個入力すると、インテント発生の度にランダムで1つが応答文として選ばれます。
      - Google Assistant  
        Google アシスタント環境向けの応答を指定します。カード表示や、サジェスト候補、メディア再生など、テキスト以外のコンテンツを使用した応答を作成することができます。
      - ADD RESPONSES  
        他の種類の応答を追加する際はここをクリックします。
      - Set this intent as end of conversation  
        スイッチをオンにすると、このインテントの発生でアプリの会話を終了し、アシスタントへ戻ります。
  - **Fulfillment**  
    インテント発生時、外部に配置されたクラウドプログラムを呼び出す場合に利用します。この際に使用する外部プログラムのことをフルフィルメントと呼びます。
      - Enable webhook call for this intent  
        オンにすると、このインテント発生時にフルフィルメントが呼び出されます。
      - Enable webhook call for slot filling  
        インテント発生時の質問文の中にパラメータが不足している場合の挙動を指定します。オンにすると、パラメータが不足していてもそのままの状態でフルフィルメントが呼び出されます。オフの場合は、パラメータがすべて揃わなければフルフィルメントの呼び出しは行われません。

### 《センサーラボ》で作成するインテント

こちらを参照してください。→ [`example_sensorlab/assistant_app/dialogflow/`](https://github.com/kyohritsu/KP-RSCSP/tree/master/example_sensorlab/assistant_app/dialogflow)

![《センサーラボ》のインテント一覧](https://raw.githubusercontent.com/kyohritsu/KP-RSCSP/master/docs/assets/fig013.png)

## フルフィルメント (Fulfillment) の登録

フルフィルメントとは、特定のインテントが発生した際に呼び出す外部プログラムです。Dialogflowだけでは実現できない複雑な場合分けを伴った応答の作成や、外部サービスとの連携を行うには、フルフィルメントに処理を記述して実行します。

Googleの提供するサービスのひとつに Firebase Cloud Functions というクラウド関数のホスティングサービスがあります。これを利用し、アシスタントアプリ用のフルフィルメント関数を運用する方法が簡単です。

次節にて説明する方法でフルフィルメント関数を作成し、デプロイします。その際に発行される関数へのURLを登録することで、Dialogflowの指定インテントから関数の実行を行うことができるようになります。

《センサーラボ》では、追加した6個のインテントのうち各種センサーとリレーに関する5個に対し、実行時にフルフィルメントを呼び出すように設定しました。ここまでの段階ではフルフィルメント関数はまだ着手していないため、呼び出し時に使用する関数のURLは未定です。完成次第、Dialogflowに戻ってきて関数のURLを登録します。

次は、Firebase を使用してフルフィルメント関数の作成とデプロイを行います。
