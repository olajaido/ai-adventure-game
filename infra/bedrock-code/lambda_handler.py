
# import json
# import os
# import random
# from story_generator import StoryGenerator
# from game_data import GameState, PlayerState
# import boto3

# dynamodb = boto3.resource('dynamodb')
# game_table = dynamodb.Table(os.environ['GAME_TABLE'])

# def handle_game_action(event, context):
#     """Main handler for game actions"""
#     try:
#         body = json.loads(event['body'])
#         user_id = event['requestContext']['authorizer']['claims']['sub']
        
#         # Initialize game components
#         story_generator = StoryGenerator()
#         game_state = GameState()
#         player_state = load_player_state(user_id)
        
#         action_type = body.get('action', 'generate_scene')
        
#         if action_type == 'generate_scene':
#             current_scene = body.get('current_scene', {})
#             player_choice = body.get('player_choice')
            
#             # Generate new scene
#             scene_data = story_generator.generate_scene(
#                 current_scene,
#                 player_state.stats,
#                 player_choice
#             )
            
#             # Process any rewards or consequences
#             if player_choice and 'consequences' in current_scene:
#                 process_consequences(player_state, current_scene['consequences'])
            
#             # Add any new quests (20% chance)
#             if random.random() < 0.2:
#                 new_quest = game_state.generate_quest(
#                     'side_quest' if random.random() < 0.7 else 'main_quest',
#                     player_state.stats
#                 )
#                 player_state.add_quest(new_quest)
#                 scene_data['new_quest'] = new_quest
            
#             # Save updated player state
#             save_player_state(user_id, player_state)
            
#             return {
#                 'statusCode': 200,
#                 'body': json.dumps({
#                     'scene': scene_data,
#                     'player_state': player_state.stats,
#                     'quests': player_state.quest_log,
#                     'inventory': player_state.inventory
#                 }),
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 }
#             }
        
#         elif action_type == 'process_item':
#             item_id = body.get('item_id')
#             # Generate item description and effects
#             item_data = story_generator.generate_item_description(
#                 item_id,
#                 player_state.stats['level']
#             )
#             return {
#                 'statusCode': 200,
#                 'body': json.dumps(item_data),
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 }
#             }
        
#         elif action_type == 'npc_dialogue':
#             npc_context = body.get('npc_context', {})
#             dialogue = story_generator.generate_npc_dialogue(
#                 npc_context,
#                 player_state.stats
#             )
#             return {
#                 'statusCode': 200,
#                 'body': json.dumps({'dialogue': dialogue}),
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 }
#             }
        
#         elif action_type == 'complete_quest':
#             quest_id = body.get('quest_id')
#             rewards = body.get('rewards')
#             player_state.complete_quest(quest_id, rewards)
#             save_player_state(user_id, player_state)
#             return {
#                 'statusCode': 200,
#                 'body': json.dumps({
#                     'player_state': player_state.stats,
#                     'quests': player_state.quest_log,
#                     'inventory': player_state.inventory
#                 }),
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 }
#             }
            
#     except Exception as e:
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)}),
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             }
#         }

# def load_player_state(user_id: str) -> PlayerState:
#     """Load player state from DynamoDB"""
#     try:
#         response = game_table.get_item(
#             Key={'userId': user_id}
#         )
        
#         if 'Item' in response:
#             player_state = PlayerState(user_id)
#             player_state.stats = response['Item'].get('stats', player_state.stats)
#             player_state.inventory = response['Item'].get('inventory', [])
#             player_state.quest_log = response['Item'].get('quest_log', [])
#             player_state.story_flags = set(response['Item'].get('story_flags', []))
#             return player_state
        
#         return PlayerState(user_id)
#     except Exception as e:
#         print(f"Error loading player state: {str(e)}")
#         return PlayerState(user_id)

# def save_player_state(user_id: str, player_state: PlayerState):
#     """Save player state to DynamoDB"""
#     try:
#         game_table.put_item(
#             Item={
#                 'userId': user_id,
#                 'stats': player_state.stats,
#                 'inventory': player_state.inventory,
#                 'quest_log': player_state.quest_log,
#                 'story_flags': list(player_state.story_flags)
#             }
#         )
#     except Exception as e:
#         print(f"Error saving player state: {str(e)}")

# def process_consequences(player_state: PlayerState, consequences: Dict):
#     """Process the consequences of player choices"""
#     try:
#         # Update stats
#         player_state.update_stats(consequences.get('stats', {}))
        
#         # Add items
#         for item in consequences.get('items', []):
#             player_state.add_item(item)
        
#         # Add experience
#         if 'experience' in consequences:
#             player_state.add_experience(consequences['experience'])
        
#         # Add story flags
#         for flag in consequences.get('story_flags', []):
#             player_state.story_flags.add(flag)
#     except Exception as e:
#         print(f"Error processing consequences: {str(e)}")
              

import json
import os
from story_generator import StoryGenerator
from game_data import GameState, PlayerState
from content_manager import ContentManager
from player_analytics import PlayerAnalytics
import boto3

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table(os.environ['GAME_TABLE'])
content_manager = ContentManager('game_content.json')
analytics = PlayerAnalytics(os.environ['GAME_TABLE'])

def handle_game_action(event, context):
    """Main handler for game actions"""
    try:
        body = json.loads(event['body'])
        user_id = event['requestContext']['authorizer']['claims']['sub']
        
        # Initialize components
        story_generator = StoryGenerator()
        game_state = GameState()
        player_state = load_player_state(user_id)
        
        action_type = body.get('action', 'generate_scene')
        
        if action_type == 'generate_scene':
            current_scene = body.get('current_scene', {})
            player_choice = body.get('player_choice')
            
            # Track player choice if it exists
            if player_choice:
                analytics.track_choice(
                    user_id,
                    current_scene.get('scene_id', 'initial'),
                    player_choice,
                    current_scene.get('consequences', {})
                )
            
            # Generate new scene with enhanced content
            scene_data = story_generator.generate_scene(
                current_scene,
                player_state.stats,
                player_choice
            )
            
            # Add random event (20% chance)
            if random.random() < 0.2:
                scene_data['random_event'] = content_manager.generate_random_event()
            
            # Process consequences
            if player_choice and 'consequences' in current_scene:
                process_consequences(player_state, current_scene['consequences'])
            
            # Add new quest (20% chance)
            if random.random() < 0.2:
                new_quest = game_state.generate_quest(
                    'side_quest' if random.random() < 0.7 else 'main_quest',
                    player_state.stats
                )
                player_state.add_quest(new_quest)
                scene_data['new_quest'] = new_quest
            
            # Add NPC if appropriate
            if 'npc_interaction' in scene_data:
                npc_data = content_manager.generate_npc()
                scene_data['npc_data'] = npc_data
            
            # Save updated state
            save_player_state(user_id, player_state)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'scene': scene_data,
                    'player_state': player_state.stats,
                    'quests': player_state.quest_log,
                    'inventory': player_state.inventory
                }),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            
        elif action_type == 'complete_quest':
            quest_id = body.get('quest_id')
            quest_data = body.get('quest_data', {})
            
            # Track quest completion
            analytics.track_quest_completion(
                user_id,
                quest_id,
                quest_data.get('time_taken', 0)
            )
            
            # Process quest rewards
            process_quest_completion(player_state, quest_id, quest_data)
            save_player_state(user_id, player_state)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'player_state': player_state.stats,
                    'quests': player_state.quest_log,
                    'inventory': player_state.inventory
                }),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            
        elif action_type == 'get_player_analytics':
            # Get player preferences and stats
            preferences = analytics.get_player_preferences(user_id)
            return {
                'statusCode': 200,
                'body': json.dumps(preferences),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

def process_quest_completion(player_state: PlayerState, quest_id: str, quest_data: dict):
    """Process quest completion and rewards"""
    rewards = quest_data.get('rewards', {})
    player_state.complete_quest(quest_id, rewards)
    
    # Add any special rewards from content manager
    if random.random() < 0.3:  # 30% chance for special reward
        special_item = content_manager.generate_item('artifacts')
        player_state.add_item(special_item)