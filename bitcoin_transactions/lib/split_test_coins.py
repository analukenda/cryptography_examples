from bitcoin import SelectParams
from bitcoin.core import CMutableTransaction, x
from bitcoin.core.script import CScript, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH

from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

from config import (my_private_key, my_public_key, my_address, faucet_address,
      network_type)

from utils import create_txin, create_txout, broadcast_transaction

def split_coins(amount_to_send, txid_to_spend, utxo_index, n, network):
    txin_scriptPubKey = address.to_scriptPubKey()
    txin = create_txin(txid_to_spend, utxo_index)
    # omoguci `replace-by-fee`:
    # `https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki`
    txin.nSequence = 0x1
    txout_scriptPubKey = address.to_scriptPubKey()
    txout = create_txout(amount_to_send / n, txout_scriptPubKey)
    tx = CMutableTransaction([txin], [txout]*n)
    sighash = SignatureHash(txin_scriptPubKey, tx,
                            0, SIGHASH_ALL)
    txin.scriptSig = CScript([private_key.sign(sighash) + bytes([SIGHASH_ALL]),
                              public_key])
    VerifyScript(txin.scriptSig, txin_scriptPubKey,
                 tx, 0, (SCRIPT_VERIFY_P2SH,))

    response = broadcast_transaction(tx, network)
    print(response.status_code, response.reason)
    print(response.text)

if __name__ == '__main__':
    SelectParams('testnet')

    ######################################################################
    # TODO: postavite sljedece parametre transakcije
    private_key = my_private_key
    public_key = private_key.pub
    address = P2PKHBitcoinAddress.from_pubkey(public_key)

    #  amount_to_send = {cjelokupni iznos BTC-a u UTXO-u kojeg dijelimo} - {fee}
    amount_to_send = 0.01823442-0.00001
    txid_to_spend = (
        'e6f2699027095938db72f9a03d315cd0bba71c0cc993f409f7f1801dda7f2e13')
    # indeks UTXO-a unutar transakcije na koju se referiramo
    # (indeksi pocinju od nula)
    utxo_index = 1
    # broj UTXO-a na koji zelimo podijeliti pocetni
    n = 6
    # U normalnim okolnostima (pod pretpostavkom da rijesite vjezbu bez gresaka)
    # dovoljno bi bilo staviti `n = 3`. No, zbog mogucih gresaka preporucamo da
    # stavite barem `n = 6`
    ######################################################################

    split_coins(amount_to_send, txid_to_spend, utxo_index, n, network_type)
