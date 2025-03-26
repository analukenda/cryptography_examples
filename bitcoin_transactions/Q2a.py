from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


######################################################################
# TODO: Implementirajte `scriptPubKey` za zadatak 2
Q2a_txout_scriptPubKey = [
    OP_2DUP, 
	OP_NEGATE, OP_ADD, 0x24, OP_NUMEQUAL, 
	OP_IF,
	OP_NEGATE, OP_SUB, 0x16AA, OP_NUMEQUAL,
	OP_ELSE, 0, 
	OP_ENDIF

]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: postavite parametre transakcije
    # amount_to_send = {cjelokupni iznos BTC-a u UTXO-u kojeg saljemo} - {fee}
    amount_to_send = 0.00303907 - 0.00001
    txid_to_spend = (
        '7779b03e843ff467746c2694416c862fb460052bd86fb4273bc3dba79cc8cebb')
    # indeks UTXO-a unutar transakcije na koju se referiramo
    # (indeksi pocinju od nula)
    utxo_index = 2
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q2a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
