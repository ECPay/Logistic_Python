# -*- coding: utf-8 -*-

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_logistic_sdk",
    "/path/to/ecpay_logistic_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

import pprint
from datetime import datetime

create_shipping_order_params = {
    'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
    'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    'LogisticsType': module.LogisticsType['CVS'],
    'LogisticsSubType': module.LogisticsSubType['UNIMART'],
    'GoodsAmount': 1500,
    'CollectionAmount': 1500,
    'IsCollection': module.IsCollection['YES'],
    'GoodsName': '測試商品',
    'SenderName': '測試寄件者',
    'SenderPhone': '0226550115',
    'SenderCellPhone': '0911222333',
    'ReceiverName': '測試收件者',
    'ReceiverPhone': '0226550115',
    'ReceiverCellPhone': '0933222111',
    'ReceiverEmail': 'test@gmail.com',
    'TradeDesc': '測試交易敘述',
    'ServerReplyURL': 'https://www.ecpay.com.tw/server_reply_url',
    'ClientReplyURL': '',
    'Remark': '測試備註',
    'PlatformID': '',
    'LogisticsC2CReplyURL': 'https://www.ecpay.com.tw/logistics_c2c_reply',
}

shipping_cvs_params = {
    'ReceiverStoreID': '991182',
    'ReturnStoreID': '991182',
}

# 更新及合併參數
create_shipping_order_params.update(shipping_cvs_params)

# 建立實體
ecpay_logistic_sdk = module.ECPayLogisticSdk(
    MerchantID='2000132',
    HashKey='5294y06JbISpM5x9',
    HashIV='v77hoKGq4kWxNNIS'
)

try:
    # 介接路徑
    action_url = 'https://logistics-stage.ecpay.com.tw/Express/Create'  # 測試環境
    # action_url = 'https://logistics.ecpay.com.tw/Express/Create' # 正式環境

    # 建立物流訂單並接收回應訊息
    reply_result = ecpay_logistic_sdk.create_shipping_order(
        action_url=action_url,
        client_parameters=create_shipping_order_params)
    pprint.pprint(reply_result)

except Exception as error:
    print('An exception happened: ' + str(error))
