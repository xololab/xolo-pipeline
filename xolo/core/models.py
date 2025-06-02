

from pydantic import BaseModel

class ProjectData(BaseModel):
    name: str
    resolution: str
    fps: str

class FolderStructure(BaseModel):
    assets: str = "/assets"
    shots: str = "/shots"
    renders: str = "/renders"
    editorial: str = "/editorial"
    reviews: str = "/reviews"
    delivery: str = "/delivery"
    published: str = "/published"