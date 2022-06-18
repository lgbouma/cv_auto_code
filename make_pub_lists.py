## import all the things
import numpy as np
import requests
import json
import pandas as pd
import bibtexparser
import sys

## get my token
token = np.loadtxt("my_key.txt", dtype=str)
token = str(token)

## get my libraries
libs, fns = np.loadtxt("my_libraries.txt", dtype=str, unpack=True)

def get_df(lib):
    ## get my papers from library
    r = requests.get("https://api.adsabs.harvard.edu/v1/biblib/libraries/"+lib,\
                    headers={'Authorization': 'Bearer ' + token})
    docs = r.json()['documents']
    ## get bibtex
    payload = {"bibcode":docs}
    r = requests.post("https://api.adsabs.harvard.edu/v1/export/bibtex", \
                     headers={"Authorization": "Bearer " + token, "Content-type": "application/json"}, \
                     data=json.dumps(payload))
    bibtex = r.json()['export']
    ## parse bibtex
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    parser.homogenise_fields = False
    bib_database = bibtexparser.loads(bibtex, parser = parser)
    ## get df
    df = pd.DataFrame(bib_database.entries)
    ## select needed columns
    try:
        selection = df[['author', 'title', 'journal', 'volume', 'number', 'eid', 'adsurl', 'primaryclass']]
    except: ##above will throw error if only nonref papers
            selection = df[['author', 'title', 'journal', 'eid', 'adsurl', 'primaryclass']]
    return selection

def fix_auth(entry):
    text = entry['author'].replace(' and ', '; ')
    names = np.loadtxt('my_names.txt', dtype=str, delimiter='\n')
    for n in names:
        text = text.replace(str(n), f'\\textbf{{{str(n)}}}')
    return text

def make_item(e):
    auths = fix_auth(e)
    title = f'\\textit{{{e["title"]}}}'
    s = ', '
    if e['journal'] == 'arXiv e-prints':
        url = f'\\href{{{e["adsurl"]}}}{{{e["eid"]}}}'
    else:
        url = f'\\href{{{e["adsurl"]}}}{{{s.join([e["journal"], e["volume"], e["number"], e["eid"]])}}}'
    if e['primaryclass'] == 'hep-ph':
        final = '\\item $\\dagger$ '+ s.join([auths, title, url])
    else:
        final = '\\item '+ s.join([auths, title, url])
    return final

#### Run
if __name__ == "__main__":
    if not isinstance(libs, (np.ndarray, list)): libs = [libs]
    if not isinstance(fns, (np.ndarray, list)): fns = [fns]
    for i,l in enumerate(libs):
        df = get_df(l)
        with open(fns[i], 'w') as f:
            for _,e in df.iterrows():
                f.write(make_item(e)+'\n \n')
        print(f'Wrote {fns[i]}. Has {len(df)} entries.')
