# -*- coding: utf-8 -*-

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_logistic_sdk",
    "/path/to/ecpay_logistic_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

import pprint

create_unimart_b2c_return_order_params = {
    'AllPayLogisticsID': '129048',
    'ServerReplyURL': 'https://www.ecpay.com.tw/server_reply',
    'GoodsName': '測試商品1',
    'GoodsAmount': 1,
    'CollectionAmount': 0,
    'ServiceType': '4',
    'SenderName': '測試寄件者',
    'SenderPhone': '0226550115',
    'Remark': '測試備註',
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
    action_url = 'https://logistics-stage.ecpay.com.tw/express/ReturnUniMartCVS'  # 測試環境
    # action_url = 'https://logistics.ecpay.com.tw/express/ReturnUniMartCVS' # 正式環境

    # 建立物流訂單並接收回應訊息
    reply_result = ecpay_logistic_sdk.create_unimart_b2c_return_order(
        action_url=action_url,
        client_parameters=create_unimart_b2c_return_order_params)
    pprint.pprint(reply_result)

except Exception as error:
    print('An exception happened: ' + str(error))
