from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import P2PKH_scriptPubKey
from Q2a import Q2a_txout_scriptPubKey


######################################################################
# TODO: postavite parametre transakcije
# amount_to_send = {cjelokupni iznos BTC-a u UTXO-u kojeg saljemo} - {fee}
amount_to_send = 0.00302907 - 0.00001
txid_to_spend = (
        'dbb0a4d1fff28589e1bb6045e7408ca39bf6344e0f937f52040ad427524801b7')
# indeks UTXO-a unutar transakcije na koju se referiramo
# (indeksi pocinju od nula)
utxo_index = 0
######################################################################

txin_scriptPubKey = Q2a_txout_scriptPubKey
######################################################################
# TODO: implementirajte skriptu `scriptSig` kojom cete otkljucati BTC zakljucan
# pomocu skripte `scriptPubKey` u zadatku 2a
txin_scriptSig = [
    0xB67, 0xB43
]
######################################################################
txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)

response = send_from_custom_transaction(
    amount_to_send, txid_to_spend, utxo_index,
    txin_scriptPubKey, txin_scriptSig, txout_scriptPubKey, network_type)
print(response.status_code, response.reason)
print(response.text)
