import json
import re
f = open("./items.txt", encoding="utf-8", errors="ignore");

# Categorie 1
baiatCounter = 0
fataCounter = 0
unisexCounter = 0

# Categorie 2
se3 = 0
b3se5 = 0
b5se8 = 0
b8se12 = 0
b12 = 0

# Categorie 3
se25pret = 0
b25se50pret = 0
b50se100pret = 0
b100se250pret = 0
b250pret = 0

# Categorie 4
se10marime = 0
b10se30marime = 0
b30se70marime = 0
b70se100marime = 0
b100se145marime = 0
b145marime = 0

# Categorie 5
toamnaCount = 0
iarnaCount = 0
primavaraCount = 0
varaCount = 0

# Categorie 6
germaniaCount = 0
frantaCount = 0
spaniaCount = 0
angliaCount = 0
cehiaCount = 0
americaCount = 0
ungariaCount = 0

# Categorie 7
se20Papuci = 0
b20se25Papuci = 0
b25se30Papuci = 0
b30se35Papuci = 0
b35Papuci = 0

# Categorie 8
zaraCount = 0
hmCount = 0
gapCount = 0
adidasCount = 0
nikeCount = 0
pumaCount = 0
newBalanceCount = 0
calvinKleinCount = 0
markSpencerCount = 0

# Categorie 9
postaCount = 0
fanCourierCount = 0
cargusCount = 0
personalCount = 0

# Categorie 10
bucurestiCount = 0
clujCount = 0
iasiCount = 0
timisoaraCount = 0
brasovCount = 0
targuMuresCount = 0
constantaCount = 0
ploiestiCount = 0
otherPlaceCount = 0

for line in f:
  # Categorie 1
  # Baiat
  item = re.search(r"(?:b[aă]i?[ae][tț](?:e[li])?i*)", line, re.I | re.M)
  if item:
    baiatCounter += 1

  # Fata
  item = re.search(r"(?:f(?:(?:at[aă])|(?:e[tț]i[tț][aăe])))", line, re.I | re.M)
  if item:
    fataCounter += 1

  # Unisex
  item = re.search(r"uni\s*sex", line, re.I | re.M)
  if item:
    unisexCounter += 1

  # Categorie 2
  # Ani / Varsta
  item = re.search(r"(\d{1,2})\s*(?=ani?)", line, re.I | re.M) or re.search(r"v[îâa]rst[ăae].*?(\d{1,2})", line, re.I | re.M)
  if item:
    age = int(item.groups()[0])
    if age <= 3:
      se3 += 1
    elif 3 < age <= 5:
      b3se5 += 1
    elif 5 < age <= 8:
      b5se8 += 1
    elif 8 < age <= 12:
      b8se12 += 1
    else:
      b12 += 1

  # Categorie 3
  # Pret
  item = re.search(r"(\d{1,4}).\D*?(?<=(?:\blei\b|\bron\b))", line, re.I | re.M)
  if item:
    price = int(item.groups()[0])
    if price <= 25:
      se25pret += 1
    elif 25 < price <= 50:
      b25se50pret += 1
    elif 50 < price <= 100:
      b50se100pret += 1
    elif 100 < price <= 250:
      b100se250pret += 1
    else:
      b250pret += 1

  # Categorie 4
  # Marime
  item = re.search(r"m[aă]rim[ei].*?(\d+)", line, re.I | re.M)
  if item:
    measure = int(item.groups()[0])
    if measure:
      if measure <= 10:
        se10marime += 1
      elif 10 < measure <= 30:
        b10se30marime += 1
      elif 30 < measure <= 70:
        b30se70marime += 1
      elif 70 < measure <= 100:
        b70se100marime += 1
      elif 100 < measure <= 145:
        b100se145marime += 1
      else:
        b145marime += 1

  # Categorie 5
  # Anotimp haine
  item = re.search(r"(toamn[aă])|(\bvar[aă]\b)|(prim[aă]var[aă])|(iarn[aă])", line, re.I | re.M)
  if item:
    itemGroups = item.groups()
    if itemGroups[0]:
      toamnaCount += 1
    if itemGroups[1]:
      varaCount += 1
    if itemGroups[2]:
      primavaraCount += 1
    if itemGroups[3]:
      iarnaCount += 1

  # Categorie 6
  # Tara origine
  item = re.search(r"(germania)|(fran[tț]a)|(spania)|(anglia)|(cehia)|(america)|(ungaria)", line, re.I | re.M)
  if item:
    itemGroups = item.groups()
    if itemGroups[0]:
      germaniaCount += 1
    if itemGroups[1]:
      frantaCount += 1
    if itemGroups[2]:
      spaniaCount += 1
    if itemGroups[3]:
      angliaCount += 1
    if itemGroups[4]:
      cehiaCount += 1
    if itemGroups[5]:
      americaCount += 1
    if itemGroups[6]:
      ungariaCount += 1

  # Categorie 7
  # Marime papuci/ghete
  item = re.search(r"(papuc(?:i|ei))|(ghea?t[ăeau](?:[tț]e)?)|(s[ăa]nd[ăa]l(?:e|u[tț]e))|(?:pantof(?:e|i*)|(?:adida[sș]i?)|(?:ten[ie][sș]i?)|(?:cizm[ăae])).*?(\d{2})", line, re.I | re.M)
  if item and item.groups()[3]:
    item = int(item.groups()[3])
    if item <= 20:
      se20Papuci += 1
    elif item > 20 and item <= 25:
      b20se25Papuci += 1
    elif item > 25 and item <= 30:
      b25se30Papuci += 1
    elif item > 30 and item <= 35:
      b30se35Papuci += 1
    else:
      b35Papuci += 1

  # Categorie 8
  # Firma haine
  item = re.search(r"(\bzara\b)|(h&amp;m)|(\bgap\b)|(\badidas\b)|(nike)|(\bpuma\b)|(new balance)|((?:\bck\b)|(?:calvin\s?klein))|(mark&amp;spencer)", line, re.I | re.M)
  if item:
    itemGroups = item.groups()
    if itemGroups[0]:
      zaraCount += 1
    if itemGroups[1]:
      hmCount += 1
    if itemGroups[2]:
      gapCount += 1
    if itemGroups[3]:
      adidasCount += 1
    if itemGroups[4]:
      nikeCount += 1
    if itemGroups[5]:
      pumaCount += 1
    if itemGroups[6]:
      newBalanceCount += 1
    if itemGroups[7]:
      calvinKleinCount += 1
    if itemGroups[8]:
      markSpencerCount += 1

  # Categorie 9
  # Modalitate livrare
  item = re.search(r"(po[sș]t[ăa])|(fan\s*co?urier)|(cargus)|(personal[ăa])", line, re.I | re.M)
  if item:
    itemGroups = item.groups()
    if itemGroups[0]:
      postaCount += 1
    if itemGroups[1]:
      fanCourierCount += 1
    if itemGroups[2]:
      cargusCount += 1
    if itemGroups[3]:
      personalCount += 1

  # Categorie 10
  # Oras transport
  item = re.search(r"((?:transport)|(?:predarea?)).*?(?:(bucure[șs]ti+)|(cluj)|(ia[șs]i+)|(timi[șs]oara)|(bra[sș]ov)|(t[âîa]rgu.*?mure[șs])|(constan[țt]a)|(ploie[șs]ti+))", line, re.I | re.M)
  if item:
    foundPlace = False
    itemGroups = item.groups()
    itemGroupsLen = len(itemGroups)
    for i in range(1, itemGroupsLen):
      if itemGroups[i]:
        if i == 1:
          bucurestiCount += 1
        elif i == 2:
          clujCount += 1
        elif i == 3:
          iasiCount += 1
        elif i == 4:
          timisoaraCount += 1
        elif i == 5:
          brasovCount += 1
        elif i == 6:
          targuMuresCount += 1
        elif i == 7:
          constantaCount += 1
        elif i == 8:
          ploiestiCount += 1
        foundPlace = True
    if not foundPlace:
      otherPlaceCount += 1

# The object containing all information
# It will be based as JSON to the frontend
objects = [{"name": "sex", "counters": {"baiat": baiatCounter, "fata": fataCounter, "unisex": unisexCounter}},
{"name": "varsta", "counters": {"varsta <= 3": se3, "3 < varsta <= 5": b3se5, "5 < varsta <= 8": b5se8, "8 < varsta <= 12": b8se12, "12 < varsta": b12}},
{"name": "pret", "counters": {"pret <= 25": se25pret, "25 < pret <= 50": b25se50pret, "50 < pret <= 100": b50se100pret, "100 < pret <= 250": b100se250pret, "250 < pret": b250pret}},
{"name": "marime haine", "counters": {"marime <= 10": se10marime, "10 < marime <= 30": b10se30marime, "30 < marime <= 70": b30se70marime, "70 < marime <= 100": b70se100marime, "100 < marime <= 145": b100se145marime, "145 < marime": b145marime}},
{"name": "anotimp haine", "counters": {"iarna": iarnaCount, "primavara": primavaraCount, "vara": varaCount, "toamna": toamnaCount}},
{"name": "tara origine", "counters": {"franta": frantaCount, "spania": spaniaCount, "anglia": angliaCount, "cehia": cehiaCount, "america": americaCount, "ungaria": ungariaCount}},
{"name": "marime papuci", "counters": {"marime papuci <= 20": se20Papuci, "20 < marime papuci <= 25": b20se25Papuci, "25 < marime papuci <= 30": b25se30Papuci, "30 < marime papuci <= 35": b30se35Papuci, "35 < marime papuci": b35Papuci}},
{"name": "firma haine", "counters": {"zara": zaraCount, "h&m": hmCount, "gap": gapCount, "adidas": adidasCount, "nike": nikeCount, "puma": pumaCount, "new balance": newBalanceCount, "calvin klein": calvinKleinCount, "mark & spencer": markSpencerCount}},
{"name": "modalitate livrare", "counters": {"posta": postaCount, "fan courier": fanCourierCount, "cargus ": cargusCount, "personal": personalCount}},
{"name": "oras transport", "counters": {"bucuresti": bucurestiCount, "cluj": clujCount, "iasi": iasiCount, "timisoara": timisoaraCount, "brasov": brasovCount, "targu-mures": targuMuresCount, "constanta": constantaCount, "ploiesti": ploiestiCount, "other": otherPlaceCount}}
]

print(json.dumps(objects))