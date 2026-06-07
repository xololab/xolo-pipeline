# content   = Context read and create
# date      = 03.25.2026
# author    = Ronny Ascencio <ronnyascencio.com>

from dataclasses import dataclass
from ..ACore import Events, Config, Model, Loader
from pathlib import Path
from typing import List, Dict, Literal, Annotated, Optional
from pydantic import BaseModel, Field, field_validator
import tomli_w
import tomli as tomllib
import re


CONFIG_FILE = Path.home() / ".ateru" / "ateru_config.toml"

@dataclass
class Pipeline:
    """

    Gobal pipeline configuration

    """

    

    def ensure_config_exists(self) -> dict:
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open("rb") as f:
                return tomllib.load(f)
        else:
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            base = {
                "title": {"name": "ateru Global Configuration"},
                "root": {"projects_root": str(Path.home() / "ateru_projects")},
                "apps": {},
            }
            with CONFIG_FILE.open("wb") as f:
                tomli_w.dump(base, f)
            return base

    def read_ateru_config(self) -> Path:
        config = self.ensure_config_exists()
        root_path_str = config.get("root", {}).get("projects_root")
        if root_path_str:
            root_path = Path(root_path_str)
        else:
            root_path = Path.home() / "ateru_projects"

        root_path.mkdir(parents=True, exist_ok=True)

        return root_path

    def read_ateru_config_apps(self, dcc: str) -> Path:
        config = self.ensure_config_exists()
        dcc_str = config.get("apps", {}).get(dcc)
        dcc_path = Path(dcc_str)

        return dcc_path

    def load_config() -> dict:
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open("rb") as f:
                return tomllib.load(f)
        else:
            # Crear archivo base vacío
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            base = {"title": {"name": "Ateru Global Configuration"}}
            with CONFIG_FILE.open("wb") as f:
                tomli_w.dump(base, f)
            return base

    def write_config(data: dict):
        """secure write data."""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with CONFIG_FILE.open("wb") as f:
            tomli_w.dump(data, f)
        Events.success(f"Config File updated {CONFIG_FILE}")

    def write_global_config_root(self, Ateru: Config.GlobalConfig):
        """update root section TOML without delete apps."""
        config = self.ensure_config_exists()
        config["root"] = Ateru.model_dump(mode="json")
        with CONFIG_FILE.open("wb") as f:
            tomli_w.dump(config, f)

    def write_global_config_software(self, apps: Config.SoftwareConfig):
        """update apps section TOML without delete root."""
        config = self.ensure_config_exists()
        config["apps"] = apps.model_dump(mode="json")
        with CONFIG_FILE.open("wb") as f:
            tomli_w.dump(config, f)
            
            
            
    """ Project Context config """
    
    def write_project_config(project: Model.Project):
        config_file = project.root / "config" / "pconfig.toml"
    
        data: dict = {
            "project": project.model_dump(mode="json"),
        }
        config_file.parent.mkdir(parents=True, exist_ok=True)
    
        with config_file.open("wb") as f:
            tomli_w.dump(data, f)
        Events.success(f"Config File created {config_file}")
    
    
    def write_shot_config(shot: Model.Shot, project_name: str):
        project = Loader.read_project_config(project_name)
        shot_name = shot.shot_name
        config_file = project.root / "shots" / shot_name / "sconfig.toml"
    
        data: dict = {
            "Shot": shot.model_dump(mode="json"),
        }
    
        config_file.parent.mkdir(parents=True, exist_ok=True)
    
        with config_file.open("wb") as f:
            tomli_w.dump(data, f)
        Events.success(f"Config File created {config_file}")
    
    
    def write_asset_config(asset: Model.Asset, project_name: str):
        project = Loader.read_project_config(project_name)
        asset_name = asset.asset_name
        config_file = project.root / "assets" / asset_name / "aconfig.toml"
    
        data: dict = {
            "Asset": asset.model_dump(mode="json"),
        }
    
        config_file.parent.mkdir(parents=True, exist_ok=True)
    
        with config_file.open("wb") as f:
            tomli_w.dump(data, f)
        Events.success(f"Config File created {config_file}")
