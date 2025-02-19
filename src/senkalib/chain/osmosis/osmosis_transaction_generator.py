from dataclasses import dataclass
from dateutil import parser
from operator import attrgetter
from math import inf
from senkalib.chain.transaction_generator import TransactionGenerator
from senkalib.senka_setting import SenkaSetting
from senkalib.chain.osmosis.osmosis_transaction import OsmosisTransaction
from typing import List
import requests

class OsmosisTransactionGenerator(TransactionGenerator):
  chain = 'osmosis'

  @classmethod
  def get_transactions(cls, settings:SenkaSetting, address:str, startblock:int = None, endblock:int = None, starttime:int = None, endtime:int = None) -> List[OsmosisTransaction]:
    startblock = startblock if startblock is not None else 0
    endblock = endblock if endblock is not None else inf
    starttime = starttime if starttime is not None else 0
    endtime = endtime if endtime is not None else inf

    total_result = []
    id_cursor = get_nearest_id(endtime)

    while True:
      result = cls.get_txs(address, id_cursor)
      for tx in result:
        id_cursor = int(tx['header']['id'])
        block_id = int(tx['data']['height'])
        time = to_timestamp(tx['header']['timestamp'])

        if starttime <= time <= endtime and startblock <= block_id <= endblock:
          total_result.append(OsmosisTransaction(tx))

        if time < starttime or block_id < startblock:
          return total_result
        else:
          continue

      if len(result) < 50:
        return total_result

  @classmethod
  def get_txs(cls, address: str, id_from: int) -> List[dict]:
    params = {'from': id_from, 'limit': 50}
    headers = {'Origin': 'https://www.mintscan.io', 'Referer': 'https://www.mintscan.io/'}  # workaround from 2022-04-25: both origin and referer headers are required

    return requests.get('https://api-osmosis.cosmostation.io/v1/account/new_txs/%s' % address, params=params, headers=headers).json()


@dataclass
class CosmostationOsmosisTxHistoryRecord:
  id: int
  timestamp: int

records: List[CosmostationOsmosisTxHistoryRecord] = sorted([
  CosmostationOsmosisTxHistoryRecord(2, 1624052574),         # 2021-06-18T21:42:54Z
  CosmostationOsmosisTxHistoryRecord(455035, 1625097604),    # 2021-07-01T00:00:04Z
  CosmostationOsmosisTxHistoryRecord(1207598, 1627776001),   # 2021-08-01T00:00:01Z
  CosmostationOsmosisTxHistoryRecord(2284219, 1630454401),   # 2021-09-01T00:00:01Z
  CosmostationOsmosisTxHistoryRecord(3815804, 1633046402),   # 2021-10-01T00:00:02Z
  CosmostationOsmosisTxHistoryRecord(5802050, 1635724801),   # 2021-11-01T00:00:01Z
  CosmostationOsmosisTxHistoryRecord(8282434, 1638316803),   # 2021-12-01T00:00:03Z
  CosmostationOsmosisTxHistoryRecord(11802509, 1640995203),  # 2022-01-01T00:00:03Z
  CosmostationOsmosisTxHistoryRecord(11843943, 1641027605),  # 2022-01-01T09:00:05Z
], key=attrgetter('id'))

def get_nearest_id(time: int):
  return next(map(attrgetter('id'), filter(lambda x: time < x.timestamp, records)), 0)

def to_timestamp(iso8601string: str) -> int:
  return int(parser.parse(iso8601string).timestamp())
