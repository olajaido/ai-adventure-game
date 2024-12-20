import random
from typing import Dict, List, Optional
import json

class GameState:
    def __init__(self):
        self.story_templates = {
            "quests": [
                {
                    "type": "main_quest",
                    "templates": [
                        "A mysterious {artifact} has been discovered in the {location}",
                        "The {faction} threatens the balance between magic and technology",
                        "An ancient {entity} has awakened in the {location}"
                    ]
                },
                {
                    "type": "side_quest",
                    "templates": [
                        "A local {npc_type} needs help with {problem}",
                        "Strange {phenomena} have been reported in the {location}",
                        "A valuable {item} has been stolen by {enemy}"
                    ]
                }
            ],
            "locations": [
                {
                    "name": "Crystal Spire",
                    "description": "A towering structure where magic and technology intertwine",
                    "possible_events": ["magical anomalies", "tech malfunctions", "mysterious visitors"]
                },
                {
                    "name": "Neon Bazaar",
                    "description": "A bustling marketplace where traders deal in both spells and circuits",
                    "possible_events": ["shady deals", "rare item auctions", "information exchange"]
                },
                {
                    "name": "The Void Gardens",
                    "description": "A park where reality itself seems to shift and change",
                    "possible_events": ["reality warps", "dimensional rifts", "time anomalies"]
                }
            ]
        }

    def generate_quest(self, quest_type: str, player_state: Dict) -> Dict:
        """Generate a quest based on player's current state and progress"""
        quest_template = random.choice([q for q in self.story_templates["quests"] 
                                     if q["type"] == quest_type])
        
        # Fill in template based on player state and game context
        quest_details = {
            "id": str(random.randint(1000, 9999)),  # Added quest ID
            "template": random.choice(quest_template["templates"]),
            "location": random.choice(self.story_templates["locations"]),
            "difficulty": min(max(1, player_state["level"] // 3), 10),
            "rewards": self.generate_rewards(player_state["level"])
        }
        
        return quest_details

    def generate_rewards(self, player_level: int) -> Dict:
        """Generate appropriate rewards based on player level"""
        return {
            "experience": player_level * 100,
            "gold": player_level * 50,
            "items": [
                self.generate_item(player_level)
                for _ in range(random.randint(1, 3))
            ]
        }

    def generate_item(self, player_level: int) -> Dict:
        """Generate a level-appropriate item"""
        item_types = ["weapon", "armor", "spell_tome", "tech_gadget", "artifact"]
        rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        
        rarity_chance = random.random()
        rarity = rarities[min(int(rarity_chance * 10), 4)]
        
        return {
            "type": random.choice(item_types),
            "rarity": rarity,
            "level": player_level,
            "power": player_level * (rarities.index(rarity) + 1)
        }

class PlayerState:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.stats = {
            "health": 100,
            "magic": 50,
            "technology": 50,
            "charisma": 50,
            "level": 1,
            "experience": 0
        }
        self.inventory = []
        self.quest_log = []
        self.story_flags = set()

    def update_stats(self, changes: Dict):
        """Update player stats based on choices and events"""
        for stat, change in changes.items():
            if stat in self.stats:
                self.stats[stat] = max(0, min(100, self.stats[stat] + change))

    def add_item(self, item: Dict):
        """Add an item to player's inventory"""
        self.inventory.append(item)

    def add_experience(self, amount: int):
        """Add experience and handle level ups"""
        self.stats["experience"] += amount
        
        # Level up if enough experience
        while self.stats["experience"] >= self.stats["level"] * 1000:
            self.stats["experience"] -= self.stats["level"] * 1000
            self.stats["level"] += 1
            
            # Boost stats on level up
            for stat in ["health", "magic", "technology", "charisma"]:
                self.stats[stat] = min(100, self.stats[stat] + 5)

    def add_quest(self, quest: Dict):
        """Add a new quest to the player's quest log"""
        self.quest_log.append(quest)

    def complete_quest(self, quest_id: str, rewards: Dict):
        """Complete a quest and grant rewards"""
        self.quest_log = [q for q in self.quest_log if q["id"] != quest_id]
        self.add_experience(rewards["experience"])
        for item in rewards["items"]:
            self.add_item(item)