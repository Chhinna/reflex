"""Interactive components provided by @radix-ui/themes."""
from typing import Any, Dict, Literal

import reflex as rx
from reflex.components import el
from reflex.components.component import Component
from reflex.components.core.debounce import DebounceInput
from reflex.components.radix.themes.components.icons import Icon
from reflex.constants import EventTriggers
from reflex.vars import Var

from ..base import (
    LiteralAccentColor,
    LiteralRadius,
    RadixThemesComponent,
)

LiteralTextFieldSize = Literal["1", "2", "3"]
LiteralTextFieldVariant = Literal["classic", "surface", "soft"]


class TextFieldRoot(el.Div, RadixThemesComponent):
    """Captures user input with an optional slot for buttons and icons."""

    tag = "TextField.Root"

    # Text field size "1" - "3"
    size: Var[LiteralTextFieldSize]

    # Variant of text field: "classic" | "surface" | "soft"
    variant: Var[LiteralTextFieldVariant]

    # Override theme color for text field
    color_scheme: Var[LiteralAccentColor]

    # Override theme radius for text field: "none" | "small" | "medium" | "large" | "full"
    radius: Var[LiteralRadius]


class TextFieldInput(el.Input, TextFieldRoot):
    """The input part of a TextField, may be used by itself."""

    tag = "TextField.Input"

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create an Input component.

        Args:
            *children: The children of the component.
            **props: The properties of the component.

        Returns:
            The component.
        """
        if props.get("value") is not None and props.get("on_change"):
            # create a debounced input if the user requests full control to avoid typing jank
            return DebounceInput.create(super().create(*children, **props))
        return super().create(*children, **props)

    def get_event_triggers(self) -> Dict[str, Any]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            **super().get_event_triggers(),
            EventTriggers.ON_CHANGE: lambda e0: [e0.target.value],
            EventTriggers.ON_FOCUS: lambda e0: [e0.target.value],
            EventTriggers.ON_BLUR: lambda e0: [e0.target.value],
            EventTriggers.ON_KEY_DOWN: lambda e0: [e0.key],
            EventTriggers.ON_KEY_UP: lambda e0: [e0.key],
        }


class TextFieldSlot(RadixThemesComponent):
    """Contains icons or buttons associated with an Input."""

    tag = "TextField.Slot"

    # Override theme color for text field slot
    color_scheme: Var[LiteralAccentColor]


class Input(RadixThemesComponent):
    """High level wrapper for the Input component."""

    # The icon to render before the input.
    icon: Var[str]

    # Text field size "1" - "3"
    size: Var[LiteralTextFieldSize]

    # Variant of text field: "classic" | "surface" | "soft"
    variant: Var[LiteralTextFieldVariant]

    # Override theme color for text field
    color_scheme: Var[LiteralAccentColor]

    # Override theme radius for text field: "none" | "small" | "medium" | "large" | "full"
    radius: Var[LiteralRadius]

    # Whether the input should have autocomplete enabled
    auto_complete: Var[bool]

    # The value of the input when initially rendered.
    default_value: Var[str]

    # Disables the input
    disabled: Var[bool]

    # Specifies the maximum number of characters allowed in the input
    max_length: Var[str]

    # Specifies the minimum number of characters required in the input
    min_length: Var[str]

    # Name of the input, used when sending form data
    name: Var[str]

    # Placeholder text in the input
    placeholder: Var[str]

    # Indicates that the input is required
    required: Var[bool]

    # Value of the input
    value: Var[str]

    @classmethod
    def create(cls, **props):
        """Create an Input component.

        Args:
            **props: The properties of the component.

        Returns:
            The component.
        """
        input_props = {
            prop: props.pop(prop)
            for prop in [
                "auto_complete",
                "default_value",
                "disabled",
                "max_length",
                "min_length",
                "name",
                "placeholder",
                "required",
                "value",
                "on_change",
                "on_focus",
                "on_blur",
                "on_key_down",
                "on_key_up",
            ]
            if prop in props
        }

        icon = props.pop("icon", None)

        return TextFieldRoot.create(
            TextFieldSlot.create(Icon.create(tag=icon)) if icon else rx.fragment(),
            TextFieldInput.create(**input_props),
            **props,
        )

    def get_event_triggers(self) -> Dict[str, Any]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            **super().get_event_triggers(),
            EventTriggers.ON_CHANGE: lambda e0: [e0.target.value],
            EventTriggers.ON_FOCUS: lambda e0: [e0.target.value],
            EventTriggers.ON_BLUR: lambda e0: [e0.target.value],
            EventTriggers.ON_KEY_DOWN: lambda e0: [e0.key],
            EventTriggers.ON_KEY_UP: lambda e0: [e0.key],
        }
