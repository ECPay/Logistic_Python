# -*- coding: utf-8 -*-

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_logistic_sdk",
    "/path/to/ecpay_logistic_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

import pprint

update_unimart_store_params = {
    'AllPayLogisticsID': '129143',
    'CVSPaymentNo': 'G6575106',
    'CVSValidationNo': '7109',
    'StoreType': '01',
    'ReceiverStoreID': '163512',
    'ReturnStoreID': '143183',
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
    action_url = 'https://logistics-stage.ecpay.com.tw/Express/UpdateStoreInfo'  # 測試環境
    # action_url = 'https://logistics.ecpay.com.tw/Express/UpdateStoreInfo' # 正式環境

    # 建立物流訂單並接收回應訊息
    reply_result = ecpay_logistic_sdk.update_unimart_store(
        action_url=action_url,
        client_parameters=update_unimart_store_params)
    pprint.pprint(reply_result)

except Exception as error:
    print('An exception happened: ' + str(error))
