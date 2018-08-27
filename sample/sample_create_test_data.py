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

create_test_data_params = {
    'LogisticsSubType': 'FAMI',
    'PlatformID': '',
}

# 建立實體
ecpay_logistic_sdk = module.ECPayLogisticSdk(
    MerchantID='2000132',
    HashKey='5294y06JbISpM5x9',
    HashIV='v77hoKGq4kWxNNIS'
)

try:
    # 介接路徑
    action_url = 'https://logistics-stage.ecpay.com.tw/Express/CreateTestData'  # 測試環境
    # action_url = 'https://logistics.ecpay.com.tw/Express/CreateTestData' # 正式環境

    # 建立物流訂單並接收回應訊息
    reply_result = ecpay_logistic_sdk.create_test_data(
        action_url=action_url,
        client_parameters=create_test_data_params)
    pprint.pprint(reply_result)

except Exception as error:
    print('An exception happened: ' + str(error))
