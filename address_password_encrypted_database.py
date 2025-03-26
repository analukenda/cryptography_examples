# Database of encrypted pairs of addresses and passwords
# Using AES-256 with 32 byte key
# First database needs to be initialized and master password set
# Command for that: python address_password_encrypted_database.py init *master_password*
# For adding new pair of address and password
# Command: python address_password_encrypted_database.py put *master_password* *address* *password*
# Getting password of the address:
# Command: python address_password_encrypted_database.py get *master_password* *address*
from sys import argv
from os.path import exists, getsize
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Cipher import AES
from json import dumps, loads

akcija = argv[1].strip()
glavna_lozinka = argv[2].strip().encode()
ime_baze = 'baza.bin'
scrypt_param = [32, 2 ** 20, 8, 1]
ostali_bajtovi = 32 + 16 + 16
salt_vel = 32
nonce_vel = 16
oznaka_vel = 16

if akcija == 'init':
    if not exists(ime_baze):
        baza = open(ime_baze, 'wb')
        salt = get_random_bytes(salt_vel)
        aes_kljuc = scrypt(glavna_lozinka, salt, scrypt_param[0], scrypt_param[1], scrypt_param[2],
                           scrypt_param[3])
        nonce = get_random_bytes(nonce_vel)
        aes = AES.new(aes_kljuc, AES.MODE_GCM, nonce=nonce)
        lozinke = {}
        sifrat, oznaka = aes.encrypt_and_digest(dumps(lozinke).encode())
        baza.write(salt + nonce + sifrat + oznaka)
        baza.close()
        print('Upravitelj lozinkama inicjaliziran!')
    else:
        print('Upravitelj lozinkama vec je inicjaliziran! Ne mozete mijenjati glavnu lozinku!')

elif akcija == 'put':
    if exists(ime_baze):
        baza = open(ime_baze, 'rb')
        salt = baza.read(salt_vel)
        aes_kljuc = scrypt(glavna_lozinka, salt, scrypt_param[0], scrypt_param[1], scrypt_param[2],
                           scrypt_param[3])
        nonce = baza.read(nonce_vel)
        aes = AES.new(aes_kljuc, AES.MODE_GCM, nonce=nonce)
        sifrat = baza.read(getsize(ime_baze) - ostali_bajtovi)
        oznaka = baza.read(oznaka_vel)
        baza.close()
        try:
            poruka = aes.decrypt_and_verify(sifrat, oznaka)
            lozinke = loads(poruka.decode())
            adresa = str(argv[3]).strip()
            lozinka = str(argv[4]).strip()
            lozinke[adresa] = lozinka
        except:
            print('Ili ste zadali krivu glavnu lozinku ili vam je netko mijenjao bazu lozinki!')
            exit(1)

        salt = get_random_bytes(salt_vel)
        aes_kljuc = scrypt(glavna_lozinka, salt, scrypt_param[0], scrypt_param[1], scrypt_param[2],
                           scrypt_param[3])
        nonce = get_random_bytes(16)
        aes = AES.new(aes_kljuc, AES.MODE_GCM, nonce=nonce)
        sifrat, oznaka = aes.encrypt_and_digest(dumps(lozinke).encode())
        baza = open(ime_baze, 'wb')
        baza.write(salt + nonce + sifrat + oznaka)
        baza.close()
        print('Postavljena lozinka za adresu ' + adresa + '.')
    else:
        print('Upravitelj zaporkama nije jos inicijaliziran! Prvo ga morate inicijalizirati!')

elif akcija == 'get':
    if exists(ime_baze):
        baza = open(ime_baze, 'rb')
        salt = baza.read(salt_vel)
        aes_key = scrypt(glavna_lozinka, salt, scrypt_param[0], scrypt_param[1], scrypt_param[2],
                         scrypt_param[3])
        nonce = baza.read(16)
        aes = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        sifrat = baza.read(getsize(ime_baze) - ostali_bajtovi)
        oznaka = baza.read(16)
        baza.close()
        try:
            poruka = aes.decrypt_and_verify(sifrat, oznaka)
            lozinke = loads(poruka.decode())
            adresa = str(argv[3]).strip()
            lozinka = lozinke.get(adresa)
            if lozinka is not None:
                print('Lozinka za adresu ' + adresa + ' je ' + lozinka + '.')
            else:
                print('Lozinka za adresu ' + adresa + ' nije jos postavljena.')
        except:
            print('Ili ste zadali krivu glavnu lozinku ili vam je netko mijenjao bazu lozinki!')
            exit(1)
    else:
        print('Upravitelj zaporkama nije jos inicijaliziran! Prvo ga morate inicijalizirati!')

else:
    print('Neispravno zadana naredba!')
