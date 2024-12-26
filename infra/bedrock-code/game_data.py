# import random
# from typing import Dict, List, Optional
# import json

# class GameState:
#     def __init__(self):
#         self.story_templates = {
#             "quests": [
#                 {
#                     "type": "main_quest",
#                     "templates": [
#                         "A mysterious {artifact} has been discovered in the {location}",
#                         "The {faction} threatens the balance between magic and technology",
#                         "An ancient {entity} has awakened in the {location}"
#                     ]
#                 },
#                 {
#                     "type": "side_quest",
#                     "templates": [
#                         "A local {npc_type} needs help with {problem}",
#                         "Strange {phenomena} have been reported in the {location}",
#                         "A valuable {item} has been stolen by {enemy}"
#                     ]
#                 }
#             ],
#             "locations": [
#                 {
#                     "name": "Crystal Spire",
#                     "description": "A towering structure where magic and technology intertwine",
#                     "possible_events": ["magical anomalies", "tech malfunctions", "mysterious visitors"]
#                 },
#                 {
#                     "name": "Neon Bazaar",
#                     "description": "A bustling marketplace where traders deal in both spells and circuits",
#                     "possible_events": ["shady deals", "rare item auctions", "information exchange"]
#                 },
#                 {
#                     "name": "The Void Gardens",
#                     "description": "A park where reality itself seems to shift and change",
#                     "possible_events": ["reality warps", "dimensional rifts", "time anomalies"]
#                 }
#             ]
#         }

#     def generate_quest(self, quest_type: str, player_state: Dict) -> Dict:
#         """Generate a quest based on player's current state and progress"""
#         quest_template = random.choice([q for q in self.story_templates["quests"] 
#                                      if q["type"] == quest_type])
        
#         # Fill in template based on player state and game context
#         quest_details = {
#             "id": str(random.randint(1000, 9999)),  # Added quest ID
#             "template": random.choice(quest_template["templates"]),
#             "location": random.choice(self.story_templates["locations"]),
#             "difficulty": min(max(1, player_state["level"] // 3), 10),
#             "rewards": self.generate_rewards(player_state["level"])
#         }
        
#         return quest_details

#     def generate_rewards(self, player_level: int) -> Dict:
#         """Generate appropriate rewards based on player level"""
#         return {
#             "experience": player_level * 100,
#             "gold": player_level * 50,
#             "items": [
#                 self.generate_item(player_level)
#                 for _ in range(random.randint(1, 3))
#             ]
#         }

#     def generate_item(self, player_level: int) -> Dict:
#         """Generate a level-appropriate item"""
#         item_types = ["weapon", "armor", "spell_tome", "tech_gadget", "artifact"]
#         rarities = ["common", "uncommon", "rare", "epic", "legendary"]
        
#         rarity_chance = random.random()
#         rarity = rarities[min(int(rarity_chance * 10), 4)]
        
#         return {
#             "type": random.choice(item_types),
#             "rarity": rarity,
#             "level": player_level,
#             "power": player_level * (rarities.index(rarity) + 1)
#         }

# class PlayerState:
#     def __init__(self, user_id: str):
#         self.user_id = user_id
#         self.stats = {
#             "health": 100,
#             "magic": 50,
#             "technology": 50,
#             "charisma": 50,
#             "level": 1,
#             "experience": 0
#         }
#         self.inventory = []
#         self.quest_log = []
#         self.story_flags = set()

#     def update_stats(self, changes: Dict):
#         """Update player stats based on choices and events"""
#         for stat, change in changes.items():
#             if stat in self.stats:
#                 self.stats[stat] = max(0, min(100, self.stats[stat] + change))

#     def add_item(self, item: Dict):
#         """Add an item to player's inventory"""
#         self.inventory.append(item)

#     def add_experience(self, amount: int):
#         """Add experience and handle level ups"""
#         self.stats["experience"] += amount
        
#         # Level up if enough experience
#         while self.stats["experience"] >= self.stats["level"] * 1000:
#             self.stats["experience"] -= self.stats["level"] * 1000
#             self.stats["level"] += 1
            
#             # Boost stats on level up
#             for stat in ["health", "magic", "technology", "charisma"]:
#                 self.stats[stat] = min(100, self.stats[stat] + 5)

#     def add_quest(self, quest: Dict):
#         """Add a new quest to the player's quest log"""
#         self.quest_log.append(quest)

#     def complete_quest(self, quest_id: str, rewards: Dict):
#         """Complete a quest and grant rewards"""
#         self.quest_log = [q for q in self.quest_log if q["id"] != quest_id]
#         self.add_experience(rewards["experience"])
#         for item in rewards["items"]:
#             self.add_item(item)

import random
from typing import Dict, List, Optional
import json
from datetime import datetime

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
                }
            ]
        }

    def generate_quest(self, quest_type: str, player_state: Dict) -> Dict:
        """Generate a quest based on player's current state and progress"""
        try:
            quest_template = random.choice([q for q in self.story_templates["quests"] 
                                         if q["type"] == quest_type])
            
            quest_details = {
                "id": f"quest_{random.randint(1000, 9999)}",
                "type": quest_type,
                "template": random.choice(quest_template["templates"]),
                "difficulty": min(max(1, player_state.get("level", 1) // 3), 10),
                "rewards": self.generate_rewards(player_state.get("level", 1)),
                "status": "active",
                "created_at": datetime.utcnow().isoformat()
            }
            
            return quest_details
        except Exception as e:
            print(f"Error generating quest: {str(e)}")
            return self._generate_fallback_quest()

    def generate_rewards(self, player_level: int) -> Dict:
        """Generate appropriate rewards based on player level"""
        try:
            return {
                "experience": player_level * 100,
                "gold": player_level * 50,
                "items": [
                    self.generate_item(player_level)
                    for _ in range(random.randint(1, 3))
                ]
            }
        except Exception as e:
            print(f"Error generating rewards: {str(e)}")
            return {"experience": 100, "gold": 50, "items": []}

    def generate_item(self, player_level: int) -> Dict:
        """Generate a level-appropriate item"""
        try:
            item_types = ["weapon", "armor", "spell_tome", "tech_gadget", "artifact"]
            rarities = ["common", "uncommon", "rare", "epic", "legendary"]
            
            rarity_chance = random.random()
            rarity = rarities[min(int(rarity_chance * 10), 4)]
            
            return {
                "id": f"item_{random.randint(1000, 9999)}",
                "type": random.choice(item_types),
                "rarity": rarity,
                "level": player_level,
                "power": player_level * (rarities.index(rarity) + 1),
                "created_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Error generating item: {str(e)}")
            return self._generate_fallback_item()

    def _generate_fallback_quest(self) -> Dict:
        """Generate a fallback quest when normal generation fails"""
        return {
            "id": f"quest_{random.randint(1000, 9999)}",
            "type": "side_quest",
            "template": "A simple task needs to be completed",
            "difficulty": 1,
            "rewards": {"experience": 100, "gold": 50, "items": []},
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        }

    def _generate_fallback_item(self) -> Dict:
        """Generate a fallback item when normal generation fails"""
        return {
            "id": f"item_{random.randint(1000, 9999)}",
            "type": "misc",
            "rarity": "common",
            "level": 1,
            "power": 1,
            "created_at": datetime.utcnow().isoformat()
        }

class PlayerState:
    def __init__(self, user_id: str, game_id: str = 'current'):
        self.user_id = user_id
        self.game_id = game_id
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
        self.last_updated = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        """Convert state to DynamoDB format"""
        try:
            return {
                'userId': self.user_id,
                'gameId': self.game_id,
                'stats': self.stats,
                'inventory': self.inventory,
                'quest_log': self.quest_log,
                'story_flags': list(self.story_flags),
                'timestamp': self.last_updated
            }
        except Exception as e:
            print(f"Error converting player state to dict: {str(e)}")
            return {
                'userId': self.user_id,
                'gameId': self.game_id,
                'stats': self.stats,
                'timestamp': self.last_updated
            }

    @classmethod
    def from_dict(cls, data: Dict):
        """Create PlayerState from DynamoDB data"""
        try:
            state = cls(data['userId'], data.get('gameId', 'current'))
            state.stats = data.get('stats', state.stats)
            state.inventory = data.get('inventory', [])
            state.quest_log = data.get('quest_log', [])
            state.story_flags = set(data.get('story_flags', []))
            state.last_updated = data.get('timestamp', datetime.utcnow().isoformat())
            return state
        except Exception as e:
            print(f"Error creating player state from dict: {str(e)}")
            return cls(data.get('userId', 'unknown'))

    def update_stats(self, changes: Dict):
        """Update player stats based on choices and events"""
        try:
            for stat, change in changes.items():
                if stat in self.stats:
                    self.stats[stat] = max(0, min(100, self.stats[stat] + change))
            self.last_updated = datetime.utcnow().isoformat()
        except Exception as e:
            print(f"Error updating stats: {str(e)}")

    def add_item(self, item: Dict):
        """Add an item to player's inventory"""
        try:
            if not item.get('id'):
                item['id'] = f"item_{random.randint(1000, 9999)}"
            self.inventory.append(item)
            self.last_updated = datetime.utcnow().isoformat()
        except Exception as e:
            print(f"Error adding item: {str(e)}")

    def add_quest(self, quest: Dict):
        """Add a new quest to the player's quest log"""
        try:
            if not quest.get('id'):
                quest['id'] = f"quest_{random.randint(1000, 9999)}"
            quest['status'] = 'active'
            quest['started_at'] = datetime.utcnow().isoformat()
            self.quest_log.append(quest)
            self.last_updated = datetime.utcnow().isoformat()
        except Exception as e:
            print(f"Error adding quest: {str(e)}")

    def complete_quest(self, quest_id: str, rewards: Dict):
        """Complete a quest and grant rewards"""
        try:
            for quest in self.quest_log:
                if quest['id'] == quest_id:
                    quest['status'] = 'completed'
                    quest['completed_at'] = datetime.utcnow().isoformat()
                    self.add_experience(rewards.get('experience', 0))
                    for item in rewards.get('items', []):
                        self.add_item(item)
                    break
            self.last_updated = datetime.utcnow().isoformat()
        except Exception as e:
            print(f"Error completing quest: {str(e)}")

    def add_experience(self, amount: int):
        """Add experience and handle level ups"""
        try:
            self.stats["experience"] += amount
            while self.stats["experience"] >= self.stats["level"] * 1000:
                self.stats["experience"] -= self.stats["level"] * 1000
                self.stats["level"] += 1
                for stat in ["health", "magic", "technology", "charisma"]:
                    self.stats[stat] = min(100, self.stats[stat] + 5)
            self.last_updated = datetime.utcnow().isoformat()
        except Exception as e:
            print(f"Error adding experience: {str(e)}")