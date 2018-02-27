"""
Clan badges
"""

from .base import BaseGen


class AreaEffects(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="area_effects")

    def run(self):
        data = self.load_csv(exclude_empty=True)
        self.save_json(data)
