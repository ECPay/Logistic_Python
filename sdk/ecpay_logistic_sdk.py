# coding: utf-8
import collections
import hashlib
import copy
import requests
import json
from urllib.parse import quote_plus, parse_qsl, parse_qs

"""
物流類型
"""
LogisticsType = {
    'CVS': 'CVS',  # 超商取貨
    'HOME': 'Home',  # 宅配
}

"""
物流子類型
"""
LogisticsSubType = {
    'TCAT': 'TCAT',  # 黑貓(宅配)
    'ECAN': 'ECAN',  # 宅配通
    'FAMILY': 'FAMI',  # 全家
    'UNIMART': 'UNIMART',  # 統一超商
    'HILIFE': 'HILIFE',  # 萊爾富
    'FAMILY_C2C': 'FAMIC2C',  # 全家店到店
    'UNIMART_C2C': 'UNIMARTC2C',  # 統一超商寄貨便
    'HILIFE_C2C': 'HILIFEC2C',  # 萊爾富富店到店
}

"""
是否代收貨款
"""
IsCollection = {
    'YES': 'Y',  # 貨到付款
    'NO': 'N',  # 僅配送
}

"""
使用設備
"""
Device = {
    'PC': 0,  # PC
    'MOBILE': 1,  # 行動裝置
}

"""
測試廠商編號
"""
ECPayTestMerchantID = {
    'B2C': '2000132',  # B2C
    'C2C': '2000933',  # C2C
}

"""
正式環境網址
"""
ECPayURL = {
    'CVS_MAP': 'https://logistics.ecpay.com.tw/Express/map',  # 電子地圖
    'SHIPPING_ORDER': 'https://logistics.ecpay.com.tw/Express/Create',  # 物流訂單建立
    'HOME_RETURN_ORDER': 'https://logistics.ecpay.com.tw/Express/ReturnHome',  # 宅配逆物流訂單
    # 超商取貨逆物流訂單(統一超商B2C)
    'UNIMART_RETURN_ORDER': 'https://logistics.ecpay.com.tw/express/ReturnUniMartCVS',
    # 超商取貨逆物流訂單(萊爾富超商B2C)
    'HILIFE_RETURN_ORDER': 'https://logistics.ecpay.com.tw/express/ReturnHiLifeCVS',
    # 超商取貨逆物流訂單(全家超商B2C)
    'FAMILY_RETURN_ORDER': 'https://logistics.ecpay.com.tw/express/ReturnCVS',
    # 全家逆物流核帳(全家超商B2C)
    'FAMILY_RETURN_CHECK': 'https://logistics.ecpay.com.tw/Helper/LogisticsCheckAccoounts',
    # 統一修改物流資訊(全家超商B2C)
    'UNIMART_UPDATE_LOGISTICS_INFO': 'https://logistics.ecpay.com.tw/Helper/UpdateShipmentInfo',
    # 更新門市(統一超商C2C)
    'UNIMART_UPDATE_STORE_INFO': 'https://logistics.ecpay.com.tw/Express/UpdateStoreInfo',
    # 取消訂單(統一超商C2C)
    'UNIMART_CANCEL_LOGISTICS_ORDER': 'https://logistics.ecpay.com.tw/Express/CancelC2COrder',
    'QUERY_LOGISTICS_INFO': 'https://logistics.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V2',  # 物流訂單查詢
    # 產生托運單(宅配)/一段標(超商取貨)
    'PRINT_TRADE_DOC': 'https://logistics.ecpay.com.tw/helper/printTradeDocument',
    # 列印繳款單(統一超商C2C)
    'PRINT_UNIMART_C2C_BILL': 'https://logistics.ecpay.com.tw/Express/PrintUniMartC2COrderInfo',
    # 全家列印小白單(全家超商C2C)
    'PRINT_FAMILY_C2C_BILL': 'https://logistics.ecpay.com.tw/Express/PrintFAMIC2COrderInfo',
    # 萊爾富列印小白單(萊爾富超商C2C)
    'Print_HILIFE_C2C_BILL': 'https://logistics.ecpay.com.tw/Express/PrintHILIFEC2COrderInfo',
    'CREATE_TEST_DATA': 'https://logistics.ecpay.com.tw/Express/CreateTestData',  # 產生 B2C 測標資料
}

"""
測試環境網址
"""
ECPayTestURL = {
    'CVS_MAP': 'https://logistics-stage.ecpay.com.tw/Express/map',  # 電子地圖
    'SHIPPING_ORDER': 'https://logistics-stage.ecpay.com.tw/Express/Create',  # 物流訂單建立
    'HOME_RETURN_ORDER': 'https://logistics-stage.ecpay.com.tw/Express/ReturnHome',  # 宅配逆物流訂單
    # 超商取貨逆物流訂單(統一超商B2C)
    'UNIMART_RETURN_ORDER': 'https://logistics-stage.ecpay.com.tw/express/ReturnUniMartCVS',
    # 超商取貨逆物流訂單(萊爾富超商B2C)
    'HILIFE_RETURN_ORDER': 'https://logistics-stage.ecpay.com.tw/express/ReturnHiLifeCVS',
    # 超商取貨逆物流訂單(全家超商B2C)
    'FAMILY_RETURN_ORDER': 'https://logistics-stage.ecpay.com.tw/express/ReturnCVS',
    # 全家逆物流核帳(全家超商B2C)
    'FAMILY_RETURN_CHECK': 'https://logistics-stage.ecpay.com.tw/Helper/LogisticsCheckAccoounts',
    # 統一修改物流資訊(全家超商B2C)
    'UNIMART_UPDATE_LOGISTICS_INFO': 'https://logistics-stage.ecpay.com.tw/Helper/UpdateShipmentInfo',
    # 更新門市(統一超商C2C)
    'UNIMART_UPDATE_STORE_INFO': 'https://logistics-stage.ecpay.com.tw/Express/UpdateStoreInfo',
    # 取消訂單(統一超商C2C)
    'UNIMART_CANCEL_LOGISTICS_ORDER': 'https://logistics-stage.ecpay.com.tw/Express/CancelC2COrder',
    'QUERY_LOGISTICS_INFO': 'https://logistics-stage.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V2',  # 物流訂單查詢
    # 產生托運單(宅配)/一段標(超商取貨)
    'PRINT_TRADE_DOC': 'https://logistics-stage.ecpay.com.tw/helper/printTradeDocument',
    # 列印繳款單(統一超商C2C)
    'PRINT_UNIMART_C2C_BILL': 'https://logistics-stage.ecpay.com.tw/Express/PrintUniMartC2COrderInfo',
    # 全家列印小白單(全家超商C2C)
    'PRINT_FAMILY_C2C_BILL': 'https://logistics-stage.ecpay.com.tw/Express/PrintFAMIC2COrderInfo',
    # 萊爾富列印小白單(萊爾富超商C2C)
    'PRINT_HILIFE_C2C_BILL': 'https://logistics-stage.ecpay.com.tw/Express/PrintHILIFEC2COrderInfo',
    'CREATE_TEST_DATA': 'https://logistics-stage.ecpay.com.tw/Express/CreateTestData',  # 產生 B2C 測標資料
}

"""
溫層
"""
Temperature = {
    'ROOM': '0001',  # 常溫
    'REFRIGERATION': '0002',  # 冷藏
    'FREEZE': '0003',  # 冷凍
}

"""
距離
"""
Distance = {
    'SAME': '00',  # 同縣市
    'OTHER': '01',  # 外縣市
    'ISLAND': '02',  # 離島
}

"""
規格
"""
Specification = {
    'CM_60': '0001',  # 60cm
    'CM_90': '0002',  # 90cm
    'CM_120': '0003',  # 120cm
    'CM_150': '0004',  # 150cm
}

"""
預計取件時段
"""
ScheduledPickupTime = {
    'TIME_9_12': '1',  # 9~12時
    'TIME_12_17': '2',  # 12~17時
    'TIME_17_20': '3',  # 17~20時
    'UNLIMITED': '4',  # 不限時
}

"""
預定送達時段
"""
ScheduledDeliveryTime = {
    'TIME_9_12': '1',  # 9~12時
    'TIME_12_17': '2',  # 12~17時
    'TIME_17_20': '3',  # 17~20時
    'UNLIMITED': '4',  # 不限時
    'TIME_20_21': '5',  # 20~21時(需限定區域)
    'TIME_9_17': '12',  # 早午 9~17
    'TIME_9_12_17_20': '13',  # 早晚 9~12 & 17~20
    'TIME_13_20': '23',  # 午晚 13~20
}

"""
門市類型
"""
StoreType = {
    'RECIVE_STORE': '01',  # 取件門市
    'RETURN_STORE': '02',  # 退件門市
}


class BasePayment(object):

    def merge(self, x, y):
        """
        Given two dicts, merge them into a new dict as a shallow copy.
        """
        z = x.copy()
        z.update(y)
        return z

    # 檢查必填參數
    # 檢查 merge.dict 是否有填正確的值或範圍
    def check_required_parameter(self, parameters, patterns):
        for patten in patterns:
            for k, v in patten.items():
                if v.get('required') and (v.get('type') is str):
                    if parameters.get(k) is None:
                        raise Exception('parameter %s is required.' % k)
                    elif len(parameters.get(k)) == 0:
                        raise Exception('%s content is required.' % k)
                    elif len(parameters.get(k)) > v.get('max'):
                        raise Exception('%s max langth is %d.' %
                                        (k, v.get('max')))
                elif v.get('required') and (v.get('type') is int):
                    if parameters.get(k) is None:
                        raise Exception('parameter %s is required.' % k)

    # 先用 required.dict 設定預設值並產生新 new.required.dict
    def create_default_dict(self, parameters):
        default_dict = dict()
        for k, v in parameters.items():
            if v['type'] is str:
                default_dict.setdefault(k, '')
            elif v['type'] is int:
                default_dict.setdefault(k, 0)
            else:
                raise Exception('unsupported type!')
        for k, v in parameters.items():
            if v.get('default'):
                default_dict[k] = v.get('default')
        return default_dict

    # 檢查 merge.dict 是否有填正確的值或範圍
    def filter_parameter(self, parameters, pattern):
        for patten in pattern:
            for k, v in patten.items():
                if (v.get('required') is False) and (v.get('type') is str):
                    if parameters.get(k) is None:
                        continue
                    if len(parameters.get(k)) == 0:
                        del parameters[k]
                elif (v.get('required') is False) and (v.get('type') is int):
                    if parameters.get(k) is None:
                        continue
                    if parameters.get(k) == 0:
                        del parameters[k]

    def generate_check_value(self, params):
        _params = copy.deepcopy(params)

        if 'CheckMacValue' in _params:
            _params.pop('CheckMacValue')

        ordered_params = collections.OrderedDict(
            sorted(_params.items(), key=lambda k: k[0]))

        encoding_lst = []
        encoding_lst.append('HashKey=%s&' % self.HashKey)
        encoding_lst.append(''.join(
            ['{}={}&'.format(key, value) for key, value in ordered_params.items()]))
        encoding_lst.append('HashIV=%s' % self.HashIV)

        safe_characters = '-_.!*()'

        encoding_str = ''.join(encoding_lst)
        encoding_str = quote_plus(
            str(encoding_str), safe=safe_characters).lower()

        check_mac_value = hashlib.md5(
            encoding_str.encode('utf-8')).hexdigest().upper()
        return check_mac_value

    def integrate_parameter(self, parameters, patterns):
        # 更新 MerchantID
        parameters['MerchantID'] = self.MerchantID
        # 檢查必填參數
        self.check_required_parameter(parameters, patterns)
        # 將 merge.dict 內的無用參數消除
        self.filter_parameter(parameters, patterns)
        # 計算 CheckMacValue
        parameters['CheckMacValue'] = self.generate_check_value(parameters)
        return parameters

    def send_post(self, url, params):
        response = requests.post(url, data=params)
        return response


class ExtendFunction(BasePayment):

    def gen_html_post_form(self, action, parameters):
        html = '<form id="data_set" action="' + action + '" method="post">'
        for k, v in parameters.items():
            html += '<input type="hidden" name="' + \
                str(k) + '" value="' + str(v) + '" />'

        html += '<script type="text/javascript">document.getElementById("data_set").submit();</script>'
        html += "</form>"
        return html


class CvsMap(BasePayment):

    __CVS_MAP_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'MerchantTradeNo': {'type': str, 'required': False, 'max': 20},
        'LogisticsType': {'type': str, 'required': True, 'max': 20},
        'LogisticsSubType': {'type': str, 'required': True, 'max': 20},
        'IsCollection': {'type': str, 'required': True, 'max': 1},
        'ServerReplyURL': {'type': str, 'required': True, 'max': 200},
        'ExtraData': {'type': str, 'required': False, 'max': 20},
        'Device': {'type': int, 'required': False, },
    }

    __url = 'https://logistics.ecpay.com.tw/Express/map'
    __final_merge_parameters = dict()
    __check_pattern = []

    def cvs_map(self, client_parameters):
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CVS_MAP_PARAMETERS)
        self.__check_pattern.append(
            self.__CVS_MAP_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        # CheckMacValue 並無使用, 移除它
        self.final_merge_parameters.pop('CheckMacValue')

        return self.final_merge_parameters


class CreateShippingOrder(BasePayment):

    __CREATE_SHIPPING_ORDER_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'MerchantTradeNo': {'type': str, 'required': False, 'max': 20},
        'MerchantTradeDate': {'type': str, 'required': True, 'max': 20},
        'LogisticsType': {'type': str, 'required': True, 'max': 20},
        'LogisticsSubType': {'type': str, 'required': True, 'max': 20},
        'GoodsAmount': {'type': int, 'required': True, },
        'CollectionAmount': {'type': int, 'required': False, },
        'IsCollection': {'type': str, 'required': False, 'max': 1},
        'GoodsName': {'type': str, 'required': False, 'max': 50},
        'SenderName': {'type': str, 'required': True, 'max': 10},
        'SenderPhone': {'type': str, 'required': False, 'max': 20},
        'SenderCellPhone': {'type': str, 'required': False, 'max': 20},
        'ReceiverName': {'type': str, 'required': True, 'max': 10},
        'ReceiverPhone': {'type': str, 'required': False, 'max': 20},
        'ReceiverCellPhone': {'type': str, 'required': False, 'max': 20},
        'ReceiverEmail': {'type': str, 'required': False, 'max': 50},
        'TradeDesc': {'type': str, 'required': False, 'max': 200},
        'ServerReplyURL': {'type': str, 'required': True, 'max': 200},
        'ClientReplyURL': {'type': str, 'required': False, 'max': 200},
        'LogisticsC2CReplyURL': {'type': str, 'required': False, 'max': 200},
        'Remark': {'type': str, 'required': False, 'max': 200},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/Create'
    __final_merge_parameters = dict()
    __check_pattern = []

    def create_shipping_order(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CREATE_SHIPPING_ORDER_PARAMETERS)
        self.__check_pattern.append(self.__CREATE_SHIPPING_ORDER_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        # 回傳給 client
        response = super().send_post(
            action_url, self.final_merge_parameters)
        normal_qs = response.text.split('|')[1]
        query = dict(parse_qsl(normal_qs, keep_blank_values=True))

        return query


class CreateHomeReturnOrder(BasePayment):

    __CREATE_HOME_RETURN_ORDER_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': False, 'max': 20},
        'LogisticsSubType': {'type': str, 'required': False, 'max': 20},
        'ServerReplyURL': {'type': str, 'required': True, 'max': 200},
        'SenderName': {'type': str, 'required': False, 'max': 10},
        'SenderPhone': {'type': str, 'required': False, 'max': 20},
        'SenderCellPhone': {'type': str, 'required': False, 'max': 20},
        'SenderZipCode': {'type': str, 'required': False, 'max': 5},
        'SenderAddress': {'type': str, 'required': False, 'max': 60},
        'ReceiverName': {'type': str, 'required': False, 'max': 10},
        'ReceiverPhone': {'type': str, 'required': False, 'max': 20},
        'ReceiverCellPhone': {'type': str, 'required': False, 'max': 20},
        'ReceiverZipCode': {'type': str, 'required': False, 'max': 5},
        'ReceiverAddress': {'type': str, 'required': False, 'max': 60},
        'ReceiverEmail': {'type': str, 'required': False, 'max': 50},
        'GoodsAmount': {'type': int, 'required': True, },
        'GoodsName': {'type': str, 'required': False, 'max': 60},
        'Temperature': {'type': str, 'required': True, 'max': 4},
        'Distance': {'type': str, 'required': True, 'max': 2},
        'Specification': {'type': str, 'required': True, 'max': 4},
        'ScheduledPickupTime': {'type': str, 'required': False, 'max': 1},
        'ScheduledDeliveryTime': {'type': str, 'required': False, 'max': 2},
        'ScheduledDeliveryDate': {'type': str, 'required': False, 'max': 10},
        'PackageCount': {'type': int, 'required': True, },
        'Remark': {'type': str, 'required': False, 'max': 200},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/ReturnHome'
    __final_merge_parameters = dict()
    __check_pattern = []

    def create_home_return_order(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CREATE_HOME_RETURN_ORDER_PARAMETERS)
        self.__check_pattern.append(self.__CREATE_HOME_RETURN_ORDER_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        # 回傳給 client
        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class CreateFamilyB2CReturnOrder(BasePayment):

    __CREATE_FAMILY_B2C_RETURN_ORDER_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': False, 'max': 20},
        'ServerReplyURL': {'type': str, 'required': True, 'max': 200},
        'GoodsName': {'type': str, 'required': False, 'max': 50},
        'GoodsAmount': {'type': int, 'required': True, },
        'CollectionAmount': {'type': int, 'required': False, },
        'ServiceType': {'type': str, 'required': True, 'max': 5},
        'SenderName': {'type': str, 'required': True, 'max': 50},
        'SenderPhone': {'type': str, 'required': False, 'max': 20},
        'Remark': {'type': str, 'required': False, 'max': 20},
        'Quantity': {'type': str, 'required': False, 'max': 50},
        'Cost': {'type': str, 'required': False, 'max': 50},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/express/ReturnCVS'
    __final_merge_parameters = dict()
    __check_pattern = []

    def create_family_b2c_return_order(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CREATE_FAMILY_B2C_RETURN_ORDER_PARAMETERS)
        self.__check_pattern.append(
            self.__CREATE_FAMILY_B2C_RETURN_ORDER_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class CheckFamilyB2CLogistics(BasePayment):

    __CHECK_FAMILY_B2C_LOGISTICS_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'RtnMerchantTradeNo': {'type': str, 'required': True, 'max': 13},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Helper/LogisticsCheckAccoounts'
    __final_merge_parameters = dict()
    __check_pattern = []

    def check_family_b2c_logistics(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CHECK_FAMILY_B2C_LOGISTICS_PARAMETERS)
        self.__check_pattern.append(
            self.__CHECK_FAMILY_B2C_LOGISTICS_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class CreateHiLifeB2CReturnOrder(BasePayment):

    __CREATE_HILIFE_B2C_RETURN_ORDER_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': False, 'max': 20},
        'ServerReplyURL': {'type': str, 'required': True, 'max': 200},
        'GoodsName': {'type': str, 'required': False, 'max': 60},
        'GoodsAmount': {'type': int, 'required': True, },
        'CollectionAmount': {'type': int, 'required': False, },
        'ServiceType': {'type': str, 'required': True, 'max': 5},
        'SenderName': {'type': str, 'required': True, 'max': 50},
        'SenderPhone': {'type': str, 'required': False, 'max': 20},
        'Remark': {'type': str, 'required': False, 'max': 20},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/express/ReturnHiLifeCVS'
    __final_merge_parameters = dict()
    __check_pattern = []

    def create_hilife_b2c_return_order(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CREATE_HILIFE_B2C_RETURN_ORDER_PARAMETERS)
        self.__check_pattern.append(
            self.__CREATE_HILIFE_B2C_RETURN_ORDER_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class CreateUnimartB2CReturnOrder(BasePayment):

    __CREATE_UNIMART_B2C_RETURN_ORDER_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': False, 'max': 20},
        'ServerReplyURL': {'type': str, 'required': True, 'max': 200},
        'GoodsName': {'type': str, 'required': False, 'max': 50},
        'GoodsAmount': {'type': int, 'required': True, },
        'CollectionAmount': {'type': int, 'required': False, },
        'ServiceType': {'type': str, 'required': True, 'max': 5},
        'SenderName': {'type': str, 'required': True, 'max': 50},
        'SenderPhone': {'type': str, 'required': False, 'max': 20},
        'Remark': {'type': str, 'required': False, 'max': 20},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/express/ReturnUniMartCVS'
    __final_merge_parameters = dict()
    __check_pattern = []

    def create_unimart_b2c_return_order(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CREATE_UNIMART_B2C_RETURN_ORDER_PARAMETERS)
        self.__check_pattern.append(
            self.__CREATE_UNIMART_B2C_RETURN_ORDER_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class UpdateUnimartLogisticsInfo(BasePayment):

    # 訂單基本參數
    __UPDATE_UNIMART_LOGISTICS_INFO_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'ShipmentDate': {'type': str, 'required': False, 'max': 10},
        'ReceiverStoreID': {'type': str, 'required': False, 'max': 6},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Helper/UpdateShipmentInfo'
    __final_merge_parameters = dict()
    __check_pattern = []

    def update_unimart_logistics_info(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__UPDATE_UNIMART_LOGISTICS_INFO_PARAMETERS)
        self.__check_pattern.append(
            self.__UPDATE_UNIMART_LOGISTICS_INFO_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class UpdateUnimartStore(BasePayment):

    __UPDATE_UNIMART_STORE_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'CVSPaymentNo': {'type': str, 'required': True, 'max': 15},
        'CVSValidationNo': {'type': str, 'required': True, 'max': 10},
        'StoreType': {'type': str, 'required': True, 'max': 2},
        'ReceiverStoreID': {'type': str, 'required': False, 'max': 6},
        'ReturnStoreID': {'type': str, 'required': False, 'max': 6},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/UpdateStoreInfo'
    __final_merge_parameters = dict()
    __check_pattern = []

    def update_unimart_store(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__UPDATE_UNIMART_STORE_PARAMETERS)
        self.__check_pattern.append(self.__UPDATE_UNIMART_STORE_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class CancelUnimartLogisticsOrder(BasePayment):

    __CANCEL_UNIMART_LOGISTICS_ORDER_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'CVSPaymentNo': {'type': str, 'required': True, 'max': 15},
        'CVSValidationNo': {'type': str, 'required': True, 'max': 10},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/CancelC2COrder'
    __final_merge_parameters = dict()
    __check_pattern = []

    def cancel_unimart_logistics_order(self, action_url=__url, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CANCEL_UNIMART_LOGISTICS_ORDER_PARAMETERS)
        self.__check_pattern.append(
            self.__CANCEL_UNIMART_LOGISTICS_ORDER_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        response = super().send_post(
            action_url, self.final_merge_parameters)
        return response.text


class QueryLogisticsInfo(BasePayment):

    __QUERY_LOGISTICS_INFO_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'TimeStamp': {'type': int, 'required': True, },
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Helper/QueryLogisticsTradeInfo/V2'
    __final_merge_parameters = dict()
    __check_pattern = []

    def query_logistics_info(self, action_url=None, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__QUERY_LOGISTICS_INFO_PARAMETERS)
        self.__check_pattern.append(self.__QUERY_LOGISTICS_INFO_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        # 回傳給 client
        response = super().send_post(
            action_url, self.final_merge_parameters)
        query = dict(parse_qsl(response.text, keep_blank_values=True))

        return query


class PrintTradeDoc(BasePayment):

    __PRINT_TRADE_DOC_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/helper/printTradeDocument'
    __final_merge_parameters = dict()
    __check_pattern = []

    def print_trade_doc(self, action_url=None, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__PRINT_TRADE_DOC_PARAMETERS)
        self.__check_pattern.append(self.__PRINT_TRADE_DOC_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        return self.final_merge_parameters


class PrintUnimartC2CBill(BasePayment):

    __PRINT_UNIMART_C2C_BILL_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'CVSPaymentNo': {'type': str, 'required': True, 'max': 15},
        'CVSValidationNo': {'type': str, 'required': True, 'max': 10},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/PrintUniMartC2COrderInfo'
    __final_merge_parameters = dict()
    __check_pattern = []

    def print_unimart_c2c_bill(self, action_url=None, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__PRINT_UNIMART_C2C_BILL_PARAMETERS)
        self.__check_pattern.append(
            self.__PRINT_UNIMART_C2C_BILL_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        return self.final_merge_parameters


class PrintFamilyC2CBill(BasePayment):

    __PRINT_FAMILY_C2C_BILL_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'CVSPaymentNo': {'type': str, 'required': True, 'max': 15},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/PrintFAMIC2COrderInfo'
    __final_merge_parameters = dict()
    __check_pattern = []

    def print_family_c2c_bill(self, action_url=None, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__PRINT_FAMILY_C2C_BILL_PARAMETERS)
        self.__check_pattern.append(
            self.__PRINT_FAMILY_C2C_BILL_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        return self.final_merge_parameters


class PrintHiLifeC2CBill(BasePayment):

    __PRINT_HILIFE_C2C_BILL_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'AllPayLogisticsID': {'type': str, 'required': True, 'max': 20},
        'CVSPaymentNo': {'type': str, 'required': True, 'max': 15},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/PrintHILIFEC2COrderInfo'
    __final_merge_parameters = dict()
    __check_pattern = []

    def print_hilife_c2c_bill(self, action_url=None, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__PRINT_HILIFE_C2C_BILL_PARAMETERS)
        self.__check_pattern.append(
            self.__PRINT_HILIFE_C2C_BILL_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        return self.final_merge_parameters


class CreateTestData(BasePayment):

    __CREATE_TEST_DATA_PARAMETERS = {
        'MerchantID': {'type': str, 'required': True, 'max': 10},
        'ClientReplyURL': {'type': str, 'required': False, 'max': 200},
        'PlatformID': {'type': str, 'required': False, 'max': 10},
        'LogisticsSubType': {'type': str, 'required': True, 'max': 20},
    }

    __url = 'https://logistics.ecpay.com.tw/Express/CreateTestData'
    __final_merge_parameters = dict()
    __check_pattern = []

    def create_test_data(self, action_url=None, client_parameters={}):
        if action_url is None:
            action_url = self.__url
        # 先用 required.dict 設定預設值並產生新 new.required.dict
        default_parameters = dict()
        default_parameters = self.create_default_dict(
            self.__CREATE_TEST_DATA_PARAMETERS)
        self.__check_pattern.append(
            self.__CREATE_TEST_DATA_PARAMETERS)

        # 用 new.required.dict 與 client.dict 合併為 merge.dict
        self.final_merge_parameters = super().merge(
            default_parameters, client_parameters)

        # 檢查參數, 並產生 CheckMacValue
        self.final_merge_parameters = self.integrate_parameter(
            self.final_merge_parameters,
            self.__check_pattern)

        # 回傳給 client
        response = super().send_post(
            action_url, self.final_merge_parameters)
        query = dict(parse_qsl(response.text, keep_blank_values=True))

        return query


"""
主程式
"""
a = [CvsMap, CreateShippingOrder, CreateHomeReturnOrder,
     CreateFamilyB2CReturnOrder, CheckFamilyB2CLogistics,
     CreateHiLifeB2CReturnOrder, CreateUnimartB2CReturnOrder,
     UpdateUnimartLogisticsInfo, UpdateUnimartStore,
     CancelUnimartLogisticsOrder, QueryLogisticsInfo,
     PrintTradeDoc, PrintUnimartC2CBill, PrintFamilyC2CBill,
     PrintHiLifeC2CBill, CreateTestData,
     ExtendFunction]


class ECPayLogisticSdk(*a):

    def __init__(self, MerchantID='', HashKey='', HashIV=''):
        self.MerchantID = MerchantID
        self.HashKey = HashKey
        self.HashIV = HashIV
