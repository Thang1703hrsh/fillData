from bs4 import BeautifulSoup
from regex import S
import requests
from lxml import html
import json
import pandas as pd

import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)

# API đăng nhập 
domain = 'http://ttd-api.tms-s.vn'

LOGIN_URL = "{main}/api/v1/login".format(main = domain)
# data đăng nhập
payload = {
    'username': 'admin02',
    'password': 'ttd123@',
}

def getPost(link):
    r = requests.post(link)
    responseObject = r.json()
    responseObject_view = json.dumps(r.json(), indent=2)
    return responseObject_view , responseObject

link_page = 'https://ttd-api.tms-s.vn/api/get-data/auth/post/products?page=1&permis=1'

link_npl = 'http://ttd-api.tms-s.vn/api/get-data/auth/post/product/6806'

view_data_page, data_page = getPost(link_page) 
view_data_npl, data_npl = getPost(link_npl) 
print(view_data_page)
# print(view_data_npl)
# dict_NPL = {"ID": [] , "Mã vật tư":[] , "Tên vật tư":[], "Loại":[] ,"Định mức": [], "Thực tồn" :[] ,"Trừ tạm": []}

# temp1 = []
# temp2 = []
# temp3 = []
# def scrapyThucap(idNpl , bac , tree):
#     link_npl = 'http://ttd-api.tms-s.vn/api/get-data/auth/post/product/{}'.format(idNpl)
#     view_data_npl, data_npl = getPost(link_npl)
#     detail = data_npl["product_detail"]
#     detail_Material = detail["allMaterial"]
#     arr_id = []
#     if(detail_Material == []):
#         return
#     else:
#         for i in range(0 , len(detail_Material)):
#             id_info = detail_Material[i]["product_id"]
#             arr_id.append(id_info)
#             print(id_info)
#             infor = detail_Material[i]["material_info"]
#             code = infor["code"]
#             name = infor["name"]
#             dinhmuc = infor["ratio_quota"]
            
#             dict_NPL["Mã vật tư bac={ba} ind={index} tree={tr}".format(ba = bac , index = i+1 , tr = tree)].append(code)
#             dict_NPL["Tên vật tư bac={ba} ind={index} tree={tr}".format(ba = bac , index = i+1 , tr = tree)].append(name)
#             dict_NPL["Định mức bac={ba} ind={index} tree={tr}".format(ba = bac , index = i+1 , tr = tree)].append(dinhmuc)

#             scrapyThucap(idNpl , bac + 1 , tree + 1)

# ttnpl = data_page["products"]["data"]

# for i in range(0 , len(ttnpl)):
#     idNpl = ttnpl[i]["product_id"]
#     print(idNpl)
#     dict_NPL["ID"].append(idNpl)
#     mavt = ttnpl[i]["code"]
#     dict_NPL["Mã vật tư"].append(mavt)
    
#     tenvt = ttnpl[i]["name"]
#     dict_NPL["Tên vật tư"].append(tenvt)

#     loai = ttnpl[i]["is_outsourcing"]
#     if(loai == 0):
#         loai = "Sơ cấp"
#     else:
#         loai = "Thứ cấp"
#     dict_NPL["Loại"].append(loai)

#     dict_NPL["Định mức"].append(0)

#     thucton = ttnpl[i]["quantity"]
#     dict_NPL["Thực tồn"].append(thucton)

#     trutam = ttnpl[i]["temp_quantity"]
#     dict_NPL["Trừ tạm"].append(trutam)

#     scrapyThucap(idNpl , 1 , 0)

# print(dict_NPL)

# # df_theodoi = pd.DataFrame.from_dict(dict_NPL)

# dict_NPL = {"ID": [] , "Mã vật tư":[] , "Tên vật tư":[] ,"Định mức": [], "Thực tồn" :[] ,"Trừ tạm": [], "Loại":[]}

# dict_NPL_TC = {"ID_TC": [] , "Mã vật tư TC":[] , "Tên vật tư TC":[] ,"Định mức TC": []}
# dict_NPL_SC = {"ID_SC": [] , "Mã vật tư SC":[] , "Tên vật tư SC":[] ,"Định mức SC": []}
# for i in range(0 , len(ttnpl)):
    

# dict_NPL_TC = {"ID_TC": [] , "Mã vật tư TC":[] , "Tên vật tư TC":[] ,"Định mức TC": [], "Thực tồn TC" :[] ,"Trừ tạm TC": [], "Loại TC":[]}
# dict_NPL_SC = {"ID_SC": [] , "Mã vật tư SC":[] , "Tên vật tư SC":[] ,"Định mức SC": [], "Thực tồn SC" :[] ,"Trừ tạm SC": [], "Loại SC":[]}



