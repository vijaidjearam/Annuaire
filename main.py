import requests
import json
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, landscape
import numpy as np
from pyodide.http import pyfetch, FetchResponse
from pyscript import document

def get_json(servID):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://annuaires.univ-reims.fr',
        'Referer': 'http://annuaires.univ-reims.fr/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    data = {
        's': 'IUT TR|'+servID,
        'e': 'n',
    }
    response = requests.post('http://annuaires.univ-reims.fr/ws/searchService.php', headers=headers, data=data, verify=False)
    r = response.text
    content = json.loads(r)
    #response = pyfetch('https://annuaires.univ-reims.fr/ws/searchService.php', method="POST", headers=headers, data=data)
    #content =  response.json()
    #content = json.loads(content)
    content = content["entry"]
    return content

def sortdata(content):
    df = pd.DataFrame.from_records(content)
    df['num_interne']= "8"+ df['num_externe'].str.extract(r'\d{2}.\d{2}.\d{2}(.\d{2}.\d{2})')
    df.sort_values(by='nom',inplace=True)
    df1 = df[['nom','prenom','num_externe','num_interne','serv']]
    filt = (df1['nom'] == 'TELECOPIE') | (df['prenom'] == 'TELECOPIE')
    df2 = df1.loc[~filt]
    return df2

def generatepdf(dataframe):
    outfilename = 'Annuaire.pdf'
    outfiledir = 'c:\\temp'
    outfilepath = os.path.join( outfiledir, outfilename )
    pdf = SimpleDocTemplate(
        outfilepath,
        pagesize=landscape(letter)
    )
    from reportlab.platypus import Table
    #table = Table(np.array(df1).tolist())
    table=Table([['Nom','Pronom','Num_externe','Num_interne','Service']]+dataframe.values.tolist(),splitByRow=1,repeatRows=1)
    # add style
    from reportlab.platypus import TableStyle
    from reportlab.lib import colors

    # 1) Styling Header and other rows
    style = TableStyle([
        ('BACKGROUND', (0,0), (4,0), colors.green),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),

        ('BOTTOMPADDING', (0,0), (-1,0), 12),

        ('BACKGROUND',(0,1),(-1,-1),colors.beige),
    ])
    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(dataframe.index) + 1
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige
        
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc),
             ('FONTSIZE', (0,i), (-1,i), 8),]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
        ('BOX',(0,0),(-1,-1),2,colors.black),

        ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
        ('LINEABOVE',(0,2),(-1,2),2,colors.green),

        ('GRID',(0,1),(-1,-1),2,colors.black),
        ]
    )
    table.setStyle(ts)
    elems = []
    elems.append(table)
    pdf.build(elems)


def submit(event):
    service = document.querySelector("#Service")
    output_div = document.querySelector("#output")
    output_div.innerText = service.value
    ServID = service.value  
    content = get_json(ServID)
    dataframe = sortdata(content)
    generatepdf(dataframe)

