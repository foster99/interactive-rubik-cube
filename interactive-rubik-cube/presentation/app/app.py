import random
from time import sleep

from kink import inject
from ursina import Ursina, Entity, EditorCamera, Vec3, mouse, window, invoke, scene


@inject
class App(Ursina):
    RESOURCES: dict[str, str] = {
        'cube_model': 'models/cube',
        'stickers_texture': 'textures/stickers',
    }

    # MOVEMENTS/SIDES
    LEFT: str = 'L'
    BOTTOM: str = 'B'
    FRONT: str = 'F'
    BACK: str = 'B'
    RIGHT: str = 'R'
    UP: str = 'U'

    SIDE_POSITIONS: dict[str, set[tuple[float, float, float]]] = {
        LEFT:   {Vec3(-1, +y, +z) for y in range(-1, 2) for z in range(-1, 2)},
        BOTTOM: {Vec3(+x, -1, +z) for x in range(-1, 2) for z in range(-1, 2)},
        FRONT:  {Vec3(+x, +y, -1) for x in range(-1, 2) for y in range(-1, 2)},
        BACK:   {Vec3(+x, +y, +1) for x in range(-1, 2) for y in range(-1, 2)},
        UP:     {Vec3(+x, +1, +z) for x in range(-1, 2) for z in range(-1, 2)},
        RIGHT:  {Vec3(+1, +y, +z) for y in range(-1, 2) for z in range(-1, 2)},
    }

    ROTATION_AXES: dict[str, str] = {LEFT: 'x', BOTTOM: 'y', FRONT: 'z', BACK: 'z', RIGHT: 'x', UP: 'y'}

    def __init__(self):
        super().__init__()

        # Set up window
        window.title = "Rubik's Cube"
        window.borderless = False
        window.forced_aspect_ratio = 1

        # Set up camera
        self.camera = EditorCamera()

        # Animation variables
        self.rotation_animation_time = 0.5  # seconds

        # Set up flow-control variables
        self.rotating = False

        # Generate cube's pieces
        self.PIECES: set[Entity] = {
            Entity(model=self.RESOURCES['cube_model'], texture=self.RESOURCES['stickers_texture'], position=pos)
            for side in self.SIDE_POSITIONS.values() for pos in side
        }

        # Cube's Core (entity to do rotations)
        self.rotator = Entity()
        self.rotator.rotation = 0

    def start_rotating(self):
        self.rotating = True

    def stop_rotating(self):
        self.rotating = False

    def rotate_side(self, side, prime):
        # Lock rotations
        self.start_rotating()

        # Get side variables
        side_positions = self.SIDE_POSITIONS[side]
        rotation_axis = self.ROTATION_AXES[side]
        degrees = 90 if not prime else -90
        pieces_to_rotate = [piece for piece in self.PIECES if piece.position in side_positions]

        # aaaaa
        self.reparent_to_scene()

        # Link pieces to rotate to the rotator
        for piece in pieces_to_rotate:
            piece.parent = self.rotator

        # Rotate the rotator
        self.rotator.animate(name=f'rotation_{rotation_axis}', value=degrees, duration=self.rotation_animation_time)

        sleep(self.rotation_animation_time)

        # Unlink the rotator
        # for piece in pieces_to_rotate:
        #     position, rotation = round(piece.world_position, 1), piece.world_rotation
        #     piece.parent = scene
        #     piece.position, piece.rotation = position, rotation

        # Reset rotator
        # self.rotator.rotation = 0

        # for piece in pieces_to_rotate:
        #     eval(f'piece.animate_rotation_{rotation_axis}({degrees}, duration=self.rotation_animation_time)')

        # Unlock rotations

        # self.stop_rotating()
        invoke(self.stop_rotating, delay=self.rotation_animation_time + 1)

    def reparent_to_scene(self):
        for piece in self.PIECES:
            if piece.parent == self.rotator:
                world_pos, world_rot = round(piece.world_position, 1), piece.world_rotation
                piece.parent = scene
                piece.position, piece.rotation = world_pos, world_rot
        self.rotator.rotation = 0

    def input(self, key):

        if key in 'mouse1' and not self.rotating:
            self.rotate_side(random.choice(list(self.SIDE_POSITIONS.keys())), prime=False)

        super().input(key)
