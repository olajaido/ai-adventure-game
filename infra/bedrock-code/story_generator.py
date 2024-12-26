# import json
# import boto3
# import uuid
# from typing import Dict, List, Optional
# from datetime import datetime, timedelta
# from time import sleep

# class StoryGenerator:
#     def __init__(self):
#         self.bedrock = boto3.client('bedrock-runtime')
#         self.last_request_time = datetime.now()
#         self.min_request_interval = timedelta(seconds=1)
        
#         # Game world context
#         self.game_context = {
#             "world_setting": "A mystical realm where magic and technology coexist",
#             "player_attributes": ["health", "magic", "technology", "charisma"],
#             "item_types": ["weapons", "spells", "gadgets", "artifacts"],
#             "enemy_types": ["magical creatures", "rogue AI", "corrupted beings", "ancient guardians"],
#             "locations": [
#                 "Crystal Spire City",
#                 "Neon Forest",
#                 "Quantum Ruins",
#                 "Tech-Mage Academy",
#                 "Digital Bazaar"
#             ],
#             "factions": [
#                 "Tech-Mages Alliance",
#                 "Digital Druids",
#                 "Quantum Knights",
#                 "Circuit Sages",
#                 "Binary Bandits"
#             ]
#         }

#     def _wait_for_rate_limit(self):
#         """Implement rate limiting for Bedrock API calls"""
#         time_since_last = datetime.now() - self.last_request_time
#         if time_since_last < self.min_request_interval:
#             sleep((self.min_request_interval - time_since_last).total_seconds())
#         self.last_request_time = datetime.now()

#     def generate_story_prompt(self, current_scene: Dict, player_state: Dict, choice: Optional[str] = None) -> str:
#         """Generate prompt for story continuation"""
#         return f"""
#         You are a master storyteller creating an interactive adventure game in a world where magic and technology coexist.
#         Generate the next scene based on:

#         Current Scene: {current_scene.get('description', 'Starting adventure')}
#         Player's Choice: {choice if choice else 'Starting game'}
#         Player Stats: {json.dumps(player_state)}
        
#         World Context: {json.dumps(self.game_context)}

#         Generate a JSON response with:
#         1. A vivid scene description (2-3 paragraphs)
#         2. Three distinct choices that meaningfully impact the story
#         3. Potential consequences for each choice (affecting player stats)
#         4. Any items or discoveries in the scene
#         5. Random events or encounters (20% chance)

#         Format the response as:
#         {{
#             "scene_description": "detailed description",
#             "choices": [
#                 {{
#                     "text": "choice description",
#                     "consequences": {{
#                         "health": 0,
#                         "magic": 0,
#                         "technology": 0,
#                         "charisma": 0,
#                         "items": [],
#                         "story_flags": []
#                     }}
#                 }}
#             ],
#             "environment": {{
#                 "items": [],
#                 "npcs": [],
#                 "events": []
#             }}
#         }}
#         """

#     def generate_scene(self, current_scene: Dict, player_state: Dict, choice: Optional[str] = None) -> Dict:
#         """Generate a new scene based on player's current state and choices"""
#         try:
#             self._wait_for_rate_limit()
            
#             prompt = self.generate_story_prompt(current_scene, player_state, choice)
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-v3',
#                 body=json.dumps({
#                     "prompt": prompt,
#                     "max_tokens": 1000,
#                     "temperature": 0.7,
#                     "top_p": 0.9,
#                 })
#             )
            
#             story_response = json.loads(response['body'].read().decode())
#             scene_data = json.loads(story_response['completion'])
            
#             # Add metadata for game mechanics
#             scene_data['timestamp'] = datetime.utcnow().isoformat()
#             scene_data['scene_id'] = str(uuid.uuid4())
#             scene_data['previous_choice'] = choice
            
#             return scene_data
#         except Exception as e:
#             print(f"Error generating scene: {str(e)}")
#             return self._generate_fallback_scene()

#     def generate_npc_dialogue(self, npc_context: Dict, player_state: Dict) -> str:
#         """Generate dynamic NPC dialogue"""
#         try:
#             self._wait_for_rate_limit()
            
#             dialogue_prompt = f"""
#             Generate dynamic dialogue for an NPC interaction:
#             NPC Context: {json.dumps(npc_context)}
#             Player State: {json.dumps(player_state)}
            
#             Create a natural conversation that reflects the NPC's personality and knowledge of the player's actions.
#             Include possible quest hints or story revelations based on player stats and history.

#             Format the response as:
#             {{
#                 "dialogue": "NPC's speech",
#                 "mood": "NPC's current mood",
#                 "quest_hints": ["list of hints"],
#                 "available_interactions": ["list of possible interactions"]
#             }}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-v3',
#                 body=json.dumps({
#                     "prompt": dialogue_prompt,
#                     "max_tokens": 300,
#                     "temperature": 0.8
#                 })
#             )
            
#             return json.loads(response['body'].read().decode())['completion']
#         except Exception as e:
#             print(f"Error generating dialogue: {str(e)}")
#             return self._generate_fallback_dialogue()

#     def generate_item_description(self, item_type: str, player_level: int) -> Dict:
#         """Generate a unique game item"""
#         try:
#             self._wait_for_rate_limit()
            
#             item_prompt = f"""
#             Generate a unique game item:
#             Type: {item_type}
#             Player Level: {player_level}
            
#             Create a detailed item description including:
#             - Name
#             - Description
#             - Rarity
#             - Effects
#             - Lore

#             Format the response as:
#             {{
#                 "name": "item name",
#                 "description": "item description",
#                 "rarity": "common/uncommon/rare/epic/legendary",
#                 "effects": {{
#                     "stat_modifications": {{}},
#                     "special_abilities": []
#                 }},
#                 "lore": "item backstory"
#             }}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-v3',
#                 body=json.dumps({
#                     "prompt": item_prompt,
#                     "max_tokens": 200,
#                     "temperature": 0.8
#                 })
#             )
            
#             return json.loads(response['body'].read().decode())['completion']
#         except Exception as e:
#             print(f"Error generating item: {str(e)}")
#             return self._generate_fallback_item(item_type, player_level)

#     def generate_combat_encounter(self, player_state: Dict) -> Dict:
#         """Generate a combat encounter"""
#         try:
#             self._wait_for_rate_limit()
            
#             combat_prompt = f"""
#             Generate a combat encounter for a player with these stats:
#             Player State: {json.dumps(player_state)}
            
#             Create an engaging combat scenario including:
#             - Enemy description
#             - Combat options
#             - Potential rewards
#             - Escape routes

#             Format the response as:
#             {{
#                 "enemy": {{
#                     "name": "enemy name",
#                     "description": "enemy description",
#                     "stats": {{
#                         "health": 100,
#                         "attack": 10,
#                         "defense": 5
#                     }}
#                 }},
#                 "combat_options": [
#                     {{
#                         "action": "action description",
#                         "requirements": {{}},
#                         "effects": {{}}
#                     }}
#                 ],
#                 "rewards": {{
#                     "experience": 0,
#                     "items": []
#                 }},
#                 "escape_options": []
#             }}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-v3',
#                 body=json.dumps({
#                     "prompt": combat_prompt,
#                     "max_tokens": 500,
#                     "temperature": 0.7
#                 })
#             )
            
#             return json.loads(response['body'].read().decode())['completion']
#         except Exception as e:
#             print(f"Error generating combat: {str(e)}")
#             return self._generate_fallback_combat()

#     def _generate_fallback_scene(self) -> Dict:
#         """Generate a fallback scene when main generation fails"""
#         return {
#             "scene_description": "You find yourself in a mysterious area. The path ahead seems unclear, but you must press forward.",
#             "choices": [
#                 {
#                     "text": "Continue exploring carefully",
#                     "consequences": {
#                         "health": 0,
#                         "magic": 0,
#                         "technology": 0,
#                         "charisma": 0,
#                         "items": [],
#                         "story_flags": []
#                     }
#                 }
#             ],
#             "environment": {
#                 "items": [],
#                 "npcs": [],
#                 "events": []
#             },
#             "scene_id": str(uuid.uuid4()),
#             "timestamp": datetime.utcnow().isoformat()
#         }

#     def _generate_fallback_dialogue(self) -> Dict:
#         """Generate fallback NPC dialogue"""
#         return {
#             "dialogue": "The character nods silently, seeming lost in thought.",
#             "mood": "neutral",
#             "quest_hints": [],
#             "available_interactions": ["Leave the conversation"]
#         }

#     def _generate_fallback_item(self, item_type: str, player_level: int) -> Dict:
#         """Generate a fallback item"""
#         return {
#             "name": f"Mysterious {item_type.title()}",
#             "description": "An enigmatic item whose true nature remains unclear.",
#             "rarity": "common",
#             "effects": {
#                 "stat_modifications": {},
#                 "special_abilities": []
#             },
#             "lore": "This item's history is shrouded in mystery."
#         }

#     def _generate_fallback_combat(self) -> Dict:
#         """Generate a fallback combat encounter"""
#         return {
#             "enemy": {
#                 "name": "Shadow Entity",
#                 "description": "A mysterious presence that's difficult to discern.",
#                 "stats": {
#                     "health": 50,
#                     "attack": 5,
#                     "defense": 3
#                 }
#             },
#             "combat_options": [
#                 {
#                     "action": "Attack",
#                     "requirements": {},
#                     "effects": {"damage": 5}
#                 }
#             ],
#             "rewards": {
#                 "experience": 10,
#                 "items": []
#             },
#             "escape_options": ["Retreat"]
#         }

# import json
# import boto3
# import uuid
# from typing import Dict, List, Optional
# from datetime import datetime, timedelta
# from time import sleep

# class StoryGenerator:
#     def __init__(self):
#         self.bedrock = boto3.client('bedrock-runtime')
#         self.last_request_time = datetime.now()
#         self.min_request_interval = timedelta(seconds=1)
        
#         # Game world context
#         self.game_context = {
#             "world_setting": "A mystical realm where magic and technology coexist",
#             "player_attributes": ["health", "magic", "technology", "charisma"],
#             "item_types": ["weapons", "spells", "gadgets", "artifacts"],
#             "enemy_types": ["magical creatures", "rogue AI", "corrupted beings", "ancient guardians"],
#             "locations": [
#                 "Crystal Spire City",
#                 "Neon Forest",
#                 "Quantum Ruins",
#                 "Tech-Mage Academy",
#                 "Digital Bazaar"
#             ],
#             "factions": [
#                 "Tech-Mages Alliance",
#                 "Digital Druids",
#                 "Quantum Knights",
#                 "Circuit Sages",
#                 "Binary Bandits"
#             ]
#         }

#     def _wait_for_rate_limit(self):
#         """Implement rate limiting for Bedrock API calls"""
#         time_since_last = datetime.now() - self.last_request_time
#         if time_since_last < self.min_request_interval:
#             sleep((self.min_request_interval - time_since_last).total_seconds())
#         self.last_request_time = datetime.now()

#     def generate_story_prompt(self, current_scene: Dict, player_state: Dict, choice: Optional[str] = None) -> str:
#         """Generate prompt for story continuation"""
#         prompt = f"""
#         You are a master storyteller creating an interactive adventure game in a world where magic and technology coexist.
#         Generate the next scene based on:

#         Current Scene: {current_scene.get('description', 'Starting adventure')}
#         Player's Choice: {choice if choice else 'Starting game'}
#         Player Stats: {json.dumps(player_state)}
        
#         World Context: {json.dumps(self.game_context)}

#         Generate a JSON response with:
#         1. A vivid scene description (2-3 paragraphs)
#         2. Three distinct choices that meaningfully impact the story
#         3. Potential consequences for each choice (affecting player stats)
#         4. Any items or discoveries in the scene
#         5. Random events or encounters (20% chance)

#         Format the response as shown in this example:
#         {{
#             "scene_description": "detailed description",
#             "choices": [
#                 {{
#                     "text": "choice description",
#                     "consequences": {{
#                         "health": 0,
#                         "magic": 0,
#                         "technology": 0,
#                         "charisma": 0,
#                         "items": [],
#                         "story_flags": []
#                     }}
#                 }}
#             ],
#             "environment": {{
#                 "items": [],
#                 "npcs": [],
#                 "events": []
#             }}
#         }}
#         """
#         return prompt

#     def generate_scene(self, current_scene: Dict, player_state: Dict, choice: Optional[str] = None) -> Dict:
#         """Generate a new scene based on player's current state and choices"""
#         try:
#             self._wait_for_rate_limit()
#             prompt = self.generate_story_prompt(current_scene, player_state, choice)
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "prompt": prompt,
#                     "max_tokens": 1000,
#                     "temperature": 0.7,
#                     "top_p": 0.9
#                 })
#             )
            
#             story_response = json.loads(response['body'].read().decode())
#             scene_data = json.loads(story_response['completion'])
            
#             # Add metadata for game mechanics
#             scene_data['timestamp'] = datetime.utcnow().isoformat()
#             scene_data['scene_id'] = str(uuid.uuid4())
#             scene_data['previous_choice'] = choice
            
#             return scene_data
#         except Exception as e:
#             print(f"Error generating scene: {str(e)}")
#             return self._generate_fallback_scene()

#     def generate_npc_dialogue(self, npc_context: Dict, player_state: Dict) -> str:
#         """Generate dynamic NPC dialogue"""
#         try:
#             self._wait_for_rate_limit()
            
#             dialogue_prompt = f"""
#             Generate dynamic dialogue for an NPC interaction:
#             NPC Context: {json.dumps(npc_context)}
#             Player State: {json.dumps(player_state)}
            
#             Create a natural conversation that reflects the NPC's personality and knowledge of the player's actions.
#             Include possible quest hints or story revelations based on player stats and history.

#             Format the response as shown in this example:
#             {{
#                 "dialogue": "NPC's speech",
#                 "mood": "NPC's current mood",
#                 "quest_hints": ["list of hints"],
#                 "available_interactions": ["list of possible interactions"]
#             }}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "prompt": dialogue_prompt,
#                     "max_tokens": 300,
#                     "temperature": 0.8
#                 })
#             )
            
#             return json.loads(response['body'].read().decode())['completion']
#         except Exception as e:
#             print(f"Error generating dialogue: {str(e)}")
#             return self._generate_fallback_dialogue()

#     def generate_item_description(self, item_type: str, player_level: int) -> Dict:
#         """Generate a unique game item"""
#         try:
#             self._wait_for_rate_limit()
            
#             item_prompt = f"""
#             Generate a unique game item:
#             Type: {item_type}
#             Player Level: {player_level}
            
#             Create a detailed item description including:
#             - Name
#             - Description
#             - Rarity
#             - Effects
#             - Lore

#             Format the response as shown in this example:
#             {{
#                 "name": "item name",
#                 "description": "item description",
#                 "rarity": "common/uncommon/rare/epic/legendary",
#                 "effects": {{
#                     "stat_modifications": {{}},
#                     "special_abilities": []
#                 }},
#                 "lore": "item backstory"
#             }}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "prompt": item_prompt,
#                     "max_tokens": 200,
#                     "temperature": 0.8
#                 })
#             )
            
#             return json.loads(response['body'].read().decode())['completion']
#         except Exception as e:
#             print(f"Error generating item: {str(e)}")
#             return self._generate_fallback_item(item_type, player_level)

#     def generate_combat_encounter(self, player_state: Dict) -> Dict:
#         """Generate a combat encounter"""
#         try:
#             self._wait_for_rate_limit()
            
#             combat_prompt = f"""
#             Generate a combat encounter for a player with these stats:
#             Player State: {json.dumps(player_state)}
            
#             Create an engaging combat scenario including:
#             - Enemy description
#             - Combat options
#             - Potential rewards
#             - Escape routes

#             Format the response as shown in this example:
#             {{
#                 "enemy": {{
#                     "name": "enemy name",
#                     "description": "enemy description",
#                     "stats": {{
#                         "health": 100,
#                         "attack": 10,
#                         "defense": 5
#                     }}
#                 }},
#                 "combat_options": [
#                     {{
#                         "action": "action description",
#                         "requirements": {{}},
#                         "effects": {{}}
#                     }}
#                 ],
#                 "rewards": {{
#                     "experience": 0,
#                     "items": []
#                 }},
#                 "escape_options": [""]
#             }}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "prompt": combat_prompt,
#                     "max_tokens": 500,
#                     "temperature": 0.7
#                 })
#             )
            
#             return json.loads(response['body'].read().decode())['completion']
#         except Exception as e:
#             print(f"Error generating combat: {str(e)}")
#             return self._generate_fallback_combat()

#     def _generate_fallback_scene(self) -> Dict:
#         """Generate a fallback scene when main generation fails"""
#         return {
#             "scene_description": "You find yourself in a mysterious area. The path ahead seems unclear, but you must press forward.",
#             "choices": [
#                 {
#                     "text": "Continue exploring carefully",
#                     "consequences": {
#                         "health": 0,
#                         "magic": 0,
#                         "technology": 0,
#                         "charisma": 0,
#                         "items": [],
#                         "story_flags": []
#                     }
#                 }
#             ],
#             "environment": {
#                 "items": [],
#                 "npcs": [],
#                 "events": []
#             },
#             "scene_id": str(uuid.uuid4()),
#             "timestamp": datetime.utcnow().isoformat()
#         }

#     def _generate_fallback_dialogue(self) -> Dict:
#         """Generate fallback NPC dialogue"""
#         return {
#             "dialogue": "The character nods silently, seeming lost in thought.",
#             "mood": "neutral",
#             "quest_hints": [],
#             "available_interactions": ["Leave the conversation"]
#         }

#     def _generate_fallback_item(self, item_type: str, player_level: int) -> Dict:
#         """Generate a fallback item"""
#         return {
#             "name": f"Mysterious {item_type.title()}",
#             "description": "An enigmatic item whose true nature remains unclear.",
#             "rarity": "common",
#             "effects": {
#                 "stat_modifications": {},
#                 "special_abilities": []
#             },
#             "lore": "This item's history is shrouded in mystery."
#         }

#     def _generate_fallback_combat(self) -> Dict:
#         """Generate a fallback combat encounter"""
#         return {
#             "enemy": {
#                 "name": "Shadow Entity",
#                 "description": "A mysterious presence that's difficult to discern.",
#                 "stats": {
#                     "health": 50,
#                     "attack": 5,
#                     "defense": 3
#                 }
#             },
#             "combat_options": [
#                 {
#                     "action": "Attack",
#                     "requirements": {},
#                     "effects": {"damage": 5}
#                 }
#             ],
#             "rewards": {
#                 "experience": 10,
#                 "items": []
#             },
#             "escape_options": ["Retreat"]
#         }

import json
import boto3
import uuid
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from time import sleep
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)

class StoryGenerator:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.last_request_time = datetime.now()
        self.min_request_interval = timedelta(seconds=1)
        
        self.game_context = {
            "world_setting": "A mystical realm where magic and technology coexist",
            "player_attributes": ["health", "magic", "technology", "charisma"],
            "item_types": ["weapons", "spells", "gadgets", "artifacts"],
            "enemy_types": ["magical creatures", "rogue AI", "corrupted beings", "ancient guardians"],
            "locations": [
                "Crystal Spire City",
                "Neon Forest",
                "Quantum Ruins",
                "Tech-Mage Academy",
                "Digital Bazaar"
            ],
            "factions": [
                "Tech-Mages Alliance",
                "Digital Druids",
                "Quantum Knights",
                "Circuit Sages",
                "Binary Bandits"
            ]
        }

    def _wait_for_rate_limit(self):
        """Implement rate limiting for Bedrock API calls"""
        time_since_last = datetime.now() - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep((self.min_request_interval - time_since_last).total_seconds())
        self.last_request_time = datetime.now()

    def generate_story_prompt(self, current_scene: Dict, player_state: Dict, choice: Optional[str] = None) -> str:
        """Generate prompt for story continuation"""
        prompt = f"""
        You are a master storyteller creating an interactive adventure game in a world where magic and technology coexist.
        Generate the next scene based on:

        Current Scene: {current_scene.get('description', 'Starting adventure')}
        Player's Choice: {choice if choice else 'Starting game'}
        Player Stats: {json.dumps(player_state, cls=DecimalEncoder)}
        
        World Context: {json.dumps(self.game_context, cls=DecimalEncoder)}

        Generate a JSON response with:
        1. A vivid scene description (2-3 paragraphs)
        2. Three distinct choices that meaningfully impact the story
        3. Potential consequences for each choice (affecting player stats)
        4. Any items or discoveries in the scene
        5. Random events or encounters (20% chance)

        Format the response exactly like this example:
        {{
            "scene_description": "detailed description",
            "choices": [
                {{
                    "text": "choice description",
                    "consequences": {{
                        "health": 0,
                        "magic": 0,
                        "technology": 0,
                        "charisma": 0
                    }}
                }}
            ],
            "environment": {{
                "items": [],
                "npcs": [],
                "events": []
            }}
        }}
        
        Response must be valid JSON and follow this structure exactly. Make it engaging and meaningful to the story.
        """
        return prompt    

    def generate_scene(self, current_scene: Dict, player_state: Dict, choice: Optional[str] = None) -> Dict:
        """Generate a new scene based on player's current state and choices"""
        try:
            self._wait_for_rate_limit()
            prompt = self.generate_story_prompt(current_scene, player_state, choice)
            
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                }, cls=DecimalEncoder)
            )
            
            response_body = response['body'].read().decode()
            response_json = json.loads(response_body)
            
            # For debugging
            print(f"Raw response: {json.dumps(response_json)}")
            
            # Get the response content
            if isinstance(response_json, dict) and 'content' in response_json:
                content = response_json['content']
                if isinstance(content, list) and len(content) > 0:
                    text = content[0].get('text', '{}')
                    try:
                        scene_data = json.loads(text)
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse scene data: {str(e)}")
                        return self._generate_fallback_scene()
                else:
                    print("No content found in response")
                    return self._generate_fallback_scene()
            else:
                print("Unexpected response format")
                return self._generate_fallback_scene()
            
            # Add metadata
            scene_data['timestamp'] = datetime.utcnow().isoformat()
            scene_data['scene_id'] = str(uuid.uuid4())
            scene_data['previous_choice'] = choice
            
            return scene_data
        except Exception as e:
            print(f"Error generating scene: {str(e)}")
            import traceback
            print(f"Full error details: {traceback.format_exc()}")
            return self._generate_fallback_scene()

    def generate_npc_dialogue(self, npc_context: Dict, player_state: Dict) -> str:
        """Generate dynamic NPC dialogue"""
        try:
            self._wait_for_rate_limit()
            dialogue_prompt = f"""
            Generate dynamic dialogue for an NPC interaction:
            NPC Context: {json.dumps(npc_context, cls=DecimalEncoder)}
            Player State: {json.dumps(player_state, cls=DecimalEncoder)}
            
            Create a natural conversation that reflects the NPC's personality and knowledge of the player's actions.
            Include possible quest hints or story revelations based on player stats and history.
            """
            
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": dialogue_prompt
                                }
                            ]
                        }
                    ]
                }, cls=DecimalEncoder)
            )
            
            response_body = response['body'].read().decode()
            dialogue_response = json.loads(response_body)
            return json.loads(dialogue_response.get('content', [{}])[0].get('text', '{}'))
        except Exception as e:
            print(f"Error generating dialogue: {str(e)}")
            return self._generate_fallback_dialogue()

    def generate_item_description(self, item_type: str, player_level: int) -> Dict:
        """Generate a unique game item"""
        try:
            self._wait_for_rate_limit()
            item_prompt = f"""
            Generate a unique game item:
            Type: {item_type}
            Player Level: {player_level}
            
            Create a detailed item description including:
            - Name
            - Description
            - Rarity
            - Effects
            - Lore
            """
            
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": item_prompt
                                }
                            ]
                        }
                    ]
                }, cls=DecimalEncoder)
            )
            
            response_body = response['body'].read().decode()
            item_response = json.loads(response_body)
            return json.loads(item_response.get('content', [{}])[0].get('text', '{}'))
        except Exception as e:
            print(f"Error generating item: {str(e)}")
            return self._generate_fallback_item(item_type, player_level)

    def generate_combat_encounter(self, player_state: Dict) -> Dict:
        """Generate a combat encounter"""
        try:
            self._wait_for_rate_limit()
            combat_prompt = f"""
            Generate a combat encounter for a player with these stats:
            Player State: {json.dumps(player_state, cls=DecimalEncoder)}
            """
            
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": combat_prompt
                                }
                            ]
                        }
                    ]
                }, cls=DecimalEncoder)
            )
            
            response_body = response['body'].read().decode()
            combat_response = json.loads(response_body)
            return json.loads(combat_response.get('content', [{}])[0].get('text', '{}'))
        except Exception as e:
            print(f"Error generating combat: {str(e)}")
            return self._generate_fallback_combat()

    # Fallback methods remain the same
    def _generate_fallback_scene(self) -> Dict:
        """Generate a fallback scene when main generation fails"""
        return {
            "scene_description": "You find yourself in a mysterious area. The path ahead seems unclear, but you must press forward.",
            "choices": [
                {
                    "text": "Continue exploring carefully",
                    "consequences": {
                        "health": 0,
                        "magic": 0,
                        "technology": 0,
                        "charisma": 0,
                        "items": [],
                        "story_flags": []
                    }
                }
            ],
            "environment": {
                "items": [],
                "npcs": [],
                "events": []
            },
            "scene_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }

    def _generate_fallback_dialogue(self) -> Dict:
        """Generate fallback NPC dialogue"""
        return {
            "dialogue": "The character nods silently, seeming lost in thought.",
            "mood": "neutral",
            "quest_hints": [],
            "available_interactions": ["Leave the conversation"]
        }

    def _generate_fallback_item(self, item_type: str, player_level: int) -> Dict:
        """Generate a fallback item"""
        return {
            "name": f"Mysterious {item_type.title()}",
            "description": "An enigmatic item whose true nature remains unclear.",
            "rarity": "common",
            "effects": {
                "stat_modifications": {},
                "special_abilities": []
            },
            "lore": "This item's history is shrouded in mystery."
        }

    def _generate_fallback_combat(self) -> Dict:
        """Generate a fallback combat encounter"""
        return {
            "enemy": {
                "name": "Shadow Entity",
                "description": "A mysterious presence that's difficult to discern.",
                "stats": {
                    "health": 50,
                    "attack": 5,
                    "defense": 3
                }
            },
            "combat_options": [
                {
                    "action": "Attack",
                    "requirements": {},
                    "effects": {"damage": 5}
                }
            ],
            "rewards": {
                "experience": 10,
                "items": []
            },
            "escape_options": ["Retreat"]
        }