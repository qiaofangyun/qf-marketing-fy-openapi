import requests
import logging
import unittest
from api.common.readconfig import conf
from api.common.timeSignUtil import get_now_time_sign
from api.common.signatureUtil import get_signature

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def PullResourceUuidList(scrollId):
    env = conf.get('common', 'runEnv')
    baseUrl = conf.get(env, 'marketingopenapi_url')
    appId = conf.get('common', 'appId')
    key = conf.get('common', 'key')
    time_sign = get_now_time_sign()
    header = {
        "Content-Type": "application/json;charset=UTF-8",
        "appId": appId,
        "timeSign": str(time_sign),
        "signature": get_signature(appId, key, time_sign)
    }
    requests_url = baseUrl + '/company/pullResourceUuidList'
    payload = {
        "dto":
            {
                # "endUpdatedTime": "2020-05-27 16:33:00",
                "scrollId": scrollId,
                # "startUpdatedTime": "2020-05-27 12:00:00",
                "useAsc": "true",
                "windowSize": 100
            },
        "resourceType": "PROPERTY_VIDEO"
    }
    r = requests.post(requests_url, json=payload, headers=header)
    return r.json()


def all_video():
    property_list = PullResourceUuidList(scrollId=None)
    scrollId = property_list['data']['scrollId']
    print(property_list['data']['listSize'])
    while scrollId is not None:
        property_list = PullResourceUuidList(scrollId)
        scrollId = property_list['data']['scrollId']
        print(property_list['data']['listSize'])
        if property_list['data']['listSize'] == 0:
            break


if __name__ == '__main__':
    all_video()
