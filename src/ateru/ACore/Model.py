# content   = Models
# date      = 06.06.2026
# author    = Ronny Ascencio <ronnyascencio.com>

from pydantic import BaseModel
from pathlib import Path
from typing import Tuple


class Ateru(BaseModel):
    projects_root: Path


class Project(BaseModel):
    id: int
    name: str
    root: Path
    renders: Path
    assets: Path
    plates: Path
    shots: Path
    fps: int
    resolution: Tuple[str, str]
    type: str
    status: str


class Shot(BaseModel):
    root: Path
    shot_name: str
    start: int
    end: int
    fps: int
    priority: str


class Asset(BaseModel):
    root: Path
    asset_type: str
    asset_name: str


