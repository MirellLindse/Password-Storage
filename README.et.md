# 🔐 Paroolide Haldamise ja Loomise Rakendus (PSAGA)

Väike lauaarvuti rakendus paroolide turvaliseks salvestamiseks. Rakendatud Pythonis, PySide6 ja SQLite abil. Kõik paroolid krüpteeritakse enne salvestamist ja neid saab mugavalt kopeerida lõikelauale ühe nupuvajutusega.

## 🧠 Projekti Eesmärk

Eesmärk on luua lihtne, kuid funktsionaalne paroolihaldur, mis:

- Salvestab paroolid turvaliselt kasutades sümmeetrilist krüpteerimist
- Lubab kopeerida paroole ühe nupuvajutusega
- Kustutab kirjed nii liidest kui ka andmebaasist
- Sisaldab lehe täpsustust ja lihtsat disaini
- Ei vaja internetiühendust — kõik töötab lokaalselt

## 💡 Funktsioonid

- 🧷 Salvestab `veebilehe / emaili / parooli` paari
- 🔒 Krüpteerib ja dekrüpteerib paroole jooksvalt
- 👁 Näitab ainult tärne — turvalisus on esikohal
- 📋 "Koopia" nupp iga kirje kõrval kiireks parooli kopeerimiseks
- 🗑 Kustutab kirjed täielikult andmebaasist
- 📄 Lehe täpsustus, et lihtsustada navigeerimist suure hulga kirjade vahel

## 🧰 Tehnoloogiad

- Python 3.x
- PySide6 (Qt GUI jaoks)
- SQLite3 (sisseehitatud andmebaas)
- Fernet (krüpteerimiseks cryptography raamatukogust)

## 🖼 Ekraanipildid

(In progress)

## 🚀 Projekti Seadistamine

1. Kloneeri hoidla:

```bash
git clone https://github.com/MirellLindse/Password-Storage.git
cd Diploma
