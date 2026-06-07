# content   = Pipeline start
# date      = 03.23.2026
# author    = Ronny Ascencio <ronnyascencio.com>


from ..ACore import Events, Context
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Project:
    STRUCTURE = {
        "assets": {
            "characters": [],
            "props": [],
            "environments": [],
            "fx": [],
        },
        "shots": {},
        "render": ["preview", "final"],
        "config": {},
    }

    pipe = Context.Pipeline()
    projects_root: Path = pipe.read_ateru_config()

    def create(self, project_name):
        """create project"""
        structure = self.STRUCTURE

        base_path = self.projects_root / project_name

        def recoursive_create(base_path, data):
            if isinstance(data, dict):
                for folder, contents in data.items():
                    new_path = base_path / folder
                    new_path.mkdir(parents=True, exist_ok=True)
                    Events.info(f"[DEBUG] Directory Created: {new_path} ")
                    recoursive_create(new_path, contents)
            elif isinstance(data, list):
                for item in data:
                    item_path = base_path / item
                    item_path.mkdir(parents=True, exist_ok=True)
                    Events.info(f"[DEBUG] Directory Created: {item_path} ")

        recoursive_create(base_path, structure)
        Events.info(f"[DEBUG] project created : {project_name}")
        

    def delate():
        """delate projects"""
        Events.info("Delate func from start")

    def update():
        """Update project"""
        Events.info("Update func from start")

    def config():
        """Project Configuration"""
        Events.info("Config func from start")

    def read():
        """List Projects"""
        Events.info("Read func from start")
