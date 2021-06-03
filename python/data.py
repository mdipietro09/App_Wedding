
import names
import pandas as pd
import numpy as np


'''
Generate random guests list
:parameter
    :param n: num - number of guests and length of dtf
    :param lst_categories: list - ["family", "friends", "university", ...]
    :param n_rules: num - number of restrictions to apply (ex. if 1 then 2 guests can't be sit together)
:return
    dtf with guests
'''
def random_data(n=100, lst_categories=["family","friends","work","university","tennis"], n_rules=0):
    ## basic list
    lst_dics = []
    for i in range(n):
        name = names.get_full_name()
        category = np.random.choice(lst_categories) if len(lst_categories) > 0 else np.nan
        lst_dics.append({"id":i, "name":name, "category":category, "avoid":np.nan})
    dtf = pd.DataFrame(lst_dics)

    ## add rules
    if n_rules > 0:
        for i in range(n_rules):
            choices = dtf[dtf["avoid"].isna()]["id"]
            ids = np.random.choice(choices, size=2)
            dtf["avoid"].iloc[ids[0]] = int(ids[1]) if int(ids[1]) != ids[0] else int(ids[1])+1

    return dtf




