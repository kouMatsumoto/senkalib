from abc import ABCMeta, abstractmethod
from senkalib.caaj_journal import CaajJournal
from senkalib.chain.transaction import Transaction
from senkalib.token_original_id_table import TokenOriginalIdTable
from typing import List

class CaajPlugin(metaclass=ABCMeta):
  chain = None

  @abstractmethod
  def can_handle(cls, transaction:Transaction) -> bool:
    pass

  @abstractmethod
  def get_caajs(cls, address:str, transaction:Transaction, token_original_id_table:TokenOriginalIdTable) -> List[CaajJournal]:
    pass