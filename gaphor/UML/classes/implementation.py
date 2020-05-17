"""
Implementation of interface.
"""

import gaphas

from gaphor import UML
from gaphor.diagram.presentation import LinePresentation, Named
from gaphor.diagram.shapes import Box, EditableText, Text
from gaphor.diagram.support import represents
from gaphor.UML.classes.interface import Folded, InterfacePort
from gaphor.UML.modelfactory import stereotypes_str


@represents(UML.Implementation)
class ImplementationItem(LinePresentation, Named):
    def __init__(self, id=None, model=None):
        super().__init__(id, model, style={"dash-style": (7.0, 5.0)})

        self.shape_middle = Box(
            Text(
                text=lambda: stereotypes_str(self.subject),
                style={"min-width": 0, "min-height": 0},
            ),
            EditableText(text=lambda: self.subject.name or ""),
        )
        self.watch("subject[NamedElement].name")
        self.watch("subject.appliedStereotype.classifier.name")

    def connected_to_folded_interface(self):
        assert isinstance(self.canvas, gaphas.Canvas)
        connection = self.canvas.get_connection(self.head)
        return (
            connection
            and isinstance(connection.port, InterfacePort)
            and connection.connected.folded != Folded.NONE
        )

    def post_update(self, context):
        super().post_update(context)
        if self.connected_to_folded_interface():
            self.style = {"dash-style": ()}
        else:
            self.style = {"dash-style": (7.0, 5.0)}

    def draw_head(self, context):
        cr = context.cairo
        cr.move_to(0, 0)
        if self.style("dash-style"):
            cr.set_dash((), 0)
            cr.line_to(15, -10)
            cr.line_to(15, 10)
            cr.close_path()
            cr.stroke()
            cr.move_to(15, 0)
