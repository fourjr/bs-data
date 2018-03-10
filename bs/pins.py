"""
Clan badges
"""

from .base import BaseGen


class Pins(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="pins")

    def run(self):
        data = self.load_csv(exclude_empty=False)
        self.save_json(data)
