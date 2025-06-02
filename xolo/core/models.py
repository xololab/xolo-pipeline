

from pydantic import BaseModel

class ProjectData(BaseModel):
    """
    Metadata for the project config file
    """
    name: str
    resolution: str
    fps: str

class FolderStructure(BaseModel):
    """
    folder structure that will be created in the base path of the PROJECTS_ROOT
    """
    assets: str = "/assets"
    shots: str = "/shots"
    renders: str = "/renders"
    editorial: str = "/editorial"
    reviews: str = "/reviews"
    delivery: str = "/delivery"
    published: str = "/published"