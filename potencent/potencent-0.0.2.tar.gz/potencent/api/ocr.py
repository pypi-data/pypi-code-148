# -*- coding: UTF-8 -*-
'''
@Author  ：程序员晚枫，B站/抖音/微博/小红书/公众号
@WeChat     ：CoderWanFeng
@Blog      ：www.python-office.com
@Date    ：2023/1/22 15:23
@Description     ：
'''

from potencent.core.OCR import OCR
from potencent.lib.CommonUtils import img2base64


def get_ocr(configPath):
    ocr = OCR()
    ocr.set_config(configPath)
    return ocr


def VatInvoiceOCR(img_path=None, configPath=None):
    """
    增值税发票的识别
    :param img_path: 必填，发票的图片位置
    :param configPath: 选填，配置文件的位置，有默认值
    :return:
    """
    ocr = get_ocr(configPath)
    ImageBase64 = img2base64(img_path)
    ocr_res = ocr.VatInvoiceOCR(ImageBase64)
    return ocr_res

def BankCardOCR(img_path=None, configPath=None):
    """
    银行卡号码的识别
    :param img_path: 必填，银行卡的图片位置
    :param configPath: 选填，配置文件的位置，有默认值
    :return:
    """
    ocr = get_ocr(configPath)
    ImageBase64 = img2base64(img_path)
    ocr_res = ocr.BankCardOCR(ImageBase64)
    return ocr_res