from typing import TYPE_CHECKING

from Journey.BaseActionComponent import BaseActionComponent, ActionConcern

if TYPE_CHECKING:
    from Journey.Journey import Journey

class CapitalLayout(BaseActionComponent):
    def __init__(self, parent: "Journey"):
        super().__init__(parent, ActionConcern.Layout)
        