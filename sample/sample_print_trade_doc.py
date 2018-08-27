# -*- coding: utf-8 -*-

import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_logistic_sdk",
    "/path/to/ecpay_logistic_sdk.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

print_trade_doc_params = {
    'AllPayLogisticsID': '129157',
    'PlatformID': '',
    'ClientReplyURL': '',
}

# 建立實體
ecpay_logistic_sdk = module.ECPayLogisticSdk(
    MerchantID='2000132',
    HashKey='5294y06JbISpM5x9',
    HashIV='v77hoKGq4kWxNNIS'
)

try:
    # 產生綠界物流訂單所需參數
    final_params = ecpay_logistic_sdk.print_trade_doc(
        client_parameters=print_trade_doc_params)

    # 產生 html 的 form 格式
    action_url = 'https://logistics-stage.ecpay.com.tw/helper/printTradeDocument'  # 測試環境
    # action_url = 'https://logistics.ecpay.com.tw/helper/printTradeDocument' # 正式環境
    html = ecpay_logistic_sdk.gen_html_post_form(action_url, final_params)
    print(html)
except Exception as error:
    print('An exception happened: ' + str(error))
