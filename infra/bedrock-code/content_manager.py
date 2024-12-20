import json
import random
from typing import Dict, List, Optional

class ContentManager:
    def __init__(self, content_file: str = 'game_content.json'):
        with open(content_file, 'r') as f:
            self.content = json.load(f)
            
    def get_random_location(self) -> Dict:
        """Get a random location with its details"""
        return random.choice(self.content['locations'])
        
    def generate_quest(self, quest_type: str = 'main_quests') -> Dict:
        """Generate a quest from templates"""
        quest_template = random.choice(self.content['quest_templates'][quest_type])
        location = self.get_random_location()
        
        # Fill in template variables
        quest = {
            'type': quest_template['type'],
            'description': quest_template['template'].format(
                location=location['name'],
                faction=random.choice(['Tech-Mages', 'Digital Druids', 'Quantum Knights']),
                artifact='Mysterious Artifact',  # Could be more dynamic
                character_type=random.choice(['merchant', 'scholar', 'adventurer'])
            )
        }
        
        if 'complications' in quest_template:
            quest['complications'] = random.choice(quest_template['complications'])
        
        return quest
        
    def generate_npc(self, npc_type: Optional[str] = None) -> Dict:
        """Generate an NPC with personality and dialogue"""
        if not npc_type:
            npc_type = random.choice([char['type'] for char in self.content['archetypes']['characters']])
            
        character = next(char for char in self.content['archetypes']['characters'] 
                        if char['type'] == npc_type)
                        
        return {
            'type': character['type'],
            'traits': random.sample(character['traits'], 2),
            'dialogue': random.choice(character['dialogue_patterns'])
        }
        
    def generate_item(self, item_type: str = 'weapons') -> Dict:
        """Generate a random item of specified type"""
        category = random.choice(self.content['items'][item_type])
        template = random.choice(category['templates'])
        
        # Fill in template variables
        if item_type == 'weapons':
            return {
                'name': template['name'].format(
                    element=random.choice(['Fire', 'Ice', 'Lightning', 'Quantum']),
                    weapon_type=random.choice(['Sword', 'Axe', 'Spear'])
                ),
                'description': template['description'],
                'effects': random.sample(template['effects'], 1)
            }
        return template
        
    def get_progression_requirements(self, level: int) -> Dict:
        """Get progression requirements for a given level"""
        level_data = next((lvl for lvl in self.content['progression_systems']['levels']['experience_curve'] 
                          if lvl['level'] == level), None)
        return level_data if level_data else {'level': level, 'exp_required': level * 1000}
        
    def generate_random_event(self, location_type: str = 'city') -> Dict:
        """Generate a random event appropriate for the location"""
        event_type = random.choice(['weather', 'random_events', 'enemy_spawns'])
        
        if event_type == 'enemy_spawns':
            enemies = self.content['dynamic_elements']['enemy_spawns'][location_type]
            return {
                'type': 'encounter',
                'description': f'You encounter {random.choice(enemies)}!',
                'enemies': random.sample(enemies, random.randint(1, 3))
            }
        
        events = self.content['dynamic_elements'][event_type]
        return {
            'type': event_type,
            'description': f'A {random.choice(events)} occurs!',
            'duration': random.randint(1, 5)  # time in game hours
        }

    def get_skill_tree(self, category: str) -> List[str]:
        """Get available skills in a category"""
        return self.content['progression_systems']['skills'].get(category, [])