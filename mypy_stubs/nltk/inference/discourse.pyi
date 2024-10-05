from abc import ABCMeta, abstractmethod

from _typeshed import Incomplete

from nltk.data import show_cfg as show_cfg
from nltk.inference.mace import MaceCommand as MaceCommand
from nltk.inference.prover9 import Prover9Command as Prover9Command
from nltk.parse import load_parser as load_parser
from nltk.parse.malt import MaltParser as MaltParser
from nltk.sem.drt import (
    AnaphoraResolutionException as AnaphoraResolutionException,
)
from nltk.sem.drt import resolve_anaphora as resolve_anaphora
from nltk.sem.glue import DrtGlue as DrtGlue
from nltk.sem.logic import Expression as Expression
from nltk.tag import RegexpTagger as RegexpTagger

class ReadingCommand(metaclass=ABCMeta):
    @abstractmethod
    def parse_to_readings(self, sentence: Incomplete) -> Incomplete: ...
    def process_thread(self, sentence_readings: Incomplete) -> Incomplete: ...
    @abstractmethod
    def combine_readings(self, readings: Incomplete) -> Incomplete: ...
    @abstractmethod
    def to_fol(self, expression: Incomplete) -> Incomplete: ...

class CfgReadingCommand(ReadingCommand):
    def __init__(self, gramfile: Incomplete | None = None) -> None: ...
    def parse_to_readings(self, sentence: Incomplete) -> Incomplete: ...
    def combine_readings(self, readings: Incomplete) -> Incomplete: ...
    def to_fol(self, expression: Incomplete) -> Incomplete: ...

class DrtGlueReadingCommand(ReadingCommand):
    def __init__(
        self,
        semtype_file: Incomplete | None = None,
        remove_duplicates: bool = False,
        depparser: Incomplete | None = None,
    ) -> None: ...
    def parse_to_readings(self, sentence: Incomplete) -> Incomplete: ...
    def process_thread(self, sentence_readings: Incomplete) -> Incomplete: ...
    def combine_readings(self, readings: Incomplete) -> Incomplete: ...
    def to_fol(self, expression: Incomplete) -> Incomplete: ...

class DiscourseTester:
    def __init__(
        self,
        input: Incomplete,
        reading_command: Incomplete | None = None,
        background: Incomplete | None = None,
    ) -> None: ...
    def sentences(self) -> None: ...
    def add_sentence(
        self,
        sentence: Incomplete,
        informchk: bool = False,
        consistchk: bool = False,
    ) -> None: ...
    def retract_sentence(
        self, sentence: Incomplete, verbose: bool = True
    ) -> None: ...
    def grammar(self) -> None: ...
    def readings(
        self,
        sentence: Incomplete | None = None,
        threaded: bool = False,
        verbose: bool = True,
        filter: bool = False,
        show_thread_readings: bool = False,
    ) -> None: ...
    def expand_threads(
        self, thread_id: Incomplete, threads: Incomplete | None = None
    ) -> Incomplete: ...
    def models(
        self,
        thread_id: Incomplete | None = None,
        show: bool = True,
        verbose: bool = False,
    ) -> None: ...
    def add_background(
        self, background: Incomplete, verbose: bool = False
    ) -> None: ...
    def background(self) -> None: ...
    @staticmethod
    def multiply(
        discourse: Incomplete, readings: Incomplete
    ) -> Incomplete: ...

def load_fol(s: Incomplete) -> Incomplete: ...
def discourse_demo(reading_command: Incomplete | None = None) -> None: ...
def drt_discourse_demo(reading_command: Incomplete | None = None) -> None: ...
def spacer(num: int = 30) -> None: ...
def demo() -> None: ...