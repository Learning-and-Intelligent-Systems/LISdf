#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# File   : shape.py
# Author : Jiayuan Mao
# Email  : maojiayuan@gmail.com
# Date   : 03/23/2022
#
# This file is part of lisdf.
# Distributed under terms of the MIT license.

"""
This file defines the basic structures for shapes, including built-in shapes and meshes.

TODO(Jiayuan Mao @ 03/23): consider object and material mapping?
"""

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional, Type

from lisdf.components.base import StringConfigurable
from lisdf.utils.typing import Vector3f


@dataclass
class ShapeInfo(StringConfigurable):
    type: ClassVar[str] = "ShapeInfo"
    type_mapping: ClassVar[Dict[str, Type["ShapeInfo"]]] = dict()

    def __init_subclass__(cls, type: str, **kwargs):
        super().__init_subclass__(**kwargs)
        setattr(cls, "type", type)
        ShapeInfo.type_mapping[type] = cls

    @staticmethod
    def from_type(type, **kwargs) -> "ShapeInfo":
        return ShapeInfo.type_mapping[type](**kwargs)


@dataclass
class BoxShapeInfo(ShapeInfo, type="box"):
    size: Vector3f

    def to_sdf(self) -> str:
        return f"""<box>
  <size>{self.size[0]} {self.size[1]} {self.size[2]}</size>
</box>
"""


@dataclass
class SphereShapeInfo(ShapeInfo, type="sphere"):
    radius: float

    def to_sdf(self) -> str:
        return f"""<sphere>
  <radius>{self.radius}</radius>
</sphere>
"""


@dataclass
class CylinderShapeInfo(ShapeInfo, type="cylinder"):
    radius: float
    half_height: float  # follows the mujoco standard.

    @property
    def length(self) -> float:
        return self.half_height * 2

    def to_sdf(self) -> str:
        return f"""<cylinder>
  <radius>{self.radius}</radius>
  <length>{self.length}</length>
</cylinder>
"""


@dataclass
class CapsuleShapeInfo(ShapeInfo, type="capsule"):
    radius: float
    half_height: float  # follows the mujoco standard.

    @property
    def length(self) -> float:
        return self.half_height * 2

    def to_sdf(self) -> str:
        return f"""<capsule>
  <radius>{self.radius}</radius>
  <length>{self.length}</length>
</capsule>
"""


@dataclass
class MeshShapeInfo(ShapeInfo, type="mesh"):
    filename: str
    size: Vector3f

    def to_sdf(self) -> str:
        return f"""<mesh>
  <uri>{self.filename}</uri>
  <scale>{self.size[0]} {self.size[1]} {self.size[2]}</scale>
</mesh>
"""


@dataclass
class PlaneShapeInfo(ShapeInfo, type="plane"):
    half_width: float  # follows the mujoco standard.
    half_height: float
    normal: Optional[Vector3f] = None

    @property
    def width(self) -> float:
        return self.half_width * 2

    @property
    def height(self) -> float:
        return self.half_height * 2

    def to_sdf(self) -> str:
        return f"""<plane>
  <size>{self.width} {self.height}</size>
</plane>
"""
