import decimal
import os
import csv
import requests
import re
import sys
import definicije

##REGULARNI IZRAZ VZOREC
vzorec = re.compile(
  r"'><h1>(?P<smucisce>.*?)<.*?"
  r"telefon.si/Images/(?P<vreme>.*?).jpg.*?"
  r"\+?(?P<temperatura>-?\d+)°</p.*?"
  r"'>(?P<sneg>(\d+|-)).*?"
#  r"'desc-timetable-index\'>(?P<odpiralni_cas>\d+\.\d{2})(?P<zapiralni_cas>\d{2}\.\d{2}).",
  r"Obratovanjecentra(?P<obratovanje>.*?)p>.*?"
  r"Obratovanjenaprav(?P<sedeznice>.*?)class='col",
  flags=re.DOTALL
)

##POGLEJ, KAJ NAJDE REGULARNI IZRAZ VZOREC
def poglej_delovanje_ragularnega_izraza_vzorec_na_datoteki(datoteka):
    for ujemanje in re.finditer(vzorec, definicije.odpri(datoteka)):
        print(ujemanje.groupdict())


##FUNKCIJA UREDI_SMUČIŠČE
def uredi_smucisce(smucisce):
    podatki=smucisce.groupdict()

    regex_obratovanja=re.compile(
        r">(?P<odpiralni>\d+\.\d{2})\-?(?P<zapiralni>\d+\.\d{2})<"
    )
    
    podatki['obratovanje']={(smuka.group('odpiralni'),smuka.group('zapiralni')) for smuka in re.finditer(regex_obratovanja,podatki['obratovanje'])}

    regex_sedeznice=re.compile(
        "-(?P<ikona>\d+)'><divclass='popover-content-lifts-number'><b>(?P<je>\d+)</b>/(?P<od>\d+)<"
    )

    podatki['sedeznice']={(definicije.funkcija_za_proge(sed.group('ikona')),sed.group('je'),sed.group('od')) for sed in re.finditer(regex_sedeznice, podatki['sedeznice'])}

    podatki['vreme']=definicije.vreme_ikone(podatki['vreme'])

    podatki['smucisce']=definicije.ime_smucisca(podatki['smucisce'])
    
    return podatki['smucisce'], podatki



## IMENA SMUČIŠČ POSEBAJ
def najdi_vsa_smucisca(mapa):
    imena=set()
    for html_datoteka in definicije.datoteke(mapa):
        if html_datoteka[-5:] != '.html':
                continue
        for smucisce in re.finditer(vzorec,definicije.odpri(html_datoteka)):
                ime,slovar=uredi_smucisce(smucisce)
                imena.add(ime)
    return imena

## POGLEJ, KAJ NAREDI FUNKCIJA UREDI_SMUČIŠČE
def poglej_funkcijo_uredi_smucisce_na_mapi(mapa):
    for html_datoteka in definicije.datoteke(mapa):
        if html_datoteka[-4:] != 'html':
            continue
        else:
            for smucisce in re.finditer(vzorec, definicije.odpri(html_datoteka)):
                ime_smucisca, podatki = uredi_smucisce(smucisce)
                print(ime_smucisca, podatki)

    for smucisce in re.finditer(vzorec, definicije.odpri('eva.html')):
        ime_smucisca, podatki=uredi_smucisce(smucisce)
        print(ime_smucisca, podatki)

## SPREMENI DATOTEKE IZ .HTML V .CSV
for html_datoteka in definicije.datoteke('sneg/'):
    if html_datoteka[-4:] == '.csv':
        continue
    csv_datoteka=html_datoteka.replace('.html','.csv')
    cas=csv_datoteka[5:-4]
    imena_polj = ['smucisce','vreme','temperatura','sneg','obratovanje','odprto','sedeznice','cas','proge']
    with open(csv_datoteka, 'w', encoding='utf8') as csv_dat:
        writer = csv.DictWriter(csv_dat , imena_polj)
        writer.writeheader()
        drugi=csv.writer(csv_dat)
        drugi.writerow([cas])
        for ujemanje in re.finditer(vzorec,definicije.odpri(html_datoteka)):
            _,slovar=uredi_smucisce(ujemanje)
            slovar['cas']=cas
            slovar['odprto']=definicije.nova_funkcija(slovar['obratovanje'])
            slovar['proge']=definicije.solata(slovar['sedeznice'])
            slovar['sedeznice']=definicije.koliko_prog(slovar['sedeznice'])
            writer.writerow(slovar)

## SKUPNA DATOTEKA
definicije.pripravi_imenik('csv_datoteke/skupna.csv')
imena_polj=['smucisce','cas','vreme','temperatura','sneg','obratovanje','odprto','sedeznice','proge']
with open('csv_datoteke/skupna.csv', 'w', encoding='utf8') as dat:
    writer=csv.DictWriter(dat, imena_polj)
    writer.writeheader()
    for html_datoteka in definicije.datoteke('sneg/'):
        if html_datoteka[-5:] != '.html':
            continue
        cas=html_datoteka[5:-4]
        for smucisce in re.finditer(vzorec,definicije.odpri(html_datoteka)):
            _,slovar=uredi_smucisce(smucisce)
            slovar['cas']=cas
            slovar['odprto']=definicije.nova_funkcija(slovar['obratovanje'])
            slovar['proge']=definicije.solata(slovar['sedeznice'])
            slovar['sedeznice']=definicije.koliko_prog(slovar['sedeznice'])
            writer.writerow(slovar)

    
## DATOTEKE PO POSAMEZNIH SMUČIŠČIH
smucisca=najdi_vsa_smucisca('sneg/')
for smucisce in smucisca:
    if smucisce=='MariborskoPoh.':
        continue
    elif smucisce=='RTCKranjskaG.':
        continue
    else:
        ime='csv_datoteke/posamezna_smucisca/' + str(smucisce) + '.csv'
        definicije.pripravi_imenik(ime)

    polja=['smucisce','cas', 'vreme', 'temperatura', 'sneg', 'obratovanje','odprto', 'sedeznice','proge']
    with open(ime, 'w', encoding='utf8') as sm:
        writer=csv.DictWriter(sm, polja)
        drugi=csv.writer(sm)
        writer.writeheader()
        for dat in definicije.datoteke('sneg/'):
            if dat[-5:] != '.html':
                continue
            cas=dat[5:-4]
            for ujemanje in re.finditer(vzorec,definicije.odpri(dat)):
                ime,slovar=uredi_smucisce(ujemanje)
                slovar['cas']=cas
                slovar['odprto']=definicije.nova_funkcija(slovar['obratovanje'])
                slovar['proge']=definicije.solata(slovar['sedeznice'])
                slovar['sedeznice']=definicije.koliko_prog(slovar['sedeznice'])
                if ime=='MariborskoPoh.':
                    ime='MariborskoPohorje'
                elif ime=='RTCKranjskaG.':
                    ime='RTCKranjskaGora'
                if ime==smucisce:
                    writer.writerow(slovar)
                else:
                    continue
