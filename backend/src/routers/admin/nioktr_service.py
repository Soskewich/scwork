import asyncio
from datetime import datetime

from requests.auth import HTTPBasicAuth
from sqlalchemy.ext.asyncio import AsyncSession as Session
import requests
import time
import json
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession as Session

from src.model.model import Identifier,  Nioktr
from src.utils.aiohttp import SingletonAiohttp

# import pandas as pd
#
# # Загрузка данных из первой таблицы
# df1 = pd.read_excel('WosandScopus.xlsx')
#
# # Загрузка данных из второй таблицы
# # df2 = pd.read_excel('путь_к_второй_таблице.xlsx')
#
# # Подсчет уникальных значений в колонке "Title" для каждой из таблиц
# unique_count_df1 = df1['Title'].nunique()
# # unique_count_df2 = df2['Title'].nunique()
#
# print("Количество уникальных ячеек в первой таблице: ", unique_count_df1)
# # print("Количество уникальных ячеек во второй таблице: ", unique_count_df2)


uid = []
uid.append('9569096') #ОмГТУ
start_date = '2022-04-20'
end_date = '2022-04-23'
# URL API, который осуществляет поиск по ИС
search_url = 'https://rosrid.ru/api/base/search'
# Формируем заготовку для основного тела поиска
payload = {
    "search_query": None,
    "critical_technologies": [],
    "dissertations": False,
    "full_text_available": False,
    "ikrbses": False,
    "nioktrs": False,
    "organization": uid,
    "page": 1,
    "priority_directions": [],
    "rids": True,
    "rubrics": [],
    "search_area": "Во всех полях",
    "sort_by": "Дата регистрации",
    "open_license": False,
    "free_licenses": False,
    "expert_estimation_exist": False,
    "start_date": start_date,
    "end_date": end_date
}


# Создаём сессию и проставляем стандартные заголовки, что бы не сильно отличаться от браузера
session = requests.session()
session.headers.update({
    'authority': 'rosrid.ru',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'content-type': 'application/json;charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Linux"',
    'origin': 'https://rosrid.ru',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://rosrid.ru/global-search',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7'
})




def get_search_results(data, timeout=1):
    items_in_page = 10
    search_results = []
    try:
        resp = session.request("POST", search_url, verify=False, data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
        if resp.status_code == 200:
            json_resp = resp.json()
            page = data['page']

            total = json_resp['hits']['total']['value']
            # print(type(total))
            count_of_pages = (int(total / items_in_page) + 1) if total % items_in_page else total / items_in_page
            print(f"Downloaded data from page {page} of {count_of_pages}")

            if page < count_of_pages:
                # time.sleep(timeout)
                search_results += json_resp['hits']['hits'] + get_search_results({**data, 'page': page}, timeout)

            # Разкомментировать после тестов, проверка данных

                # for item in json_resp['hits']['hits']:



                    # print(item["_source"])

                    # key_len = len(item['_source']['keyword_list'])
                    # list_keywords = []
                    # # keyword
                    #
                    # keywords = item['_source']['keyword_list']
                    # for key in keywords:
                    #     list_keywords.append(key)
                    #
                    # print(list_keywords)
                    # page = payload['page']
                    # print("-------------------")
                    # print(page)
                    # print("-------------------")
                    # print(item['_source']['work_supervisor']['position'])
                    # count = 0
                    # types_len = len(item['_source']['nioktr_types'])
                    # for i in range(types_len):
                    #     budget_name = item['_source']['nioktr_types'][count]['name']
                    #     print(item['_source']['name'])
                    #     print("-------------------")
                    #     print(budget_name)
                    #     print("-------------------")
                    #     print(type(budget_name))
                    #     print("-------------------")
                    #     # print(budget_kbk)
                    #     # print("-------------------")
                    #     count += 1

                    # print(item['_source']['name'])

                    # for keyword_value in range(key_len):
                    #     if count_nir < key_len:
                    #         keyword_list = item['_source']['keyword_list'][count_nir]['name']
                    #
                    #
                    #         # print(nioktr['_source']['keyword_list'][count_nir]['name'])
                    #         count_nir += 1

                    # print(item['_source'])
                    # print(type(item))
                    # print(item['_source']['budgets'][count]['budget_type']['name'])
                    # count += 1
                    # print("-------------------")
                    # print(item['_source']['keyword_list'])
                    # print("-------------------")
                    # first_index = item['_source']['work_supervisor']['position'].find('«')
                    # first_index = item['_source']['work_supervisor']
                    # test = item['_source']['last_status']['created_date']
                    # new_test = test.split(" ")
                    # end_date = datetime.strptime(item['_source']['last_status']['created_date'][:10], "%Y-%m-%d").date()
                    # print(end_date)
                    # print(type(end_date))
                    # firstt_index = item['_source']['work_supervisor']['position'].find('"')
                    # department_index = item['_source']['work_supervisor']['position'].find('Кафедры')
                    # second_index = item['_source']['work_supervisor']['position'].find('»')
                    # secondd_index = item['_source']['work_supervisor']['position'].find('"')
                    # print("Исходный вариант:")
                    # print(item['_source']['work_supervisor']['name'])
                    # print("Измененный вариант:")
                    # print(item['_source']['work_supervisor']['position'][(first_index+1) or (firstt_index+1):(second_index) or (secondd_index-1)])
                    # print("Измененный вариант2222222:")
                    # print(item['_source']['work_supervisor']['position'][(firstt_index+1):(secondd_index)])

                    # print("-------------------")
                    # key_len = len(item['_source']['keyword_list'])
                    # for k in range(key_len):
                    #     if count < key_len:
                    #         print(item['_source']['keyword_list'][count]['name'])
                    #         count+=1 «»

        #Start Test

            #Сначала сделать зависимости с которыми связаны nioktr и параллельно заполнять поля
            # count_nir = 0
            # for nioktr in json_resp['hits']['hits']:
            #     if not nioktr['_source']['name']:
            #         continue
            #     nioktr_result = await db.execute(select(Nioktr).filter(Nioktr.name.ilike(nioktr['name'])))
            #     nir = nioktr_result.scalars().first()
            #     if nir is not None:
            #         continue
            #     keyword_list = nioktr['_source']['keyword_list']
            #     # keyword_list = nioktr['_source']['keyword_list']['name'] ????
            #
            #     count_nir += 1
            #     # nir = nioktr['_source']['name']
            #     print(f'{count_nir}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{nir}!!!!!!!!!!!!!!!!!!!!!!')


        # End Test


    #
    except BaseException as e:
        print('Retry connection', str(e))
        search_results = get_search_results({**data, 'page': 1}, timeout)

    return search_results
# #
res = get_search_results(data=payload)
print(res)
# #
# #
#
# name = "Никитин  К.И."
# print(len(name))
# new_name = name.split(' ')
# # pat_name = new_name[1].split('.')
# # print(name.split(' '))
# print(new_name[::len(new_name) - 1])

# test_list = [1, 5, 6, 7, 4]
#
# # printing original list
# print("The original list is : " + str(test_list))
#
# # using List slicing
# # to get first and last element of list
# res = test_list[::len(test_list) - 1]


# сделать авторов, с различными условиями заполнения, с года которые указны в этом файле
# заполнить наконец то всю базу нирами и перейти на фронт


