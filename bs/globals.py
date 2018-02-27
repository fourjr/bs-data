"""
Clan badges
"""

from .base import BaseGen


class Globals(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="globals")

    def run(self):
        data = self.load_csv(exclude_empty=True)
        self.save_json(data)
