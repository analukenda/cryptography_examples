# Simulation of admin activities
# Adding new user with arguments: add *user*
# Changing password of existing user with arguments: passwd *user*
# Forcing user to change password on next login with arguments: forcepass *user*
# Deleting user with arguments: del *user*

from os.path import exists
from json import dumps, loads
from sys import argv
from getpass import getpass
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA512
from Cryptodome.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode

ime_baze = 'baza.bin'
min_duljina = 8

if not exists(ime_baze):
    baza = open(ime_baze, 'wb')
    lozinke = {}
    baza.write(dumps(lozinke).encode(encoding='UTF-8'))
    baza.close()

akcija = argv[1].strip()
korisnik = argv[2].strip()
baza = open(ime_baze, 'rb')
lozinke = loads(baza.read().decode(encoding='UTF-8'))
baza.close()


def stvaranje_lozinke(objekt, akcija):
    print('Lozinka mora imati bar 8 znakova i mora sadržavati bar jedan broj, malo slovo i veliko slovo.')
    while (True):
        lozinka = getpass('Lozinka:').strip()
        podatci = lozinke.get(korisnik)
        if podatci is not None:
            stari_salt = b64decode(podatci[0].encode(encoding='UTF-8'))
            stari_kljuc = b64decode(podatci[1].encode(encoding='UTF-8'))
            if stari_kljuc == PBKDF2(lozinka.encode(encoding='UTF-8'), stari_salt, 20, count=1000000,
                                     hmac_hash_module=SHA512):
                print('Nova lozinka ne smije biti jednaka prethodnoj!')
                continue
        if len(lozinka) < min_duljina:
            print('Lozinka mora imati bar 8 znakova!')
        else:
            broj = False
            malo_slovo = False
            veliko_slovo = False
            for znak in lozinka:
                if znak.isdigit():
                    broj = True
                elif znak.islower():
                    malo_slovo = True
                elif znak.isupper():
                    veliko_slovo = True
                if broj and malo_slovo and veliko_slovo:
                    if lozinka == getpass('Ponovite lozinku:').strip():
                        salt = get_random_bytes(32)
                        kljuc = PBKDF2(lozinka.encode(encoding='UTF-8'), salt, 20, count=1000000,
                                       hmac_hash_module=SHA512)
                        lozinke[korisnik] = (b64encode(salt).decode(encoding='UTF-8'),
                                             b64encode(kljuc).decode(encoding='UTF-8'), 0, 0)
                        baza = open(ime_baze, 'wb')
                        baza.write(dumps(lozinke).encode(encoding='UTF-8'))
                        baza.close()
                        print('--------------------------------------------------------')
                        print(objekt + ' uspjesno ' + akcija + '.')
                        exit(0)
                    else:
                        print(objekt + ' nije ' + akcija + '. Upisane lozinke nisu iste.')
                        exit(1)
            print('Lozinka mora sadrzavati bar jedan broj, malo slovo i veliko slovo.')

if akcija == 'add':
    if korisnik not in lozinke.keys():
        stvaranje_lozinke('Korisnik', 'dodan')
    else:
        print('Zadani korisnik vec ima lozinku! Za mijenjanje lozinke koristite akciju passwd.')

elif akcija == 'passwd':
    if korisnik in lozinke.keys():
        stvaranje_lozinke('Lozinka', 'promijenjena')
    else:
        print('Zadani korisnik ne postoji!')

elif akcija == 'forcepass':
    podatci = lozinke.get(korisnik)
    if podatci is not None:
        lozinke[korisnik] = (podatci[0], podatci[1], 1, 0)
        baza = open(ime_baze, 'wb')
        baza.write(dumps(lozinke).encode(encoding='UTF-8'))
        baza.close()
        print('Od korisnika ce se traziti da promijeni lozinku pri sljedecem loginu.')
    else:
        print('Zadani korisnik ne postoji!')

elif akcija == 'del':
    try:
        del lozinke[korisnik]
        baza = open(ime_baze, 'wb')
        baza.write(dumps(lozinke).encode(encoding='UTF-8'))
        baza.close()
        print('Korisnik uspjesno obrisan.')
    except KeyError:
        print('Zadani korisnik ne postoji!')

else:
    print('Zadali ste akciju koja ne postoji! Mogucnosti su add, passwd, forcepass i del.')
