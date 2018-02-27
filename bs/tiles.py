"""
Clan badges
"""

from .base import BaseGen


class Tiles(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="tiles")

    def run(self):
        data = self.load_csv(exclude_empty=True)
        self.save_json(data)
