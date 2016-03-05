import os
import csv
import sys
import requests
import re
import decimal

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]

def odpri(imedatoteke):
    with open(imedatoteke, encoding='utf8') as contents:
        napisano=contents.read()
        napisano = ''.join(napisano.split())
    return napisano

def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)

def vreme_ikone(ikonica):
    if ikonica=='WM1': return 'sončno'
    elif ikonica=='WM1M': return 'sončno, vetrovno'
    elif ikonica=='WM2': return 'sončno'
    elif ikonica=='WM2M': return 'sončno, vetrovno'
    elif ikonica=='WM3': return 'pretežno jasno'
    elif ikonica=='WM3M': return 'pretežno jasno, vetrovno'
    elif ikonica=='WM4': return 'delno jasno'
    elif ikonica=='WM4M': return 'delno jasno, vetrovno'    
    elif ikonica=='WM5': return 'oblačno'
    elif ikonica=='WM5M': return 'oblačno, vetrovno'
    elif ikonica=='WM6': return 'pretežno oblačno'
    elif ikonica=='WM6M': return 'pretežno oblačno, vetrovno'
    elif ikonica=='WM7': return 'pretežno oblačno'
    elif ikonica=='WM7M': return 'pretežno oblačno, vetrovno'
    elif ikonica=='WM8': return 'oblačno'
    elif ikonica=='WM8M': return 'oblačno, vetrovno'
    elif ikonica=='WM9': return 'pretežno oblačno'
    elif ikonica=='WM9M': return 'pretežno oblačno, vetrovno'
    elif ikonica=='P1': return 'sneži'
    elif ikonica=='P1M': return 'oblačno, sneži, vetrovno'
    elif ikonica=='P2': return 'oblačno, rahlo sneži'
    elif ikonica=='P2M': return 'oblačno, rahlo sneži, vetrovno'
    elif ikonica=='P3' : return 'oblačno, rahlo sneži'
    elif ikonica=='P3M': return 'oblačno, rahlo sneži, vetrovno'
    elif ikonica=='P4': return 'oblačno, močno sneži'
    elif ikonica=='P4M': return 'oblačno, močno sneži, vetrovno'
    elif ikonica=='P5': return 'pretežno oblačno, dežuje'
    elif ikonica=='P5M': return 'pretežno oblačno, vetrovno, dežuje'
    elif ikonica=='P6': return 'oblačno, zg. sneg - sp. dež'
    elif ikonica=='P6M': return 'oblačno, zg. sneg - sp. dež'
    elif ikonica=='P7': return 'sneži'
    elif ikonica=='P7M': return 'sneži, vetrovno'
    elif ikonica=='P8': return 'sneži, smog'
    elif ikonica=='P8M': return 'sneži, smog, vetrovno'
    elif ikonica=='P9': return 'toča'
    elif ikonica=='P9M': return 'toča, vetrovno'
    elif ikonica=='P10': return 'pretežno oblačno'
    elif ikonica=='P10M': return 'pretežno oblačno, vetrovno'
    elif ikonica=='P11': return 'visoka oblačnost, zg. sneg - sp. dež'
    elif ikonica=='P11M': return 'visoka oblačnost, zg. sneg - sp. dež, vetrovno'
    else: return ikonica

def ime_smucisca(name):
    if name=='MariborskoPoh.':
        return 'MariborskoPohorje'
    elif name=='RTCKranjskaG.':
        return 'RTCKranjskaGora'
    else:
        return name

def odstrani_piko(string):
    vse=''
    for i in string:
        if i!='.':
            vse +=i
    pred_piko=int(vse[:-2])
    za_piko=int(vse[-2:])/60
    return pred_piko + za_piko

def nova_funkcija(mnozica):
    seznam=[]
    for x,y in mnozica:
        x=odstrani_piko(x)
        y=odstrani_piko(y)
        seznam.append(y-x)
    return sum(seznam)

def funkcija_za_proge(ikona):
    if ikona=='0':
        return 'gondola'
    elif ikona=='1':
        return 'sedeznica'
    elif ikona=='2':
        return 'vlečnica'
    elif ikona=='3':
        return 'park'
    else: return ikona

def koliko_prog(mnozice):
    slovarcek=dict()
    for x,y,z in mnozice:
        k=y + '/' + z
        slovarcek[x]=k
    return slovarcek

def solata(mnozica):
    koliko=0
    od=0
    for x,y,z in mnozica:
        koliko+=int(y)
        od+=int(z)
    if od==0:
        return 0
    else:
        procent=decimal.Decimal(koliko/od)*100
        return round(procent,2)
