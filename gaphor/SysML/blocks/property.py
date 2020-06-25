"""Property item."""

from typing import Sequence, Union

from gaphor import UML
from gaphor.core.modeling.properties import attribute
from gaphor.diagram.presentation import ElementPresentation, Named
from gaphor.diagram.shapes import Box, EditableText, Text, draw_border
from gaphor.diagram.support import represents
from gaphor.diagram.text import FontWeight, VerticalAlign
from gaphor.UML.classes.stereotype import stereotype_compartments


@represents(UML.Property)
class PropertyItem(ElementPresentation[UML.Property], Named):
    def __init__(self, id=None, model=None):
        super().__init__(id, model)

        self.watch("show_stereotypes", self.update_shapes)
        self.watch("subject[NamedElement].name")
        self.watch("subject.appliedStereotype", self.update_shapes)
        self.watch("subject.appliedStereotype.classifier.name")
        self.watch("subject.appliedStereotype.slot", self.update_shapes)
        self.watch("subject.appliedStereotype.slot.definingFeature.name")
        self.watch("subject.appliedStereotype.slot.value", self.update_shapes)
        self.watch("subject[Property].aggregation", self.update_shapes)

    show_stereotypes: attribute[int] = attribute("show_stereotypes", int)

    def alignment(self) -> VerticalAlign:
        if self.canvas and self.canvas.get_children(self):
            return VerticalAlign.TOP
        else:
            return VerticalAlign.MIDDLE

    def dash(self) -> Sequence[Union[int, float]]:
        if self.subject and self.subject.aggregation != "composite":
            return (7.0, 5.0)
        else:
            return ()

    def update_shapes(self, event=None):
        self.shape = Box(
            Box(
                Text(text=lambda: UML.model.stereotypes_str(self.subject),),
                EditableText(
                    text=lambda: self.subject.name or "",
                    style={"font-weight": FontWeight.BOLD},
                ),
                style={"padding": (12, 4, 12, 4), "min-height": 44},
            ),
            *(self.show_stereotypes and stereotype_compartments(self.subject) or []),
            style={
                "min-width": 100,
                "min-height": 50,
                "vertical-align": self.alignment(),
                "dash-style": self.dash(),
            },
            draw=draw_border
        )