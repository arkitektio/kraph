from koil.composition import Composition
from pydantic import Field

from kraph.rath import KraphRath
from kraph.datalayer import DataLayer


class Kraph(Composition):
    rath: KraphRath
    datalayer: DataLayer
