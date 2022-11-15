import pandas as pd
import numpy as np

dfChild = pd.read_excel("NPL_Child_dequy.xlsx" , sheet_name = "Sheet1")
dfParent = pd.read_excel("NPL_Parent_dequy.xlsx" , sheet_name = "Sheet1")

g = dfChild.groupby(["ID_Parent"]).cumcount().add(1)
dfChildMerge = dfChild.set_index(["ID_Parent", g]).unstack(fill_value=0).sort_index(axis=1, level=1)
dfChildMerge.columns = ["{}{}".format(a, b) for a, b in dfChildMerge.columns]

dfChildMerge = dfChildMerge.reset_index()

dfChildMerge = dfChildMerge.replace(np.nan, 0)

print(dfChildMerge)

dfTotal = pd.merge(dfParent, dfChildMerge, on='ID_Parent', how='inner')

print(dfTotal)