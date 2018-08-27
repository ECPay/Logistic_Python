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
    'LogisticsType': module.LogisticsType['HOME'],
    'LogisticsSubType': module.LogisticsSubType['TCAT'],
    'GoodsAmount': 1500,
    'CollectionAmount': 1500,
    'IsCollection': module.IsCollection['NO'],
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

shipping_home_params = {
    'SenderZipCode': '11560',
    'SenderAddress': '台北市南港區三重路19-2號10樓D棟',
    'ReceiverZipCode': '11560',
    'ReceiverAddress': '台北市南港區三重路19-2號5樓D棟',
    'Temperature': module.Temperature['FREEZE'],
    'Distance': module.Distance['SAME'],
    'Specification': module.Specification['CM_120'],
    'ScheduledPickupTime': module.ScheduledPickupTime['TIME_17_20'],
    'ScheduledDeliveryTime': module.ScheduledDeliveryTime['TIME_17_20'],
    'ScheduledDeliveryDate': '',
    'PackageCount': '',
}

# 更新及合併參數
create_shipping_order_params.update(shipping_home_params)

# 建立實體
ecpay_logistic_sdk = module.ECPayLogisticSdk(
    MerchantID='2000933',
    HashKey='XBERn1YOvpM9nfZc',
    HashIV='h1ONHk4P4yqbl5LK'
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
