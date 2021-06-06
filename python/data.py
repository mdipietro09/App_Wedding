
import names
import pandas as pd
import numpy as np
import base64
import io


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


'''
When a file is uploaded it contains "contents", "filename", "date"
:parameter
    :param contents: file
    :param filename: str
:return
    pandas table
'''
def load_file(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            return pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            return pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print("ERROR:", e)
        return 'There was an error processing this file.'




