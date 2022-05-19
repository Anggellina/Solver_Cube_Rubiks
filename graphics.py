from ursina import *

import cube
from solve import Solver

Colors = {"W": color.white, "R": color.red, "Y": color.yellow, "O": color.orange, "B": color.blue, "G": color.green}


class Graphics:
    def __init__(self, Cube):

        # окружение вокруг кубика
        Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)
        Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.dark_gray)  # plane

        self._Win = Ursina()
        self._Cube = Cube
        self._Flat = Cube.Flat
        self._SetupCube()
        self._SetupArrows()
        self.Cam = EditorCamera()

    def Start(self):
        self._Win.run()
        self._Cube

    def Stop(self):
        self._Win.quit()

    def _SendOrientedMove(self, Move):
        getattr(self._Cube, Move)()

    # функия вызывающая решатель
    def Solve(self, D):
        strCub = getattr(self._Cube, D)()

        c = cube.Cube(strCub)
        solver = Solver(c)
        solver.solve()
        for i in solver.moves:
            self._SendOrientedMove(i)
            self._UpdateCubeGraphics()

    # обновление цветов кубика
    def _UpdateCubeGraphics(self):
        for i in range(9 * 6):
            self._Flat[i].color = Colors[self._Cube.Flat[i]]

    # основная функция просмотра кнопок с камеры
    def _MakeMove(self, Position=(0, 0, 0), Color=color.black, Rot=(0, 0, 0), Ext="arrow_down"):
        return Draggable(parent=camera.ui, model="cube", color=Color, position=Position, texture=Ext,
                         scale=Vec2(.07, .04), rotation=Rot, require_key="left shift")

    # основная функция просмотра кубика с камеры
    def _MakePiece(self, Position=(1, 0, 0), Color=color.black, Rotation=(0, 0, 0)):
        return Entity(parent=scene, model="quad", color=Color, position=Position, texture="white_cube",
                      rotation=Rotation)

    # расположение кубика
    def _SetupCube(self):
        FaceColor = iter(self._Flat)
        self._Front = [self._MakePiece((x - 1, y - 1, -1.5), Colors[next(FaceColor)]) for y in reversed(range(3)) for x
                       in range(3)]
        self._Right = [self._MakePiece((1.5, y - 1, z - 1), Colors[next(FaceColor)], (0, -90, 0)) for y in
                       reversed(range(3)) for z in range(3)]
        self._Back = [self._MakePiece((x - 1, y - 1, 1.5), Colors[next(FaceColor)], (180, 0, 0)) for y in
                      reversed(range(3)) for x in reversed(range(3))]
        self._Left = [self._MakePiece((-1.5, y - 1, z - 1), Colors[next(FaceColor)], (0, 90, 0)) for y in
                      reversed(range(3)) for z in reversed(range(3))]
        self._Up = [self._MakePiece((x - 1, 1.5, z - 1), Colors[next(FaceColor)], (90, 0, 0)) for z in
                    reversed(range(3)) for x in range(3)]
        self._Down = [self._MakePiece((x - 1, -1.5, z - 1), Colors[next(FaceColor)], (-90, 0, 0)) for z in range(3) for
                      x in range(3)]
        self._Flat = self._Front + self._Right + self._Back + self._Left + self._Up + self._Down

    # расположение кнопок
    def _SetupArrows(self):
        RPMove = self._MakeMove((self._Front[2].screen_position[0], self._Front[2].screen_position[1] + .12, 0),
                                color.violet, (180, 0, 0))
        RPMove.tooltip = Tooltip("R", scale=Vec2(0.5, 0.5))
        RPMove.on_click = lambda: self._SendOrientedMove("Ri")
        MMove = self._MakeMove((self._Front[1].screen_position[0], self._Front[1].screen_position[1] + .12, 0),
                               color.violet, (180, 0, 0))
        MMove.tooltip = Tooltip("M", scale=Vec2(0.5, 0.5))
        MMove.on_click = lambda: self._SendOrientedMove("M")
        LMove = self._MakeMove((self._Front[0].screen_position[0], self._Front[0].screen_position[1] + .12, 0),
                               color.violet, (180, 0, 0))
        LMove.tooltip = Tooltip("L", scale=Vec2(0.5, 0.5))
        LMove.on_click = lambda: self._SendOrientedMove("L")

        RMove = self._MakeMove((self._Front[8].screen_position[0], self._Front[8].screen_position[1] - .12, 0),
                               color.violet, (0, 0, 0))
        RMove.tooltip = Tooltip("R'", scale=Vec2(0.5, 0.5))
        RMove.on_click = lambda: self._SendOrientedMove("R")
        MPMove = self._MakeMove((self._Front[7].screen_position[0], self._Front[7].screen_position[1] - .12, 0),
                                color.violet, (0, 0, 0))
        MPMove.tooltip = Tooltip("M'", scale=Vec2(0.5, 0.5))
        MPMove.on_click = lambda: self._SendOrientedMove("Mi")
        LPMove = self._MakeMove((self._Front[6].screen_position[0], self._Front[6].screen_position[1] - .12, 0),
                                color.violet, (0, 0, 0))
        LPMove.tooltip = Tooltip("L'", scale=Vec2(0.5, 0.5))
        LPMove.on_click = lambda: self._SendOrientedMove("Li")

        UPMove = self._MakeMove((self._Front[0].screen_position[0] - .15, self._Front[0].screen_position[1], 0),
                                color.violet, (0, 0, 90))
        UPMove.tooltip = Tooltip("U", scale=Vec2(0.5, 0.5))
        UPMove.on_click = lambda: self._SendOrientedMove("Ui")
        EMove = self._MakeMove((self._Front[3].screen_position[0] - .15, self._Front[3].screen_position[1], 0),
                               color.violet, (0, 0, 90))
        EMove.tooltip = Tooltip("E", scale=Vec2(0.5, 0.5))
        EMove.on_click = lambda: self._SendOrientedMove("E")
        DMove = self._MakeMove((self._Front[6].screen_position[0] - .15, self._Front[6].screen_position[1], 0),
                               color.violet, (0, 0, 90))
        DMove.tooltip = Tooltip("D", scale=Vec2(0.5, 0.5))
        DMove.on_click = lambda: self._SendOrientedMove("D")

        UMove = self._MakeMove((self._Front[2].screen_position[0] + .15, self._Front[2].screen_position[1], 0),
                               color.violet, (0, 0, -90))
        UMove.tooltip = Tooltip("U'", scale=Vec2(0.5, 0.5))
        UMove.on_click = lambda: self._SendOrientedMove("U")
        EPMove = self._MakeMove((self._Front[5].screen_position[0] + .15, self._Front[5].screen_position[1], 0),
                                color.violet, (0, 0, -90))
        EPMove.tooltip = Tooltip("E'", scale=Vec2(0.5, 0.5))
        EPMove.on_click = lambda: self._SendOrientedMove("Ei")
        DPMove = self._MakeMove((self._Front[8].screen_position[0] + .15, self._Front[8].screen_position[1], 0),
                                color.violet, (0, 0, -90))
        DPMove.tooltip = Tooltip("D'", scale=Vec2(0.5, 0.5))
        DPMove.on_click = lambda: self._SendOrientedMove("Di")

        FMove = self._MakeMove((self._Front[0].screen_position[0] - .15, self._Front[0].screen_position[1] + .1, 0),
                               color.turquoise, (0, 180, 0), "turn")
        FMove.tooltip = Tooltip("F", scale=Vec2(0.5, 0.5))
        FMove.on_click = lambda: self._SendOrientedMove("F")
        FPMove = self._MakeMove((self._Front[2].screen_position[0] + .15, self._Front[2].screen_position[1] + .1, 0),
                                color.turquoise, (0, 0, 0), "turn")
        FPMove.tooltip = Tooltip("F'", scale=Vec2(0.5, 0.5))
        FPMove.on_click = lambda: self._SendOrientedMove("Fi")

        BMove = self._MakeMove((self._Front[6].screen_position[0] - .15, self._Front[6].screen_position[1] - .1, 0),
                               color.turquoise, (180, 180, 0), "turn")
        BMove.tooltip = Tooltip("B", scale=Vec2(0.5, 0.5))
        BMove.on_click = lambda: self._SendOrientedMove("B")
        BPMove = self._MakeMove((self._Front[8].screen_position[0] + .15, self._Front[8].screen_position[1] - .1, 0),
                                color.turquoise, (180, 0, 0), "turn")
        BPMove.tooltip = Tooltip("B'", scale=Vec2(0.5, 0.5))
        BPMove.on_click = lambda: self._SendOrientedMove("Bi")

        BPMove = self._MakeMove((self._Front[8].screen_position[0] - .95, self._Front[8].screen_position[1] + .55, 0),
                                color.text_color, (0, 0, 0), "shuffle")
        BPMove.tooltip = Tooltip("Shuffle", scale=Vec2(0.5, 0.5))
        BPMove.on_click = lambda: self._SendOrientedMove("Shuffle")

        BPMove = self._MakeMove((self._Front[8].screen_position[0] - .95, self._Front[0].screen_position[1] + .22, 0),
                                color.text_color, (0, 0, 0), "solve")
        BPMove.tooltip = Tooltip("Solve", scale=Vec2(0.5, 0.5))
        BPMove.on_click = lambda: self.Solve("Solver")

        BPMove = self._MakeMove((self._Front[8].screen_position[0] - .95, self._Front[0].screen_position[1] - .55, 0),
                                color.text_color, (0, 0, 0), "quit")
        BPMove.tooltip = Tooltip("Quit", scale=Vec2(0.5, 0.5))
        BPMove.on_click = lambda: self.Stop()
