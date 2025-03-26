from bitcoin import SelectParams
from bitcoin.base58 import decode
from bitcoin.core import x
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress


SelectParams('testnet')

faucet_address = CBitcoinAddress('mohjSavDdQYHRYXcS3uS6ttaHP8amyvX78')

# Koristimo testnet 'btc-test3'
network_type = 'btc-test3'

######################################################################
# TODO: Nadopunite skriptu sa svojim privatnim kljucem
#
# Generirajte privatni kljuc i pripadnu adresu u formatu Base58
# pomocu skripte `keygen.py`
# Dohvatite novcice s adrese `https://testnet-faucet.com/btc-testnet/`

my_private_key = CBitcoinSecret(
    'cVDRSLcwDAnqgHhiDZvFX6DdH66gGtn4fbjNkuBnhLRisxJLV8Dp')

my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)
######################################################################
