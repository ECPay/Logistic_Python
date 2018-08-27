# -*- coding: utf-8 -*-

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_logistic_sdk",
    "/path/to/ecpay_logistic_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

cvs_map_params = {
    "MerchantTradeNo": "anyno",
    "LogisticsType": "CVS",
    # 若申請類型為 B2C，只能串參數為 FAMI、UNIMART、HILIFE
    # 若申請類型為 C2C，只能串參數為 FAMIC2C、UNIMARTC2C、HILIFEC2C
    "LogisticsSubType": "FAMIC2C",
    "IsCollection": "N",
    "ServerReplyURL": "https://www.ecpay.com.tw/receive",
    "ExtraData": "額外資訊",
    "Device": module.Device['PC'],
}

# 建立實體
ecpay_logistic_sdk = module.ECPayLogisticSdk(
    MerchantID='2000933',
    HashKey='XBERn1YOvpM9nfZc',
    HashIV='h1ONHk4P4yqbl5LK'
)

try:
    # 產生綠界物流訂單所需參數
    final_params = ecpay_logistic_sdk.cvs_map(cvs_map_params)

    # 產生 html 的 form 格式
    action_url = 'https://logistics-stage.ecpay.com.tw/Express/map'  # 測試環境
    #action_url = 'https://logistics.ecpay.com.tw/Express/map' # 正式環境
    html = ecpay_logistic_sdk.gen_html_post_form(action_url, final_params)
    print(html)
except Exception as error:
    print('An exception happened: ' + str(error))
