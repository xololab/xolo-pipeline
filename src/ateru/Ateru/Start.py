# content   = Pipeline start
# date      = 03.23.2026
# author    = Ronny Ascencio <ronnyascencio.com>


from ..ACore import Events


class Project:
    def create():
        """create projects"""
        Events.info("Create func from start")

    def delate():
        """delate projects"""
        Events.info("Delate func from start")

    def update():
        """Update project"""
        pass

    def config():
        """Project Configuration"""
        pass

    def read():
        """List Projects"""
        pass
