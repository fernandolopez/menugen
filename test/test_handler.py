from abc import ABC
from pathlib import Path

import pytest

from menugen.handler import Handler, Priority


def test_handler_is_abc():
    assert issubclass(Handler, ABC)


def test_handler_subclasses_enforce_handle_method_implementation():
    with pytest.raises(TypeError):

        class ConcreteHandler(Handler, priority=0):
            pass

        ch = ConcreteHandler()
