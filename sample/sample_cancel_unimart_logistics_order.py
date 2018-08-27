# -*- coding: utf-8 -*-

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_logistic_sdk",
    "/path/to/ecpay_logistic_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

import pprint

cancel_unimart_logistics_order_params = {
    'AllPayLogisticsID': '129141',
    'CVSPaymentNo': 'G6575105',
    'CVSValidationNo': '3729',
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
    action_url = 'https://logistics-stage.ecpay.com.tw/Express/CancelC2COrder'  # 測試環境
    # action_url = 'https://logistics.ecpay.com.tw/Express/CancelC2COrder' # 正式環境

    # 建立物流訂單並接收回應訊息
    reply_result = ecpay_logistic_sdk.cancel_unimart_logistics_order(
        action_url=action_url,
        client_parameters=cancel_unimart_logistics_order_params)
    pprint.pprint(reply_result)

except Exception as error:
    print('An exception happened: ' + str(error))
