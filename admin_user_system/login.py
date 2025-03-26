# Simulation of user activity
# Command for login: python login.py *user*

from os.path import exists
from sys import argv
from json import dumps, loads
from getpass import getpass
from base64 import b64encode, b64decode
from Cryptodome.Hash import SHA512
from Cryptodome.Protocol.KDF import PBKDF2
from time import sleep
from Cryptodome.Random import get_random_bytes

ime_baze = 'baza.bin'
min_duljina = 8
cekanje = 3
max_pokusaj = 5

if not exists(ime_baze):
    baza = open(ime_baze, 'wb')
    lozinke = {}
    baza.write(dumps(lozinke).encode(encoding='UTF-8'))
    baza.close()

korisnik = argv[1].strip()
baza = open(ime_baze, 'rb')
lozinke = loads(baza.read().decode(encoding='UTF-8'))
baza.close()
podatci = lozinke.get(korisnik)
pokusaj = 0

if podatci is not None:
    if podatci[3] == 1:
        print('Blokirani ste zbog previse neuspjelih prijava.\nObratite se administratoru.')
    else:
        salt = b64decode(podatci[0].encode(encoding='UTF-8'))
        kljuc = b64decode(podatci[1].encode(encoding='UTF-8'))
        while pokusaj < max_pokusaj:
            lozinka = getpass('Lozinka:').strip()
            if kljuc == PBKDF2(lozinka.encode(encoding='UTF-8'), salt, 20, count=1000000, hmac_hash_module=SHA512):
                if podatci[2] == 1:
                    print('Promijenite lozinku! Nova lozinka mora imati bar 8 znakova\n'
                        'i mora sadržavati bar jedan broj, malo slovo i veliko slovo.')
                    promjena = False
                    while (not promjena):
                        nova_loz = getpass('Nova lozinka:')
                        if kljuc == PBKDF2(nova_loz.encode(encoding='UTF-8'), salt, 20, count=1000000,
                                           hmac_hash_module=SHA512):
                            print('Nova lozinka ne smije biti jednaka prethodnoj!')
                        elif len(nova_loz) < min_duljina:
                            print('Lozinka mora imati bar 8 znakova!')
                        else:
                            broj = False
                            malo_slovo = False
                            veliko_slovo = False
                            for znak in nova_loz:
                                if znak.isdigit():
                                    broj = True
                                elif znak.islower():
                                    malo_slovo = True
                                elif znak.isupper():
                                    veliko_slovo = True
                                if broj and malo_slovo and veliko_slovo:
                                    if nova_loz == getpass('Ponovite lozinku:').strip():
                                        novi_salt = get_random_bytes(32)
                                        novi_kljuc = PBKDF2(nova_loz.encode(encoding='UTF-8'), novi_salt, 20,
                                                            count=1000000, hmac_hash_module=SHA512)
                                        lozinke[korisnik] = (b64encode(novi_salt).decode(encoding='UTF-8'),
                                                             b64encode(novi_kljuc).decode(encoding='UTF-8'), 0, 0)
                                        baza = open(ime_baze, 'wb')
                                        baza.write(dumps(lozinke).encode(encoding='UTF-8'))
                                        baza.close()
                                        promjena = True
                                        pokusaj = max_pokusaj
                                        print('Uspjesna prijava.')
                                    else:
                                        print('Upisane lozinke nisu iste. Pokusajte ponovno.')
                                    break
                            if not (broj and malo_slovo and veliko_slovo):
                                print('Lozinka mora sadrzavati bar jedan broj, malo slovo i veliko slovo.')
                else:
                    pokusaj = max_pokusaj
                    print('Uspjesna prijava.')
            else:
                print('Krivo korisnicko ime ili lozinka.')
                if pokusaj < (max_pokusaj - 1):
                    sleep(pokusaj * cekanje)
                else:
                    lozinke[korisnik] = (podatci[0], podatci[1], podatci[2], 1)
                    baza = open(ime_baze, 'wb')
                    baza.write(dumps(lozinke).encode(encoding='UTF-8'))
                    baza.close()
                    print('--------------------------------------------------------')
                    print('Upisali ste krive podatke ' + str(max_pokusaj) +
                          ' puta.\nSustav ce vas blokirati. Obratite se administratoru.')
                pokusaj += 1
else:
    while pokusaj < max_pokusaj:
        getpass('Lozinka:')
        print('Krivo korisnicko ime ili lozinka.')
        if pokusaj < max_pokusaj - 1:
            sleep(pokusaj * cekanje)
        else:
            print('--------------------------------------------------------')
            print('Upisali ste krive podatke ' + str(max_pokusaj) +
                  ' puta.\nSustav ce vas blokirati. Obratite se administratoru.')
        pokusaj += 1
