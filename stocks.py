"""
Simple Enum class as a module as its used by multiple Lambdas
"""
from enum import Enum, auto

class Stock(Enum):
    """
    Simple Enum class
    """
    LIMITED = auto()
    YES = auto()
    NO = auto()
