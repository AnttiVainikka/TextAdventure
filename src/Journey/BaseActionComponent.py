from abc import ABC

from Journey.Action import Action, Actions, ActionConcern

import log

_logger = log.getLogger(__name__)

class BaseActionComponent(ABC):
    def __init__(self, parent: "BaseActionComponent", action_concern: ActionConcern):
        self._parent = parent
        self._action_concern = action_concern

    @property
    def parent(self) -> object:
        return self._parent
    
    @parent.setter
    def parent(self, parent: "BaseActionComponent"):
        self._parent = parent

    @property
    def concern(self) -> ActionConcern:
        return self._action_concern
    
    @concern.setter
    def concern(self, concern: ActionConcern):
        self._action_concern = concern

    def _raise_actions(self, actions: Actions):
        for action in actions:
            _logger.debug(f"{type(self).__name__} raised action {type(action).__name__}")
        if self._parent is not None:
            self._parent._accept_actions(actions)

    def _raise_action(self, action: Action):
        _logger.debug(f"{type(self).__name__} raised action {type(action).__name__}")
        if self._parent is not None:
            self._parent._accept_action(action)
        
    def _accept_actions(self, actions: Actions):
        self._process_actions(actions)
        self._raise_actions(actions)

    def _accept_action(self, action: Action):
        if self._action_concern in action.concern:
            self._process_action(action)
        self._raise_action(action)

    def _process_actions(self, actions: Actions):
        for action in actions.specific(self._action_concern):
            self._process_action(action)

    def _process_action(self, action: Action):
        _logger.debug(f"{type(self).__name__} received action {type(action).__name__}")
        action_method_str = f"_process_{type(action).__name__}"
        if hasattr(self, action_method_str):
            action_method = getattr(self, action_method_str)
            action_method(action)
        else:
            _logger.warning(f"{type(self).__name__} received action {type(action).__name__}, but the processing is not implemented")
