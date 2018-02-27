"""
Clan badges
"""

from .base import BaseGen


class PlayerThumbnails(BaseGen):
    def __init__(self, config):
        super().__init__(config, id="player_thumbnails")

    def run(self):
        data = self.load_csv(exclude_empty=False)
        for item in data:
            item['id'] = 28000000 + item['sort_order']
        self.save_json(data)
