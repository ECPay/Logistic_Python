# -*- coding: utf-8 -*-

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_logistic_sdk",
    "/path/to/ecpay_logistic_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

import time
import pprint

query_logistics_info_params = {
    'AllPayLogisticsID': '129143',
    'TimeStamp': int(time.time()),
    'PlatformID': '',
}

# 建立實體
ecpay_logistic_sdk = module.ECPayLogisticSdk(
    MerchantID='2000933',
    HashKey='XBERn1YOvpM9nfZc',
    HashIV='h1ONHk4P4yqbl5LK'
)

try:
    # 介接路徑
    action_url = 'https://logistics-stage.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V2'  # 測試環境
    # action_url = 'https://logistics.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V2' # 正式環境

    # 建立物流訂單並接收回應訊息
    reply_result = ecpay_logistic_sdk.query_logistics_info(
        action_url=action_url,
        client_parameters=query_logistics_info_params)
    pprint.pprint(reply_result)

except Exception as error:
    print('An exception happened: ' + str(error))
