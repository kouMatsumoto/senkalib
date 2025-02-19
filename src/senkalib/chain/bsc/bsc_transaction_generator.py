from senkalib.chain.bsc.bsc_transaction import BscTransaction
from senkalib.chain.transaction import Transaction 
from senkalib.chain.transaction_generator import TransactionGenerator
from senkalib.senka_setting import SenkaSetting
from web3 import Web3
from bscscan import BscScan
from typing import List
import asyncio

class BscTransactionGenerator(TransactionGenerator):
  chain = 'bsc'

  @classmethod
  def get_transactions(cls, settings:SenkaSetting, address:str, startblock:int = None, endblock:int = None, starttime:int = None, endtime:int = None) -> List[Transaction]:
    settings = settings.get_settings()
    startblock = startblock if startblock is not None else 0
    endblock = endblock if endblock is not None else None
    w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
    transactions = []
    
    page = 1
    while True:
      txs = asyncio.run(BscTransactionGenerator.get_txs(settings, address, startblock, endblock, page))
      for tx in txs:
        if '1' in tx['isError']:
          continue
        else:
          receipt = w3.eth.get_transaction_receipt(tx['hash'])
          transactions.append(BscTransaction(tx['hash'], receipt, tx['timeStamp'], tx['gasUsed'], tx['gasPrice']))

      page += 1
      if len(txs) < 10000: # bscscan api return 10000 results for each page
        break

    return transactions

  @classmethod
  async def get_txs(cls, settings:dict, address:str, arg_startblock:int = None, arg_endblock:int = None, arg_page:int = None):
    async with BscScan(settings['bscscan_key']) as bscscan:
      txs = await bscscan.get_normal_txs_by_address_paginated(address=address, startblock=arg_startblock, endblock=arg_endblock, 
        page=arg_page, offset=0, sort='asc')

    return txs
