from collections import OrderedDict as OrderedDict
from operator import abs as _abs_
from operator import add as _add_
from operator import and_ as _and_
from operator import floordiv as _floordiv_
from operator import inv as _inv_
from operator import lshift as _lshift_
from operator import mod as _mod_
from operator import mul as _mul_
from operator import neg as _neg_
from operator import or_ as _or_
from operator import pos as _pos_
from operator import pow as _pow_
from operator import rshift as _rshift_
from operator import sub as _sub_
from operator import truediv as _truediv_
from operator import xor as _xor_

from _typeshed import Incomplete

from ._py3 import *

__all__ = [
    "pyver",
    "PY2",
    "PY2_6",
    "PY3",
    "PY3_3",
    "PY3_4",
    "PY3_5",
    "PY3_6",
    "PY3_7",
    "PY3_11",
    "_or_",
    "_and_",
    "_xor_",
    "_inv_",
    "_abs_",
    "_add_",
    "_floordiv_",
    "_lshift_",
    "_rshift_",
    "_mod_",
    "_mul_",
    "_neg_",
    "_pos_",
    "_pow_",
    "_truediv_",
    "_sub_",
    "unicode",
    "basestring",
    "baseinteger",
    "long",
    "NoneType",
    "_Addendum",
    "is_descriptor",
    "is_dunder",
    "is_sunder",
    "is_internal_class",
    "is_private_name",
    "get_attr_from_chain",
    "_value",
    "constant",
    "make_class_unpicklable",
    "bltin_property",
    "skip",
    "nonmember",
    "member",
    "Member",
    "NonMember",
    "OrderedDict",
]

pyver: tuple[int, int]
PY2: bool
PY3: bool
PY2_6: tuple[int, int]
PY3_3: tuple[int, int]
PY3_4: tuple[int, int]
PY3_5: tuple[int, int]
PY3_6: tuple[int, int]
PY3_7: tuple[int, int]
PY3_11: tuple[int, int]
bltin_property = property
unicode = unicode
unicode = str
basestring: Incomplete
baseinteger: Incomplete
long = long
long = int
baseint = baseinteger
NoneType: Incomplete

class _Addendum:
    dict: Incomplete
    ns: Incomplete
    added: Incomplete
    def __init__(
        self, dict: Incomplete, doc: Incomplete, ns: Incomplete
    ) -> None: ...
    def __call__(self, func: Incomplete) -> Incomplete: ...
    def __getitem__(self, name: Incomplete) -> Incomplete: ...
    def __setitem__(self, name: Incomplete, value: Incomplete) -> None: ...
    def resolve(self) -> Incomplete: ...

def is_descriptor(obj: Incomplete) -> Incomplete: ...
def is_dunder(name: Incomplete) -> Incomplete: ...
def is_sunder(name: Incomplete) -> Incomplete: ...
def is_internal_class(cls_name: Incomplete, obj: Incomplete) -> Incomplete: ...
def is_private_name(cls_name: Incomplete, name: Incomplete) -> Incomplete: ...
def get_attr_from_chain(cls: Incomplete, attr: Incomplete) -> Incomplete: ...
def _value(obj: Incomplete) -> Incomplete: ...

class constant:
    value: Incomplete
    __doc__: Incomplete
    def __init__(
        self, value: Incomplete, doc: Incomplete | None = None
    ) -> None: ...
    def __get__(self, *args: Incomplete) -> Incomplete: ...
    def __and__(self, other: Incomplete) -> Incomplete: ...
    def __rand__(self, other: Incomplete) -> Incomplete: ...
    def __invert__(self) -> Incomplete: ...
    def __or__(self, other: Incomplete) -> Incomplete: ...
    def __ror__(self, other: Incomplete) -> Incomplete: ...
    def __xor__(self, other: Incomplete) -> Incomplete: ...
    def __rxor__(self, other: Incomplete) -> Incomplete: ...
    def __abs__(self) -> Incomplete: ...
    def __add__(self, other: Incomplete) -> Incomplete: ...
    def __radd__(self, other: Incomplete) -> Incomplete: ...
    def __neg__(self) -> Incomplete: ...
    def __pos__(self) -> Incomplete: ...
    def __rdiv__(self, other: Incomplete) -> Incomplete: ...
    def __floordiv__(self, other: Incomplete) -> Incomplete: ...
    def __rfloordiv__(self, other: Incomplete) -> Incomplete: ...
    def __truediv__(self, other: Incomplete) -> Incomplete: ...
    def __rtruediv__(self, other: Incomplete) -> Incomplete: ...
    def __lshift__(self, other: Incomplete) -> Incomplete: ...
    def __rlshift__(self, other: Incomplete) -> Incomplete: ...
    def __rshift__(self, other: Incomplete) -> Incomplete: ...
    def __rrshift__(self, other: Incomplete) -> Incomplete: ...
    def __mod__(self, other: Incomplete) -> Incomplete: ...
    def __rmod__(self, other: Incomplete) -> Incomplete: ...
    def __mul__(self, other: Incomplete) -> Incomplete: ...
    def __rmul__(self, other: Incomplete) -> Incomplete: ...
    def __pow__(self, other: Incomplete) -> Incomplete: ...
    def __rpow__(self, other: Incomplete) -> Incomplete: ...
    def __sub__(self, other: Incomplete) -> Incomplete: ...
    def __rsub__(self, other: Incomplete) -> Incomplete: ...
    name: Incomplete
    clsname: Incomplete
    def __set_name__(
        self, ownerclass: Incomplete, name: Incomplete
    ) -> None: ...

def make_class_unpicklable(obj: Incomplete) -> None: ...

class NonMember:
    value: Incomplete
    def __init__(self, value: Incomplete) -> None: ...
    def __get__(
        self, instance: Incomplete, ownerclass: Incomplete | None = None
    ) -> Incomplete: ...

skip = NonMember
nonmember = NonMember

class Member:
    value: Incomplete
    def __init__(self, value: Incomplete) -> None: ...

member = Member
