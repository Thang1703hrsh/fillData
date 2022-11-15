from bs4 import BeautifulSoup
from regex import S
import requests
from lxml import html
import json
import pandas as pd
import numpy as np

import sys, threading
sys.setrecursionlimit(10**7) # max depth of recursion
threading.stack_size(2**27)
pd.set_option('display.max_rows', None)

# API đăng nhập 
domain = 'http://ttd-api.tms-s.vn'

loginUrl = "{main}/api/v1/login".format(main = domain)
# data đăng nhập
payload = {
    'username': 'admin02',
    'password': 'ttd123@',
}

def getPost(link):
    r = requests.post(link)
    responseObject = r.json()
    responseObjectView = json.dumps(r.json(), indent=2)
    return responseObjectView , responseObject

## Đọc thông tin chi tiết của từng nguyên phụ liệu sơ cấp cấu thành nên thứ cấp 
def scrapyThucap(idNpl):
    url = 'http://ttd-api.tms-s.vn/api/get-data/auth/post/product/{}'.format(idNpl)
    viewDetailMaterial, dataDetailMaterial = getPost(url)
    detail = dataDetailMaterial["product_detail"]
    detailMaterial = detail["allMaterial"]
    b = []
    ## detailMaterial là thông tin sơ cấp của NPL đang xét
    ## Trường hợp detailMaterial không tồn tại
    if(detailMaterial == []):
        pass
    ## Trường hợp detailMaterial tồn tại
    else:
        for i in range(0 , len(detailMaterial)):
            idInfor = detailMaterial[i]["product_id"]
            outIdInf = detailMaterial[i]["outsourcing_product_id"]
            b.append(outIdInf)
            b.append(idInfor)
            # arr_id.append(idInfor)
            infor = detailMaterial[i]["material_info"]
            code = infor["code"]
            b.append(code)
            name = infor["name"]
            b.append(name)
            try:
                ratioQuota = infor['ratio_quota']
            except KeyError:
                continue
            b.append(ratioQuota)
            c = scrapyThucap(idInfor)
            b.extend(c)
    return b

dictNpl = {"ID": []}
def scrapyPage(indpage):
    url = 'https://ttd-api.tms-s.vn/api/get-data/auth/post/products?page={}&permis=1'.format(indpage)
    viewDataPage, dataPage = getPost(url) 
    if(indpage > dataPage["products"]["last_page"]):
    # if(indpage > 1):
        return 0
    else:
        ttnpl = dataPage["products"]["data"]

        for i in range(0 , len(ttnpl)):
            temp = []
            product_id = ttnpl[i]["product_id"]
            temp.append(product_id)
            code = ttnpl[i]["code"]
            print(code)
            temp.append(code)
            
            name = ttnpl[i]["name"]
            temp.append(name)

            is_outsourcing = ttnpl[i]["is_outsourcing"]
            if(is_outsourcing == 0):
                is_outsourcing = "Sơ cấp"
            else:
                is_outsourcing = "Thứ cấp"

            temp.append(0)

            quantity = ttnpl[i]["quantity"]
            temp.append(quantity)

            temp_quantity = ttnpl[i]["temp_quantity"]
            temp.append(temp_quantity)

            temp.append(is_outsourcing)

            b = scrapyThucap(product_id)
            temp.extend(b)

            dictNpl["ID"].append(temp)
    scrapyPage(indpage + 1)

scrapyPage(1)
print(dictNpl)
print("------------------------------------------------")

def append_SC(dictNplSc, dictNpl, indexNpl, indexArr):
    dictNplSc["ID_Parent"].append(dictNpl["ID"][indexNpl][indexArr])
    dictNplSc["ID_Child"].append(dictNpl["ID"][indexNpl][indexArr+1])
    dictNplSc["Mã vật tư Child"].append(dictNpl["ID"][indexNpl][indexArr+2])
    dictNplSc["Tên vật tư Child"].append(dictNpl["ID"][indexNpl][indexArr+3])
    dictNplSc["Định mức Child"].append(dictNpl["ID"][indexNpl][indexArr+4])
    return dictNplSc

## Chuyển dictNpl tổng thành file con chứa thông tin parent - child
dictNplAll = {"ID_Parent": [] , "Mã vật tư Parent":[] , "Tên vật tư Parent":[] ,"Định mức Parent": [], "Thực tồn Parent" :[] ,"Trừ tạm Parent": [], "Loại Parent":[]}
dictNplSc = {"ID_Parent": [], "ID_Child": [] , "Mã vật tư Child":[] , "Tên vật tư Child":[] ,"Định mức Child": []}

for i in range(0 , len(dictNpl["ID"])):
    lenNpl = len(dictNpl["ID"][i])
    dictNplAll["ID_Parent"].append(dictNpl["ID"][i][0])
    dictNplAll["Mã vật tư Parent"].append(dictNpl["ID"][i][1])
    dictNplAll["Tên vật tư Parent"].append(dictNpl["ID"][i][2])
    dictNplAll["Định mức Parent"].append(dictNpl["ID"][i][3])
    dictNplAll["Thực tồn Parent"].append(dictNpl["ID"][i][4])
    dictNplAll["Trừ tạm Parent"].append(dictNpl["ID"][i][5])
    dictNplAll["Loại Parent"].append(dictNpl["ID"][i][6])
    if(lenNpl == 8):
        continue
    else: 
        for j in range(0 , int((lenNpl-7)/5)):
            dictNplSc = append_SC(dictNplSc , dictNpl, i, lenNpl - 5*(int((lenNpl-7)/5) - j))  

print(dictNplAll)
print(dictNplSc)

dfNplParent = pd.DataFrame.from_dict(dictNplAll)
dfNplChild = pd.DataFrame.from_dict(dictNplSc)

dfNplParent.to_excel("dfNplParent.xlsx", index=False)
dfNplChild.to_excel("dfNplChild.xlsx", index=False)



# g = dfNplChild.groupby(["ID_Parent"]).cumcount().add(1)
# dfNplChildMerge = dfNplChild.set_index(["ID_Parent", g]).unstack(fill_value=0).sort_index(axis=1, level=1)
# dfNplChildMerge.columns = ["{}{}".format(a, b) for a, b in dfNplChildMerge.columns]

# dfNplChildMerge = dfNplChildMerge.reset_index()

# dfNplChildMerge = dfNplChildMerge.replace(np.nan, 0)

# print(dfNplChildMerge)

# dfTotal = pd.merge(dfNplParent, dfNplChildMerge, on='ID_Parent', how='inner')

# dfNplChild.to_excel("NplTotal.xlsx", index=False)

