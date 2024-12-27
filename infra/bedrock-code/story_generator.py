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

# import json
# import boto3
# import uuid
# from typing import Dict, List, Optional
# from datetime import datetime, timedelta
# from time import sleep
# from decimal import Decimal

# class DecimalEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Decimal):
#             return float(obj)
#         if isinstance(obj, datetime):
#             return obj.isoformat()
#         return super(DecimalEncoder, self).default(obj)

# class StoryGenerator:
#     def __init__(self):
#         self.bedrock = boto3.client('bedrock-runtime')
#         self.last_request_time = datetime.now()
#         self.min_request_interval = timedelta(seconds=1)
        
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
#         Player Stats: {json.dumps(player_state, cls=DecimalEncoder)}
        
#         World Context: {json.dumps(self.game_context, cls=DecimalEncoder)}

#         Generate a JSON response with:
#         1. A vivid scene description (2-3 paragraphs)
#         2. Three distinct choices that meaningfully impact the story
#         3. Potential consequences for each choice (affecting player stats)
#         4. Any items or discoveries in the scene
#         5. Random events or encounters (20% chance)

#         Format the response exactly like this example:
#         {{
#             "scene_description": "detailed description",
#             "choices": [
#                 {{
#                     "text": "choice description",
#                     "consequences": {{
#                         "health": 0,
#                         "magic": 0,
#                         "technology": 0,
#                         "charisma": 0
#                     }}
#                 }}
#             ],
#             "environment": {{
#                 "items": [],
#                 "npcs": [],
#                 "events": []
#             }}
#         }}
        
#         Response must be valid JSON and follow this structure exactly. Make it engaging and meaningful to the story.
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
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 1000,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             response_json = json.loads(response_body)
            
#             # For debugging
#             print(f"Raw response: {json.dumps(response_json)}")
            
#             # Get the response content
#             if isinstance(response_json, dict) and 'content' in response_json:
#                 content = response_json['content']
#                 if isinstance(content, list) and len(content) > 0:
#                     text = content[0].get('text', '{}')
#                     try:
#                         scene_data = json.loads(text)
#                     except json.JSONDecodeError as e:
#                         print(f"Failed to parse scene data: {str(e)}")
#                         return self._generate_fallback_scene()
#                 else:
#                     print("No content found in response")
#                     return self._generate_fallback_scene()
#             else:
#                 print("Unexpected response format")
#                 return self._generate_fallback_scene()
            
#             # Add metadata
#             scene_data['timestamp'] = datetime.utcnow().isoformat()
#             scene_data['scene_id'] = str(uuid.uuid4())
#             scene_data['previous_choice'] = choice
            
#             return scene_data
#         except Exception as e:
#             print(f"Error generating scene: {str(e)}")
#             import traceback
#             print(f"Full error details: {traceback.format_exc()}")
#             return self._generate_fallback_scene()

#     def generate_npc_dialogue(self, npc_context: Dict, player_state: Dict) -> str:
#         """Generate dynamic NPC dialogue"""
#         try:
#             self._wait_for_rate_limit()
#             dialogue_prompt = f"""
#             Generate dynamic dialogue for an NPC interaction:
#             NPC Context: {json.dumps(npc_context, cls=DecimalEncoder)}
#             Player State: {json.dumps(player_state, cls=DecimalEncoder)}
            
#             Create a natural conversation that reflects the NPC's personality and knowledge of the player's actions.
#             Include possible quest hints or story revelations based on player stats and history.
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 300,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": dialogue_prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             dialogue_response = json.loads(response_body)
#             return json.loads(dialogue_response.get('content', [{}])[0].get('text', '{}'))
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
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 300,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": item_prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             item_response = json.loads(response_body)
#             return json.loads(item_response.get('content', [{}])[0].get('text', '{}'))
#         except Exception as e:
#             print(f"Error generating item: {str(e)}")
#             return self._generate_fallback_item(item_type, player_level)

#     def generate_combat_encounter(self, player_state: Dict) -> Dict:
#         """Generate a combat encounter"""
#         try:
#             self._wait_for_rate_limit()
#             combat_prompt = f"""
#             Generate a combat encounter for a player with these stats:
#             Player State: {json.dumps(player_state, cls=DecimalEncoder)}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 500,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": combat_prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             combat_response = json.loads(response_body)
#             return json.loads(combat_response.get('content', [{}])[0].get('text', '{}'))
#         except Exception as e:
#             print(f"Error generating combat: {str(e)}")
#             return self._generate_fallback_combat()

#     # Fallback methods remain the same
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
# from typing import Dict, List, Optional, Union
# from datetime import datetime, timedelta
# from time import sleep
# from decimal import Decimal

# class DecimalEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Decimal):
#             return float(obj)
#         if isinstance(obj, datetime):
#             return obj.isoformat()
#         return super(DecimalEncoder, self).default(obj)

# class StoryGenerator:
#     def __init__(self):
#         self.bedrock = boto3.client('bedrock-runtime')
#         self.last_request_time = datetime.now()
#         self.min_request_interval = timedelta(seconds=1)
        
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

#     def _validate_player_state(self, player_state: Optional[Dict]) -> Dict:
#         """Validate and return a proper player state dictionary"""
#         default_state = {
#             "health": 100,
#             "magic": 50,
#             "technology": 50,
#             "charisma": 50
#         }
        
#         if not isinstance(player_state, dict):
#             return default_state
            
#         # Ensure all required stats are present
#         for stat in default_state.keys():
#             if stat not in player_state:
#                 player_state[stat] = default_state[stat]
                
#         return player_state

#     def _validate_scene(self, scene: Union[Dict, str, None]) -> Dict:
#         """Validate and return a proper scene dictionary"""
#         if isinstance(scene, str):
#             return {"description": scene}
#         elif scene is None:
#             return {"description": "Starting adventure"}
#         elif isinstance(scene, dict):
#             if "description" not in scene:
#                 scene["description"] = "Continuing the adventure"
#             return scene
#         else:
#             return {"description": "Starting adventure"}

#     def generate_story_prompt(self, current_scene: Union[Dict, str, None], player_state: Dict, choice: Optional[str] = None) -> str:
#         """Generate prompt for story continuation"""
#         # Validate inputs
#         current_scene = self._validate_scene(current_scene)
#         player_state = self._validate_player_state(player_state)
        
#         prompt = f"""
#         You are a master storyteller creating an interactive adventure game in a world where magic and technology coexist.
#         Generate the next scene based on:

#         Current Scene: {current_scene.get('description', 'Starting adventure')}
#         Player's Choice: {choice if choice else 'Starting game'}
#         Player Stats: {json.dumps(player_state, cls=DecimalEncoder)}
        
#         World Context: {json.dumps(self.game_context, cls=DecimalEncoder)}

#         Generate a JSON response with:
#         1. A vivid scene description (2-3 paragraphs)
#         2. Three distinct choices that meaningfully impact the story
#         3. Potential consequences for each choice (affecting player stats)
#         4. Any items or discoveries in the scene
#         5. Random events or encounters (20% chance)

#         Format the response exactly like this example:
#         {{
#             "scene_description": "detailed description",
#             "choices": [
#                 {{
#                     "text": "choice description",
#                     "consequences": {{
#                         "health": 0,
#                         "magic": 0,
#                         "technology": 0,
#                         "charisma": 0
#                     }}
#                 }}
#             ],
#             "environment": {{
#                 "items": [],
#                 "npcs": [],
#                 "events": []
#             }}
#         }}
        
#         Response must be valid JSON and follow this structure exactly. Make it engaging and meaningful to the story.
#         """
#         return prompt

#     def generate_scene(self, current_scene: Union[Dict, str, None], player_state: Dict, choice: Optional[str] = None) -> Dict:
#         """Generate a new scene based on player's current state and choices"""
#         try:
#             # Validate inputs
#             current_scene = self._validate_scene(current_scene)
#             player_state = self._validate_player_state(player_state)
            
#             self._wait_for_rate_limit()
#             prompt = self.generate_story_prompt(current_scene, player_state, choice)
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 1000,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             response_json = json.loads(response_body)
            
#             # For debugging
#             print(f"Raw response: {json.dumps(response_json)}")
            
#             # Get the response content
#             if isinstance(response_json, dict) and 'content' in response_json:
#                 content = response_json['content']
#                 if isinstance(content, list) and len(content) > 0:
#                     text = content[0].get('text', '{}')
#                     try:
#                         scene_data = json.loads(text)
#                     except json.JSONDecodeError as e:
#                         print(f"Failed to parse scene data: {str(e)}")
#                         return self._generate_fallback_scene()
#                 else:
#                     print("No content found in response")
#                     return self._generate_fallback_scene()
#             else:
#                 print("Unexpected response format")
#                 return self._generate_fallback_scene()
            
#             # Add metadata
#             scene_data['timestamp'] = datetime.utcnow().isoformat()
#             scene_data['scene_id'] = str(uuid.uuid4())
#             scene_data['previous_choice'] = choice
            
#             return scene_data
#         except Exception as e:
#             print(f"Error generating scene: {str(e)}")
#             import traceback
#             print(f"Full error details: {traceback.format_exc()}")
#             return self._generate_fallback_scene()

#     def generate_npc_dialogue(self, npc_context: Dict, player_state: Dict) -> str:
#         """Generate dynamic NPC dialogue"""
#         try:
#             self._wait_for_rate_limit()
#             dialogue_prompt = f"""
#             Generate dynamic dialogue for an NPC interaction:
#             NPC Context: {json.dumps(npc_context, cls=DecimalEncoder)}
#             Player State: {json.dumps(player_state, cls=DecimalEncoder)}
            
#             Create a natural conversation that reflects the NPC's personality and knowledge of the player's actions.
#             Include possible quest hints or story revelations based on player stats and history.
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 300,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": dialogue_prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             dialogue_response = json.loads(response_body)
#             return json.loads(dialogue_response.get('content', [{}])[0].get('text', '{}'))
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
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 300,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": item_prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             item_response = json.loads(response_body)
#             return json.loads(item_response.get('content', [{}])[0].get('text', '{}'))
#         except Exception as e:
#             print(f"Error generating item: {str(e)}")
#             return self._generate_fallback_item(item_type, player_level)

#     def generate_combat_encounter(self, player_state: Dict) -> Dict:
#         """Generate a combat encounter"""
#         try:
#             self._wait_for_rate_limit()
#             combat_prompt = f"""
#             Generate a combat encounter for a player with these stats:
#             Player State: {json.dumps(player_state, cls=DecimalEncoder)}
#             """
            
#             response = self.bedrock.invoke_model(
#                 modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                 body=json.dumps({
#                     "anthropic_version": "bedrock-2023-05-31",
#                     "max_tokens": 500,
#                     "messages": [
#                         {
#                             "role": "user",
#                             "content": [
#                                 {
#                                     "type": "text",
#                                     "text": combat_prompt
#                                 }
#                             ]
#                         }
#                     ]
#                 }, cls=DecimalEncoder)
#             )
            
#             response_body = response['body'].read().decode()
#             combat_response = json.loads(response_body)
#             return json.loads(combat_response.get('content', [{}])[0].get('text', '{}'))
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
# from typing import Dict, List, Optional, Union
# from datetime import datetime, timedelta
# from time import sleep
# from decimal import Decimal

# class DecimalEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Decimal):
#             return float(obj)
#         if isinstance(obj, datetime):
#             return obj.isoformat()
#         return super(DecimalEncoder, self).default(obj)

# class StoryGenerator:
#     def __init__(self):
#         self.bedrock = boto3.client('bedrock-runtime')
#         self.last_request_time = datetime.now()
#         self.min_request_interval = timedelta(seconds=1)
#         self.MAX_RETRIES = 3
#         self.BASE_DELAY = 2  # seconds
        
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
#         """Implement rate limiting for Bedrock API calls with exponential backoff"""
#         retry_count = 0
        
#         while retry_count < self.MAX_RETRIES:
#             time_since_last = datetime.now() - self.last_request_time
#             if time_since_last >= self.min_request_interval:
#                 self.last_request_time = datetime.now()
#                 return
                
#             delay = self.BASE_DELAY * (2 ** retry_count)  # Exponential backoff
#             print(f"Rate limit hit. Waiting {delay} seconds...")
#             sleep(delay)
#             retry_count += 1
            
#         raise Exception("Rate limit retry count exceeded")

#     def _bedrock_invoke_with_retry(self, prompt: str, max_tokens: int = 1000) -> dict:
#         """Helper method to invoke Bedrock with retry logic"""
#         retry_count = 0
#         while retry_count < self.MAX_RETRIES:
#             try:
#                 self._wait_for_rate_limit()
#                 response = self.bedrock.invoke_model(
#                     modelId='anthropic.claude-3-sonnet-20240229-v1:0',
#                     body=json.dumps({
#                         "anthropic_version": "bedrock-2023-05-31",
#                         "max_tokens": max_tokens,
#                         "messages": [
#                             {
#                                 "role": "user",
#                                 "content": [
#                                     {
#                                         "type": "text",
#                                         "text": prompt
#                                     }
#                                 ]
#                             }
#                         ]
#                     }, cls=DecimalEncoder)
#                 )
                
#                 response_body = response['body'].read().decode()
#                 return json.loads(response_body)
#             except self.bedrock.exceptions.ThrottlingException:
#                 retry_count += 1
#                 if retry_count >= self.MAX_RETRIES:
#                     print(f"Max retries ({self.MAX_RETRIES}) exceeded for Bedrock API call")
#                     raise
#                 delay = self.BASE_DELAY * (2 ** retry_count)
#                 print(f"Throttling occurred. Retrying in {delay} seconds...")
#                 sleep(delay)
#             except Exception as e:
#                 print(f"Unexpected error in Bedrock call: {str(e)}")
#                 raise

#     def _validate_player_state(self, player_state: Optional[Dict]) -> Dict:
#         """Validate and return a proper player state dictionary"""
#         default_state = {
#             "health": 100,
#             "magic": 50,
#             "technology": 50,
#             "charisma": 50
#         }
        
#         if not isinstance(player_state, dict):
#             return default_state
            
#         # Ensure all required stats are present
#         for stat in default_state.keys():
#             if stat not in player_state:
#                 player_state[stat] = default_state[stat]
                
#         return player_state

#     def _validate_scene(self, scene: Union[Dict, str, None]) -> Dict:
#         """Validate and return a proper scene dictionary"""
#         if isinstance(scene, str):
#             return {"description": scene}
#         elif scene is None:
#             return {"description": "Starting adventure"}
#         elif isinstance(scene, dict):
#             if "description" not in scene:
#                 scene["description"] = "Continuing the adventure"
#             return scene
#         else:
#             return {"description": "Starting adventure"}

#     def generate_story_prompt(self, current_scene: Union[Dict, str, None], player_state: Dict, choice: Optional[str] = None) -> str:
#         """Generate prompt for story continuation"""
#         # Validate inputs
#         current_scene = self._validate_scene(current_scene)
#         player_state = self._validate_player_state(player_state)
        
#         prompt = f"""
#         You are a master storyteller creating an interactive adventure game in a world where magic and technology coexist.
#         Generate the next scene based on:

#         Current Scene: {current_scene.get('description', 'Starting adventure')}
#         Player's Choice: {choice if choice else 'Starting game'}
#         Player Stats: {json.dumps(player_state, cls=DecimalEncoder)}
        
#         World Context: {json.dumps(self.game_context, cls=DecimalEncoder)}

#         Generate a JSON response with:
#         1. A vivid scene description (2-3 paragraphs)
#         2. Three distinct choices that meaningfully impact the story
#         3. Potential consequences for each choice (affecting player stats)
#         4. Any items or discoveries in the scene
#         5. Random events or encounters (20% chance)

#         Format the response exactly like this example:
#         {{
#             "scene_description": "detailed description",
#             "choices": [
#                 {{
#                     "text": "choice description",
#                     "consequences": {{
#                         "health": 0,
#                         "magic": 0,
#                         "technology": 0,
#                         "charisma": 0
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

#     def generate_scene(self, current_scene: Union[Dict, str, None], player_state: Dict, choice: Optional[str] = None) -> Dict:
#         """Generate a new scene based on player's current state and choices with retry logic"""
#         try:
#             # Validate inputs
#             current_scene = self._validate_scene(current_scene)
#             player_state = self._validate_player_state(player_state)
            
#             prompt = self.generate_story_prompt(current_scene, player_state, choice)
            
#             try:
#                 response_json = self._bedrock_invoke_with_retry(prompt)
                
#                 # Get the response content
#                 if isinstance(response_json, dict) and 'content' in response_json:
#                     content = response_json['content']
#                     if isinstance(content, list) and len(content) > 0:
#                         text = content[0].get('text', '{}')
#                         try:
#                             scene_data = json.loads(text)
#                         except json.JSONDecodeError as e:
#                             print(f"Failed to parse scene data: {str(e)}")
#                             return self._generate_fallback_scene()
#                     else:
#                         print("No content found in response")
#                         return self._generate_fallback_scene()
#                 else:
#                     print("Unexpected response format")
#                     return self._generate_fallback_scene()
                
#                 # Add metadata
#                 scene_data['timestamp'] = datetime.utcnow().isoformat()
#                 scene_data['scene_id'] = str(uuid.uuid4())
#                 scene_data['previous_choice'] = choice
                
#                 return scene_data
#             except Exception as e:
#                 print(f"Error in scene generation: {str(e)}")
#                 return self._generate_fallback_scene()
                
#         except Exception as e:
#             print(f"Error generating scene: {str(e)}")
#             import traceback
#             print(f"Full error details: {traceback.format_exc()}")
#             return self._generate_fallback_scene()

#     def generate_npc_dialogue(self, npc_context: Dict, player_state: Dict) -> str:
#         """Generate dynamic NPC dialogue with retry logic"""
#         try:
#             dialogue_prompt = f"""
#             Generate dynamic dialogue for an NPC interaction:
#             NPC Context: {json.dumps(npc_context, cls=DecimalEncoder)}
#             Player State: {json.dumps(player_state, cls=DecimalEncoder)}
            
#             Create a natural conversation that reflects the NPC's personality and knowledge of the player's actions.
#             Include possible quest hints or story revelations based on player stats and history.
#             """
            
#             response_json = self._bedrock_invoke_with_retry(dialogue_prompt, max_tokens=300)
#             return json.loads(response_json.get('content', [{}])[0].get('text', '{}'))
#         except Exception as e:
#             print(f"Error generating dialogue: {str(e)}")
#             return self._generate_fallback_dialogue()

#     def generate_item_description(self, item_type: str, player_level: int) -> Dict:
#         """Generate a unique game item with retry logic"""
#         try:
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
#             """
            
#             response_json = self._bedrock_invoke_with_retry(item_prompt, max_tokens=300)
#             return json.loads(response_json.get('content', [{}])[0].get('text', '{}'))
#         except Exception as e:
#             print(f"Error generating item: {str(e)}")
#             return self._generate_fallback_item(item_type, player_level)

#     def generate_combat_encounter(self, player_state: Dict) -> Dict:
#         """Generate a combat encounter with retry logic"""
#         try:
#             combat_prompt = f"""
#             Generate a combat encounter for a player with these stats:
#             Player State: {json.dumps(player_state, cls=DecimalEncoder)}
#             """
            
#             response_json = self._bedrock_invoke_with_retry(combat_prompt, max_tokens=500)
#             return json.loads(response_json.get('content', [{}])[0].get('text', '{}'))
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
import os
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
from time import sleep
from decimal import Decimal
import random
import hashlib

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
        self.dynamodb = boto3.resource('dynamodb')
        self.story_cache_table = self.dynamodb.Table(os.environ.get('STORY_CACHE_TABLE'))
        self.last_request_time = datetime.now()
        self.min_request_interval = timedelta(seconds=61)  # Strict 1-minute limit
        
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

    # Cache and Rate Limit Methods
    def _wait_for_rate_limit(self) -> bool:
        """Check if we can make an API call, returns True if we can proceed"""
        time_since_last = datetime.now() - self.last_request_time
        if time_since_last < self.min_request_interval:
            wait_time = (self.min_request_interval - time_since_last).total_seconds()
            print(f"Rate limit in effect. Need to wait {wait_time:.1f} seconds")
            return False
        return True

    def _get_cache_key(self, identifier: str, context: Optional[Dict] = None) -> str:
        """Generate a unique cache key"""
        key_parts = [identifier]
        if context:
            key_parts.append(json.dumps(context, sort_keys=True, cls=DecimalEncoder))
        return hashlib.md5('|'.join(key_parts).encode()).hexdigest()

    # def _get_from_cache(self, base_id: str, context_type: str = 'scene') -> Optional[List[Dict]]:
    #     """Try to get content from cache"""
    #     try:
    #         response = self.story_cache_table.query(
    #             KeyConditionExpression='base_id = :bid AND context_type = :type',
    #             ExpressionAttributeValues={
    #                 ':bid': base_id,
    #                 ':type': context_type
    #             }
    #         )
    #         items = response.get('Items', [])
    #         if items:
    #             print(f"Found {len(items)} cached {context_type}s")
    #             return items
    #         return None
    #     except Exception as e:
    #         print(f"Error retrieving from cache: {str(e)}")
    #         return None

    # def _store_in_cache(self, items: List[Dict], base_id: str, context_type: str = 'scene'):
    #     """Store content in cache"""
    #     try:
    #         expiry_time = int((datetime.utcnow() + timedelta(hours=24)).timestamp())
            
    #         with self.story_cache_table.batch_writer() as batch:
    #             for item in items:
    #                 cache_item = {
    #                     'base_id': base_id,
    #                     'context_type': context_type,
    #                     'content': item,
    #                     'expiry_time': expiry_time,
    #                     'timestamp': datetime.utcnow().isoformat(),
    #                     'cache_id': str(uuid.uuid4())
    #                 }
    #                 batch.put_item(Item=cache_item)
    #         print(f"Cached {len(items)} {context_type}s successfully")
    #     except Exception as e:
    #         print(f"Error storing in cache: {str(e)}")

    # def clean_old_cache(self):
    #     """Remove expired cache entries"""
    #     try:
    #         current_time = int(datetime.utcnow().timestamp())
            
    #         response = self.story_cache_table.scan(
    #             FilterExpression='expiry_time < :now',
    #             ExpressionAttributeValues={
    #                 ':now': current_time
    #             }
    #         )
            
    #         with self.story_cache_table.batch_writer() as batch:
    #             for item in response.get('Items', []):
    #                 batch.delete_item(
    #                     Key={
    #                         'base_id': item['base_id'],
    #                         'cache_id': item['cache_id']
    #                     }
    #                 )
            
    #         print(f"Cleared {len(response.get('Items', []))} expired cache entries")
    #     except Exception as e:
    #         print(f"Error clearing cache: {str(e)}")
    def _get_from_cache(self, base_scene_id: str, context_type: str = 'scene') -> Optional[List[Dict]]:
        """Try to get content from cache using GSI"""
        try:
            # Query using the GSI
            response = self.story_cache_table.query(
                IndexName='BaseSceneIndex',
                KeyConditionExpression='base_scene_id = :bid AND context_type = :type',
                ExpressionAttributeValues={
                    ':bid': base_scene_id,
                    ':type': context_type
                }
            )
            items = response.get('Items', [])
            if items:
                print(f"Found {len(items)} cached {context_type}s")
                return items
            return None
        except Exception as e:
            print(f"Error retrieving from cache: {str(e)}")
            return None

    def _store_in_cache(self, items: List[Dict], base_scene_id: str, context_type: str = 'scene'):
        """Store content in cache"""
        try:
            expiry_time = int((datetime.utcnow() + timedelta(hours=24)).timestamp())
            
            with self.story_cache_table.batch_writer() as batch:
                for item in items:
                    cache_item = {
                        'scene_id': str(uuid.uuid4()),  # Primary key
                        'context_type': context_type,   # Sort key
                        'base_scene_id': base_scene_id, # For GSI
                        'content': item,
                        'expiry_time': expiry_time,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    batch.put_item(Item=cache_item)
            print(f"Cached {len(items)} {context_type}s successfully")
        except Exception as e:
            print(f"Error storing in cache: {str(e)}")

    def clean_old_cache(self):
        """Remove expired cache entries"""
        try:
            current_time = int(datetime.utcnow().timestamp())
            
            response = self.story_cache_table.scan(
                FilterExpression='expiry_time < :now',
                ExpressionAttributeValues={
                    ':now': current_time
                }
            )
            
            with self.story_cache_table.batch_writer() as batch:
                for item in response.get('Items', []):
                    batch.delete_item(
                        Key={
                            'scene_id': item['scene_id'],
                            'context_type': item['context_type']
                        }
                    )
            
            print(f"Cleared {len(response.get('Items', []))} expired cache entries")
        except Exception as e:
            print(f"Error clearing cache: {str(e)}")

    def debug_cache_status(self, base_scene_id: str):
        """Debug method to check cache status"""
        try:
            response = self.story_cache_table.query(
                IndexName='BaseSceneIndex',
                KeyConditionExpression='base_scene_id = :bid',
                ExpressionAttributeValues={
                    ':bid': base_scene_id
                }
            )
            
            print(f"Cache query response for {base_scene_id}:")
            print(json.dumps(response, cls=DecimalEncoder, indent=2))
            
            return bool(response.get('Items'))
        except Exception as e:
            print(f"Error checking cache status: {str(e)}")
            return False        

    # API and Validation Methods
    def _bedrock_invoke_with_retry(self, prompt: str, max_tokens: int = 1000) -> dict:
        """Invoke Bedrock with rate limit check"""
        if not self._wait_for_rate_limit():
            raise Exception("Rate limit in effect")
            
        try:
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
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
            
            self.last_request_time = datetime.now()
            response_body = response['body'].read().decode()
            return json.loads(response_body)
        except Exception as e:
            print(f"Error in Bedrock call: {str(e)}")
            raise

    def _validate_player_state(self, player_state: Optional[Dict]) -> Dict:
        """Validate and return a proper player state dictionary"""
        default_state = {
            "health": 100,
            "magic": 50,
            "technology": 50,
            "charisma": 50
        }
        
        if not isinstance(player_state, dict):
            return default_state
            
        for stat in default_state.keys():
            if stat not in player_state:
                player_state[stat] = default_state[stat]
                
        return player_state

    def _validate_scene(self, scene: Union[Dict, str, None]) -> Dict:
        """Validate and return a proper scene dictionary"""
        if isinstance(scene, str):
            return {"description": scene}
        elif scene is None:
            return {"description": "Starting adventure"}
        elif isinstance(scene, dict):
            if "description" not in scene:
                scene["description"] = "Continuing the adventure"
            return scene
        else:
            return {"description": "Starting adventure"}

    # Fallback Methods
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

    # Main Generation Methods
    def generate_story_prompt(self, current_scene: Union[Dict, str, None], player_state: Dict, choice: Optional[str] = None) -> str:
        """Generate prompt for story continuation"""
        current_scene = self._validate_scene(current_scene)
        player_state = self._validate_player_state(player_state)
        
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
        """
        return prompt

    # def _generate_multiple_scenes(self, current_scene: Dict, player_state: Dict, variations: int = 5) -> List[Dict]:
    #     """Generate multiple scene variations in one API call"""
    #     prompt = f"""Generate {variations} different possible story continuations.
    #     {self.generate_story_prompt(current_scene, player_state)}
    #     Return an array of {variations} complete scenes."""

    #     try:
    #         response = self._bedrock_invoke_with_retry(prompt, max_tokens=2000)
    #         scenes = []
            
    #         if isinstance(response, dict) and 'content' in response:
    #             content = response['content']
    #             if isinstance(content, list) and len(content) > 0:
    #                 text = content[0].get('text', '[]')
    #                 try:
    #                     scenes = json.loads(text)
    #                     # Add metadata to each scene
    #                     for scene in scenes:
    #                         scene['scene_id'] = str(uuid.uuid4())
    #                         scene['timestamp'] = datetime.utcnow().isoformat()
    #                         if current_scene.get('scene_id'):
    #                             scene['previous_scene_id'] = current_scene['scene_id']
    #                 except json.JSONDecodeError as e:
    #                     print(f"Failed to parse scenes: {str(e)}")
            
    #         return scenes if scenes else []
    #     except Exception as e:
    #         print(f"Error generating multiple scenes: {str(e)}")
    #         return []

    def _generate_multiple_scenes(self, current_scene: Dict, player_state: Dict, variations: int = 5) -> List[Dict]:
        """Generate multiple scene variations in one API call"""
        # First check if we can make an API call
        if not self._wait_for_rate_limit():
            print("Rate limited in _generate_multiple_scenes")
            return []

        prompt = f"""Generate {variations} different possible story continuations.
        {self.generate_story_prompt(current_scene, player_state)}
        Return an array of {variations} complete scenes."""

        try:
            response = self._bedrock_invoke_with_retry(prompt, max_tokens=2000)
            scenes = []
            
            if isinstance(response, dict) and 'content' in response:
                content = response['content']
                if isinstance(content, list) and len(content) > 0:
                    text = content[0].get('text', '[]')
                    try:
                        scenes = json.loads(text)
                        # Add metadata to each scene
                        for scene in scenes:
                            scene['scene_id'] = str(uuid.uuid4())
                            scene['timestamp'] = datetime.utcnow().isoformat()
                            if current_scene.get('scene_id'):
                                scene['previous_scene_id'] = current_scene['scene_id']
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse scenes: {str(e)}")
            
            return scenes if scenes else []
        except Exception as e:
            print(f"Error generating multiple scenes: {str(e)}")
            return []

    def generate_scene(self, current_scene: Union[Dict, str, None], player_state: Dict, choice: Optional[str] = None) -> Dict:
        """Generate a new scene with caching and rate limiting"""
        try:
            current_scene = self._validate_scene(current_scene)
            player_state = self._validate_player_state(player_state)
            
            current_scene_id = current_scene.get('scene_id', 'initial')
            print(f"Generating scene for scene_id: {current_scene_id}")
            
            # Try to get from cache first
            cached_scenes = self._get_from_cache(current_scene_id, 'scene')
            if cached_scenes:
                print(f"Found {len(cached_scenes)} cached scenes")
                if choice:
                    # Try to find a scene matching the player's choice
                    matching_scenes = [s['content'] for s in cached_scenes 
                                    if any(c.get('text', '').lower() == choice.lower() 
                                        for c in s.get('content', {}).get('choices', []))]
                    if matching_scenes:
                        print("Found matching scene for choice")
                        return random.choice(matching_scenes)
                
                # If no matching choice or no choice provided, return random scene
                print("Returning random cached scene")
                return random.choice(cached_scenes)['content']
            
            print("No cached scenes found, generating new scenes")
            
            # Check rate limit before generating new scenes
            if not self._wait_for_rate_limit():
                print("Rate limited, returning fallback scene")
                return self._generate_fallback_scene()
            
            # Generate multiple scenes
            new_scenes = self._generate_multiple_scenes(current_scene, player_state)
            if new_scenes:
                # Store in cache
                print(f"Generated {len(new_scenes)} new scenes, storing in cache")
                self._store_in_cache(new_scenes, current_scene_id, 'scene')
                
                # Return appropriate scene
                if choice:
                    matching_scenes = [s for s in new_scenes 
                                    if any(c.get('text', '').lower() == choice.lower() 
                                        for c in s.get('choices', []))]
                    if matching_scenes:
                        print("Returning matching scene from new scenes")
                        return random.choice(matching_scenes)
                
                print("Returning random new scene")
                return random.choice(new_scenes)
            
            print("No scenes generated, returning fallback")
            return self._generate_fallback_scene()
                
        except Exception as e:
            print(f"Error in scene generation: {str(e)}")
            return self._generate_fallback_scene()

    def generate_scene(self, current_scene: Union[Dict, str, None], player_state: Dict, choice: Optional[str] = None) -> Dict:
            """Generate a new scene with caching and rate limiting"""
            try:
                current_scene = self._validate_scene(current_scene)
                player_state = self._validate_player_state(player_state)
                
                current_scene_id = current_scene.get('scene_id', 'initial')
                
                # Try to get from cache first
                cached_scenes = self._get_from_cache(current_scene_id, 'scene')
                if cached_scenes:
                    if choice:
                        # Try to find a scene matching the player's choice
                        matching_scenes = [s['content'] for s in cached_scenes 
                                        if any(c.get('text', '').lower() == choice.lower() 
                                            for c in s.get('content', {}).get('choices', []))]
                        if matching_scenes:
                            return random.choice(matching_scenes)
                    
                    # If no matching choice or no choice provided, return random scene
                    return random.choice(cached_scenes)['content']
                
                # Generate multiple scenes if we can make an API call
                try:
                    new_scenes = self._generate_multiple_scenes(current_scene, player_state)
                    if new_scenes:
                        # Store in cache and update last request time
                        self._store_in_cache(new_scenes, current_scene_id, 'scene')
                        
                        # Return appropriate scene
                        if choice:
                            matching_scenes = [s for s in new_scenes 
                                            if any(c.get('text', '').lower() == choice.lower() 
                                                for c in s.get('choices', []))]
                            if matching_scenes:
                                return random.choice(matching_scenes)
                        
                        return random.choice(new_scenes)
                except Exception as e:
                    print(f"Error generating scenes: {str(e)}")
                
                return self._generate_fallback_scene()
                
            except Exception as e:
                print(f"Error in scene generation: {str(e)}")
                return self._generate_fallback_scene()

    def generate_npc_dialogue(self, npc_context: Dict, player_state: Dict) -> Dict:
        """Generate NPC dialogue with caching"""
        try:
            cache_key = self._get_cache_key('npc', npc_context)
            
            
            # Check cache first
            cached_dialogues = self._get_from_cache(cache_key, 'dialogue')
            if cached_dialogues:
                return random.choice(cached_dialogues)['content']
            
            # Generate new dialogue if we can make an API call
            if self._wait_for_rate_limit():
                dialogue_prompt = f"""
                Generate multiple variations of dynamic dialogue for an NPC interaction.
                NPC Context: {json.dumps(npc_context, cls=DecimalEncoder)}
                Player State: {json.dumps(player_state, cls=DecimalEncoder)}
                
                Create 5 different versions of the conversation that:
                1. Reflect the NPC's personality and knowledge
                2. Include quest hints or story revelations
                3. Consider the player's current state and history
                4. Offer meaningful interaction choices
                
                Format each dialogue variation as a complete JSON object.
                Return an array of 5 dialogue variations.
                """
                
                response = self._bedrock_invoke_with_retry(dialogue_prompt, max_tokens=1000)
                if response and 'content' in response:
                    dialogues = json.loads(response['content'][0]['text'])
                    if dialogues:
                        self._store_in_cache(dialogues, cache_key, 'dialogue')
                        return random.choice(dialogues)
            
            return self._generate_fallback_dialogue()
        except Exception as e:
            print(f"Error generating dialogue: {str(e)}")
            return self._generate_fallback_dialogue()

    def generate_item_description(self, item_type: str, player_level: int) -> Dict:
        """Generate item description with caching"""
        try:
            cache_key = f"item_{item_type}_{player_level}"
            
            # Check cache first
            cached_items = self._get_from_cache(cache_key, 'item')
            if cached_items:
                return random.choice(cached_items)['content']
            
            # Generate new item if we can make an API call
            if self._wait_for_rate_limit():
                item_prompt = f"""
                Generate multiple unique game items:
                Type: {item_type}
                Player Level: {player_level}
                
                Create 5 different items, each with:
                - Unique name and description
                - Appropriate rarity for player level
                - Balanced effects and stats
                - Interesting lore or history
                - Special abilities or unique features
                
                Format each item as a complete JSON object.
                Return an array of 5 different items.
                """
                
                response = self._bedrock_invoke_with_retry(item_prompt, max_tokens=1000)
                if response and 'content' in response:
                    items = json.loads(response['content'][0]['text'])
                    if items:
                        self._store_in_cache(items, cache_key, 'item')
                        return random.choice(items)
            
            return self._generate_fallback_item(item_type, player_level)
        except Exception as e:
            print(f"Error generating item: {str(e)}")
            return self._generate_fallback_item(item_type, player_level)

    def generate_combat_encounter(self, player_state: Dict) -> Dict:
        """Generate combat encounter with caching"""
        try:
            cache_key = self._get_cache_key('combat', player_state)
            
            # Check cache first
            cached_encounters = self._get_from_cache(cache_key, 'combat')
            if cached_encounters:
                return random.choice(cached_encounters)['content']
            
            # Generate new encounter if we can make an API call
            if self._wait_for_rate_limit():
                combat_prompt = f"""
                Generate multiple combat encounters for a player with these stats:
                Player State: {json.dumps(player_state, cls=DecimalEncoder)}
                
                Create 5 different possible encounters, each including:
                1. Unique enemy or group of enemies with stats
                2. Combat options and special abilities
                3. Balanced rewards based on difficulty
                4. Multiple escape or alternative options
                5. Environmental factors or conditions
                
                Format each encounter as a complete JSON object.
                Return an array of 5 different encounters.
                """
                
                response = self._bedrock_invoke_with_retry(combat_prompt, max_tokens=1000)
                if response and 'content' in response:
                    encounters = json.loads(response['content'][0]['text'])
                    if encounters:
                        self._store_in_cache(encounters, cache_key, 'combat')
                        return random.choice(encounters)
            
            return self._generate_fallback_combat()
        except Exception as e:
            print(f"Error generating combat: {str(e)}")
            return self._generate_fallback_combat()    