#!/usr/bin/env python
"""
Generate data JSON from APK CSV source.
"""

import yaml
from box import Box

from bs import *

if __name__ == '__main__':
    config_path = './config.yml'

    with open(config_path) as f:
        config = Box(yaml.load(f))

    for cls in [AllianceBadges, AllianceRoles, AreaEffects, Bosses, Campaign, Cards, 
            Characters, Globals, Items, Locations, Maps, PlayerThumbnails, Projectiles, 
            Regions, Resources, Skills, Skins, Tiles]:
        app = cls(config=config)
        app.run()
