# content   = Configuration and security
# date      = 03.25.2026
# author    = Ronny Ascencio <ronnyascencio.com>

import getpass


from pathlib import Path
from typing import List, Dict, Literal, Annotated, Optional
from pydantic import BaseModel, Field, field_validator






Permission = Literal["read", "write", "delete"]


class User(BaseModel):
    projects: List[str] = Field(default_factory=list)
    permissions: List[Permission] = Field(default_factory=list)


class Users(BaseModel):
    artists: Dict[str, User] = Field(default_factory=dict)
    managers: Dict[str, User] = Field(default_factory=dict)


class Projects(BaseModel):
    list: List[str] = Field(default_factory=list)


class Config(BaseModel):
    projects: Projects
    users: Users

class Security:
    def user_name() -> str:
        user = getpass.getuser()
        return user
        
        
        
""" global models """

class GlobalConfig(BaseModel):
    projects_root: Path
    ocio_config: Optional[Path]



    logs_dir: Path = Field(default_factory=lambda: Path.home() / ".ateru" / "logs")
    cache_dir: Path = Field(default_factory=lambda: Path.home() / ".ateru" / "cache")
    
class SoftwareConfig(BaseModel):
    nuke: Path
    gaffer: Path
    blender: Path