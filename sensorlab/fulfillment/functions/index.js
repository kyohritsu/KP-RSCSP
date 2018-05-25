const DialogflowApp = require('actions-on-google').DialogflowApp;
const functions = require('firebase-functions');
const admin = require('firebase-admin');

// 当アプリが使用するデータベース内のルート位置
const dbRootPath = '/sensorlab';

admin.initializeApp();

exports.fulfillment = functions.https.onRequest((request, response) => {
    const app = new DialogflowApp({request, response});
    console.log('Request headers: ' + JSON.stringify(request.headers));
    console.log('Request body: ' + JSON.stringify(request.body));
    
    if (request.body.result) {
        processRequest(request, response);
    } else {
        console.log('Invalid Webhook Request');
        return response.status(400).end('Invalid Webhook request');
    }
});

const processRequest = (request, response) => {
    // Dialogflow のアクション種別 (type: string)
    const action = (request.body.result.action) ?
        request.body.result.action : 'default';
    // アクションのリクエスト内に含まれるパラメータ (type: Object)
    const parameters = request.body.result.parameters || {};
    // アクションのリクエスト発信元 (type: string)
    const requestSource = (request.body.originalRequest) ?
        request.body.originalRequest.source : undefined;
    // データベースの当アプリで使用するルート要素へのリファレンス
    const ref = admin.database().ref(dbRootPath);
    
    const sendResponse = (responseToUser) => {
        if (typeof responseToUser === 'string') {
            let responseJson = {};
            responseJson.speech = responseToUser;
            responseJson.displayText = responseToUser;
            response.json(responseJson);
        } else {
            let responseJson = {};
            responseJson.speech = responseToUser.speech ||
                responseToUser.displayText;
            responseJson.displayText = responseToUser.displayText ||
                responseToUser.speech;
            responseJson.data = responseToUser.data;
            responseJson.contextOut = responseToUser.outputContexts;
            response.json(responseJson);
        }
    };
    
    // タイムスタンプ文字列を読み、現在時刻からの経過分数を返す関数
    const minutesAfterTimestamp = (ts) => {
        return Math.floor((Date.now() - Date.parse(ts)) / 60000.0);
    };
    
    const actionHandlers = {
        'action.output': () => {
            const valueDevice = parameters['outdevice'];
            const valueCommand = parameters['outcommand'];
            const responseTable = {
                'outdevice': {
                    'relay': 'リレー'
                },
                'outcommand': {
                    'on': 'オンにしました。',
                    'off': 'オフにしました。',
                    'toggle': 'トグルしました。'
                }
            };
            if (valueCommand === 'on') {
                // オン
                ref.child(valueDevice).set({state: 1});
            } else if (valueCommand === 'off') {
                // オフ
                ref.child(valueDevice).set({state: 0});
            } else if (valueCommand === 'toggle') {
                // トグル (現在値を取得して反転)
                ref.child(valueDevice).once('value', (snapshot) => {
                    const state = snapshot.val()['state'] == 0 ? 0 : 1;
                    ref.child(valueDevice).set({state: 1 - state});
                });
            }
            sendResponse(responseTable['outdevice'][valueDevice] + 'を' +
                responseTable['outcommand'][valueCommand]);
        },
        'action.moisture': () => {
            const setResultString = (v) => {
                if (typeof v === 'number') {
                    return '水分量の指示値は' + v + 'です。';
                } else {
                    return '水分量の取得に失敗しました。';
                }
            };
            ref.child('moisture').once('value', (snapshot) => {
                const v = snapshot.val()['value'] !== undefined ?
                    snapshot.val()['value'] : undefined;
                const ts = snapshot.val()['timestamp'] || undefined;
                let resultString = '';
                let minsString = '';
                
                // 計測データのタイムスタンプを確認し、何分前の計測か確認
                const mins = minutesAfterTimestamp(ts);
                if (isNaN(mins)) {
                    // タイムスタンプ読み取り不可
                    resultString = '水分量の計測記録がありません。';
                } else if (mins >= 120) {
                    // 2 時間以上経過: 計測停止中とみなす
                    resultString = '水分量の計測が停止しています。';
                } else {
                    resultString = setResultString(v);
                    if (mins >= 1) {
                        // 1 分～2 時間未満
                        resultString = '最近の' + resultString;
                        minsString = 'このデータは' + mins +
                            '分前に計測されました。';
                    } else {
                        // 1 分未満
                        resultString = '現在の' + resultString;
                    }
                }
                sendResponse(resultString + minsString);
            });
        },
        'action.humitemp': () => {
            const setResultString = (temp, humi) => {
                if (typeof temp === 'number' && typeof humi === 'number') {
                    return '温度は' + temp + '度、湿度は' + humi + '%です。';
                } else if (typeof temp === 'number') {
                    return '温度は' + temp + '度です。';
                } else if (typeof humi === 'number') {
                    return '湿度は' + humi + '%です。';
                } else {
                    return '温湿度の取得に失敗しました。';
                }
            };
            ref.child('dht').once('value', (snapshot) => {
                const temp = snapshot.val()['temperature'] !== undefined ?
                    snapshot.val()['temperature'] : undefined;
                const humi = snapshot.val()['humidity'] !== undefined ?
                    snapshot.val()['humidity'] : undefined;
                const ts = snapshot.val()['timestamp'] || undefined
                let resultString = '';
                let minsString = '';
                
                // 計測データのタイムスタンプを確認し、何分前の計測か確認
                const mins = minutesAfterTimestamp(ts);
                if (isNaN(mins)) {
                    // タイムスタンプ読み取り不可
                    resultString = '温湿度の計測記録がありません。';
                } else if (mins >= 120) {
                    // 2 時間以上経過: 計測停止中とみなす
                    resultString = '温湿度の計測が停止しています。';
                } else {
                    resultString = setResultString(temp, humi);
                    if (mins >= 1) {
                        // 1 分～2 時間未満
                        resultString = '最近の' + resultString;
                        minsString = 'このデータは' + mins +
                            '分前に計測されました。';
                    } else {
                        // 1 分未満
                        resultString = '現在の' + resultString;
                    }
                }
                sendResponse(resultString + minsString);
            });
        },
        'action.pir': () => {
            ref.child('pir').once('value', (snapshot) => {
                const ts = snapshot.val()['timestamp'] || undefined;
                let resultString = '';
                let minsString = '';
                
                // 計測データのタイムスタンプを確認し、何分前の計測か確認
                const mins = minutesAfterTimestamp(ts);
                if (isNaN(mins)) {
                    // タイムスタンプ読み取り不可
                    resultString = '人感センサーの検出記録がありません。';
                } else if (mins >= 120) {
                    // 2 時間以上経過: 計測停止中とみなす
                    resultString = '人感センサーは2時間以上反応を' +
                        '検出していません。';
                } else {
                    if (mins >= 1) {
                        // 1 分～2 時間未満
                        minsString = '人感センサーは、最近' + mins +
                            '分前に反応しました。';
                    } else {
                        // 1 分未満
                        minsString = '人感センサーは、最近1分以内に' +
                            '反応しました。';
                    }
                }
                sendResponse(resultString + minsString);
            });
        },
        'action.accel': () => {
            ref.child('accel').once('value', (snapshot) => {
                const ts = snapshot.val()['timestamp'] || undefined;
                let resultString = '';
                let minsString = '';
                
                // 計測データのタイムスタンプを確認し、何分前の計測か確認
                const mins = minutesAfterTimestamp(ts);
                if (isNaN(mins)) {
                    // タイムスタンプ読み取り不可
                    resultString = '加速度センサーの検出記録がありません。';
                } else if (mins >= 120) {
                    // 2 時間以上経過
                    resultString = '加速度センサーは2時間以上Z軸の変化を' +
                        '検出していません。';
                } else {
                    if (mins >= 1) {
                        // 1 分～2 時間未満
                        minsString = '加速度センサーは、最近' + mins +
                            '分前にZ軸の変化を検出しました。';
                    } else {
                        // 1 分未満
                        minsString = '加速度センサーは、最近1分以内に' +
                            'Z軸の変化を検出しました。';
                    }
                }
                sendResponse(resultString + minsString);
            });
        },
        'default': () => {
            sendResponse('アクションが定義されていません。');
        }
    };
    (actionHandlers[action] || actionHandlers['default'])();
};
