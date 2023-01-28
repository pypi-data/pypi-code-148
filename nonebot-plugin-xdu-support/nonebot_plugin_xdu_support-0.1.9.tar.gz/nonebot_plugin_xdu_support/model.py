import time
import pytz
import datetime
import requests
from libxduauth import EhallSession, SportsSession
import json
from datetime import datetime, timedelta
from typing import List, Dict, Union
from pathlib import Path
import os
from .data_source import questions_multi, questions_single
import random
from nonebot.adapters.onebot.v11 import Message
from pyDes import des, CBC, PAD_PKCS5
import binascii

# 晨午晚检------------------------------------------------------------------------


def commit_data(username: str, password: str) -> str:
    sess = requests.session()
    sess.post(
        'https://xxcapp.xidian.edu.cn/uc/wap/login/check', data={
            'username': username,
            'password': password
        })
    return sess.post(
        'https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save',
        data={
            'sfzx': '1',
            'tw': '1',
            'area': '陕西省 西安市 长安区',
            'city': '西安市',
            'province': '陕西省',
            'address': '陕西省西安市长安区兴隆街道竹园3号宿舍楼西安电子科技大学南校区',
            'geo_api_info': '{"type":"complete","position":{"Q":34.127332356771,"R":108.83943196614598,"lng":108.839432,"lat":34.127332},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":30,"isConverted":true,"status":1,"addressComponent":{"citycode":"029","adcode":"610116","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"竹园一路","streetNumber":"248号","country":"中国","province":"陕西省","city":"西安市","district":"长安区","towncode":"610116016000","township":"兴隆街道"},"formattedAddress":"陕西省西安市长安区兴隆街道竹园3号宿舍楼西安电子科技大学南校区","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
            'sfcyglq': '0',
            'sfyzz': '0',
            'qtqk': '',
            'ymtys': '0'}).json()['m']


def get_hour_message() -> str:
    h = datetime.datetime.fromtimestamp(
        int(time.time()), pytz.timezone('Asia/Shanghai')).hour
    if 6 <= h <= 11:
        return '晨'
    elif 12 <= h <= 17:
        return '午'
    elif 18 <= h <= 24:
        return '晚'
    else:
        return '凌晨'


def check(username: str, password: str) -> str:
    message = ''
    try:
        message += commit_data(username, password)
        message += '\n' + (get_hour_message()) + '检-'

    except BaseException:
        message += '信息有误或网页无法打开,操作失败'
    return message

# 体育打卡----------------------------------------------------------------------------------


def cron_check(ses: SportsSession, username: str) -> (bool, str):
    message = ''

    response = ses.post(ses.BASE_URL + 'stuTermPunchRecord/findList',
                        data={
                            'userId': ses.user_id
                        }).json()
    term_id = response['data'][0]['sysTermId']

    response2 = ses.post(ses.BASE_URL + 'stuPunchRecord/findPagerOk',
                         data={
                             'userNum': username,
                             'sysTermId': term_id,
                             'pageSize': 999,
                             'pageIndex': 1
                         }).json()

    vaild_punch_data = response2['data']

    return False, message


def get_sport_record(ses: SportsSession, username: str) -> (bool, str):
    message = ''

    response = ses.post(ses.BASE_URL + 'stuTermPunchRecord/findList',
                        data={
                            'userId': ses.user_id
                        }).json()
    term_id, term_name = response['data'][0]['sysTermId'], response['data'][0]['sysTerm']
    name = response['data'][0]['name']
    vaild_punch_times = response['data'][0]['goodNum']

    message += f"当前学期: {term_name}\n"
    response2 = ses.post(ses.BASE_URL + 'stuPunchRecord/findPagerOk',
                         data={
                             'userNum': username,
                             'sysTermId': term_id,
                             'pageSize': 999,
                             'pageIndex': 1
                         }).json()

    message += f"姓名:{name}\n" \
               f"学号:{username}\n" \
               f"有效打卡次数为:{vaild_punch_times}\n"
    if vaild_punch_times >= 50:
        message += "恭喜您已经完成体育打卡了!,即将为您自动取消订阅"
        return True, message
    vaild_punch_data = response2['data']

    return False, message

# 课表查询------------------------------------------------------------------


def get_timetable(ses: EhallSession, username: str,
                  basic_path: Union[Path, str]):
    semesterCode = ses.post(
        'http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/jshkcb/dqxnxq.do',
        headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
    ).json()['datas']['dqxnxq']['rows'][0]['DM']
    termStartDay = datetime.strptime(ses.post(
        'http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/jshkcb/cxjcs.do',
        headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        },
        data={
            'XN': semesterCode.split('-')[0] + '-' + semesterCode.split('-')[1],
            'XQ': semesterCode.split('-')[2]
        }
    ).json()['datas']['cxjcs']['rows'][0]["XQKSRQ"].split(' ')[0], '%Y-%m-%d')
    qResult = ses.post(
        'http://ehall.xidian.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do',
        headers={  # 学生课程表
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }, data={
            'XNXQDM': semesterCode
        }
    ).json()
    qResult = qResult['datas']['xskcb']  # 学生课程表
    if qResult['extParams']['code'] != 1:
        raise Exception(qResult['extParams']['msg'])

    courseList = []
    for i in qResult['rows']:
        while len(courseList) < len(i['SKZC']):
            courseList.append([[], [], [], [], [], [], []])
        for j in range(len(i['SKZC'])):
            if i['SKZC'][j] == '1' and int(
                    i['KSJC']) <= 10 and int(
                    i['JSJC']) <= 10:
                courseList[j][int(i['SKXQ']) - 1].append({
                    'name': i['KCM'],
                    'location': i['JASMC'],
                    'sectionSpan': (int(i['KSJC']), int(i['JSJC']))
                })
    remake = {}
    for week_cnt in range(len(courseList)):
        for day_cnt in range(len(courseList[week_cnt])):
            if courseList[week_cnt][day_cnt]:
                date = termStartDay + \
                    timedelta(days=week_cnt * 7 + day_cnt)  # 从第一 周的第一天起
                remake[f"{date.year}-{date.month}-{date.day}"] = {}
                for course in courseList[week_cnt][day_cnt]:
                    if course['sectionSpan'][0] > 10:
                        continue
                    elif course['location'] is None:
                        course['location'] = '待定'
                    remake[f"{date.year}-{date.month}-{date.day}"][int(course['sectionSpan'][1] / 2 - 1)] = {
                        'name': course['name'],
                        'location': course['location'],
                    }
    with open(os.path.join(basic_path, f"{username}-remake.json"), "w", encoding="utf-8") as f:

        f.write(json.dumps(remake, ensure_ascii=False))


def get_next_course(username: str, basic_path: Union[Path, str]) -> str:
    message = ""
    with open(os.path.join(basic_path, f"{username}-remake.json"), "r", encoding="utf-8") as f:
        courses = json.loads(f.read())
    today = datetime.now()
    if courses.get(f"{today.year}-{today.month}-{today.day}", None):
        today_course = courses.get(
            f"{today.year}-{today.month}-{today.day}", None)
        if today.hour == 8:
            if today_course.get(0, None):
                course = today_course.get(0)
                message += f"小小垚温馨提醒\n今天8:30-10.05\n你有一节 {course['name']} 在 {course['location']}上，\n请合理安排时间，不要迟到"
        elif today.hour == 9:
            if today_course.get(1, None):
                course = today_course.get(1)
                message += f"小小垚温馨提醒\n今天10:25-12:00\n你有一节 {course['name']} 在 {course['location']}上，\n请合理安排时间，不要迟到"
        elif today.hour == 13:
            if today_course.get(2, None):
                course = today_course.get(2)
                message += f"小小垚温馨提醒\n今天14:00-15:35\n你有一节 {course['name']} 在 {course['location']}上，\n请合理安排时间，不要迟到"
        elif today.hour == 15:
            if today_course.get(3, None):
                course = today_course.get(3)
                message += f"小小垚温馨提醒\n今天15:55-17:30\n你有一节 {course['name']} 在 {course['location']}上，\n请合理安排时间，不要迟到"
        elif today.hour == 18:
            if today_course.get(4, None):
                course = today_course.get(4)
                message += f"小小垚温馨提醒\n今天19:00-20:35\n你有一节 {course['name']} 在 {course['location']}上，\n请合理安排时间，不要迟到"
    return message


def get_whole_day_course(username: str, time_sche: List,
                         basic_path: Union[Path, str], _time: int = 0) -> str:
    message = ""
    with open(os.path.join(basic_path, f"{username}-remake.json"), "r", encoding="utf-8") as f:
        courses = json.loads(f.read())
    today = datetime.now()
    y = today.year
    m = today.month
    d = today.day
    if _time == 1:
        d += 1
    if courses.get(f"{y}-{m}-{d}", None):

        today_course: Dict = courses.get(
            f"{y}-{m}-{d}", None)
        if _time == 0:
            message += f"今天一共有{len(list(today_course.keys()))}结课需要上\n"
        else:
            message += f"明天一共有{len(list(today_course.keys()))}结课需要上\n"
        message += "****************\n"
        for i in range(4):
            if today_course.get(i, None):
                message += f"{time_sche[i]} 有一节{today_course[i]['name']}\n上课地点在{today_course[i]['location']}\n"
                message += "****************\n"
    else:
        if _time == 0:
            message += "今天没有课哦，安排好时间，合理学习合理放松吧!"
        else:
            message += "明天没有课哦，安排好时间，合理学习合理放松吧!"

    return message


def get_question(mode: int) -> (Message, Message, Message):
    """
    返回一道随机题目以及答案
    :param mode: 1为单选，2为多选，3为任意题型随机
    :return:如果返回None,则为假
    """
    questions_single_des = list(questions_single.keys())
    questions_multi_des = list(questions_multi.keys())
    if mode == 1:
        res = random.choice(questions_single_des)
        ans = questions_single.get(res)
        _type = "[单选题]\n"
    elif mode == 2:
        res = random.choice(questions_multi_des)
        ans = questions_multi.get(res)
        _type = "[多选题]\n"
    elif mode == 3:
        rand = random.random()
        if rand < 0.4:
            res = random.choice(questions_multi_des)
            ans = questions_multi.get(res)
            _type = "[多选题]\n"
        else:
            res = random.choice(questions_single_des)
            ans = questions_single.get(res)
            _type = "[单选题]\n"
    else:
        res = None
        ans = None
        _type = None
    return res, ans, _type

# 加密解密-------------------------------------------------


def des_encrypt(s: str, key: str) -> bytes:
    secret_key = key
    iv = secret_key
    des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    secret_bytes = des_obj.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(secret_bytes)


def des_descrypt(s: str, key: str) -> bytes:
    secret_key = key
    iv = secret_key
    des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    decrypt_str = des_obj.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return decrypt_str
