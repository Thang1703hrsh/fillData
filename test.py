from asyncio.windows_events import NULL
from unittest import skip
from bs4 import BeautifulSoup
from regex import S
import requests
from lxml import html
import json
import pandas as pd
import numpy as np


dictNplAll = {"ID_Parent": [] , "Mã vật tư Parent":[] , "Tên vật tư Parent":[] ,"Định mức Parent": [], "Thực tồn Parent" :[] ,"Trừ tạm Parent": [], "Loại Parent":[]}
dictNplSc = {"ID_Parent": [], "ID_Child": [] , "Mã vật tư Child":[] , "Tên vật tư Child":[] ,"Định mức Child": []}
for i in range(1,10):
  dictNplSc = {"ID_Parent_{}".format(i): [], "ID_Child_{}".format(i): [] , "Mã vật tư Child_{}".format(i):[] , "Tên vật tư Child_{}".format(i):[] ,"Định mức Child_{}".format(i): []}
  dictNplAll.update(dictNplSc)

print(dictNplAll)