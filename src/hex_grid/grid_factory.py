from .hex_vertex import HexagonVertex
from .hex_enums import HexDirection, VertexDirection as VD
from .hex_grid_points import HexGridPoint
from .hex_edge import HexagonEdge


def get_neighbour_step(dir: HexDirection) -> HexGridPoint:
    match dir:
        case HexDirection.right:
            return HexGridPoint(1, 0, -1)
        case HexDirection.left:
            return HexGridPoint(-1, 0, 1)
        case HexDirection.top_right:
            return HexGridPoint(1, -1, 0)
        case HexDirection.bottom_right:
            return HexGridPoint(0, 1, -1)
        case HexDirection.top_left:
            return HexGridPoint(0, -1, 1)
        case HexDirection.bottom_left:
            return HexGridPoint(-1, 1, 0)
        case _:
            raise ValueError()


class NeighbourFactory():
    def __init__(self, hex : HexGridPoint):
        self.hex = hex

    def __call__(self, dir: HexDirection) -> HexGridPoint:
        other = get_neighbour_step(dir)
        return self.hex + other


class EdgeFactory():
    def __init__(self, hex : HexGridPoint):
        self.hex = hex

    def __call__(self, dir : HexDirection):

        match dir:
            case HexDirection.left:
                hex = NeighbourFactory(self.hex)(dir)
                dir = HexDirection.right
            case HexDirection.top_left:
                hex = NeighbourFactory(self.hex)(dir)
                dir = HexDirection.bottom_right
            case HexDirection.bottom_left:
                hex = NeighbourFactory(self.hex)(dir)
                dir = HexDirection.top_right
            case HexDirection.right | HexDirection.bottom_right | HexDirection.top_right:
                hex = self.hex
            case _:
                raise ValueError()

        return HexagonEdge(hex, dir)

class VertexFactory():
    def __init__(self, hex : HexGridPoint):
        self.hex = hex

    def __call__(self, dir : VD):

        match dir:
            case VD.top:
                hex = NeighbourFactory(self.hex)(HexDirection.top_left)
                dir = VD.bottom_right
            case VD.bottom:
                hex = NeighbourFactory(self.hex)(HexDirection.bottom_left)
                dir = VD.top_right
            case VD.top_left:
                hex = NeighbourFactory(self.hex)(HexDirection.left)
                dir = VD.top_right
            case VD.bottom_left:
                hex = NeighbourFactory(self.hex)(HexDirection.left)
                dir = VD.bottom_right
            case VD.top_right | VD.bottom_right:
                hex = self.hex
            case _:
                raise ValueError()

        return HexagonVertex(hex, dir)
