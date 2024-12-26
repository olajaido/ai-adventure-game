
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
              

# import json
# import os
# from story_generator import StoryGenerator
# from game_data import GameState, PlayerState
# from content_manager import ContentManager
# from player_analytics import PlayerAnalytics
# import boto3

# dynamodb = boto3.resource('dynamodb')
# game_table = dynamodb.Table(os.environ['GAME_TABLE'])
# content_manager = ContentManager('game_content.json')
# analytics = PlayerAnalytics(os.environ['GAME_TABLE'])

# def handle_game_action(event, context):
#     """Main handler for game actions"""
#     try:
#         body = json.loads(event['body'])
#         user_id = event['requestContext']['authorizer']['claims']['sub']
        
#         # Initialize components
#         story_generator = StoryGenerator()
#         game_state = GameState()
#         player_state = load_player_state(user_id)
        
#         action_type = body.get('action', 'generate_scene')
        
#         if action_type == 'generate_scene':
#             current_scene = body.get('current_scene', {})
#             player_choice = body.get('player_choice')
            
#             # Track player choice if it exists
#             if player_choice:
#                 analytics.track_choice(
#                     user_id,
#                     current_scene.get('scene_id', 'initial'),
#                     player_choice,
#                     current_scene.get('consequences', {})
#                 )
            
#             # Generate new scene with enhanced content
#             scene_data = story_generator.generate_scene(
#                 current_scene,
#                 player_state.stats,
#                 player_choice
#             )
            
#             # Add random event (20% chance)
#             if random.random() < 0.2:
#                 scene_data['random_event'] = content_manager.generate_random_event()
            
#             # Process consequences
#             if player_choice and 'consequences' in current_scene:
#                 process_consequences(player_state, current_scene['consequences'])
            
#             # Add new quest (20% chance)
#             if random.random() < 0.2:
#                 new_quest = game_state.generate_quest(
#                     'side_quest' if random.random() < 0.7 else 'main_quest',
#                     player_state.stats
#                 )
#                 player_state.add_quest(new_quest)
#                 scene_data['new_quest'] = new_quest
            
#             # Add NPC if appropriate
#             if 'npc_interaction' in scene_data:
#                 npc_data = content_manager.generate_npc()
#                 scene_data['npc_data'] = npc_data
            
#             # Save updated state
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
            
#         elif action_type == 'complete_quest':
#             quest_id = body.get('quest_id')
#             quest_data = body.get('quest_data', {})
            
#             # Track quest completion
#             analytics.track_quest_completion(
#                 user_id,
#                 quest_id,
#                 quest_data.get('time_taken', 0)
#             )
            
#             # Process quest rewards
#             process_quest_completion(player_state, quest_id, quest_data)
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
            
#         elif action_type == 'get_player_analytics':
#             # Get player preferences and stats
#             preferences = analytics.get_player_preferences(user_id)
#             return {
#                 'statusCode': 200,
#                 'body': json.dumps(preferences),
#                 'headers': {
#                     'Content-Type': 'application/json',
#                     'Access-Control-Allow-Origin': '*'
#                 }
#             }
            
#     except Exception as e:
#         print(f"Error processing request: {str(e)}")
#         return {
#             'statusCode': 500,
#             'body': json.dumps({'error': str(e)}),
#             'headers': {
#                 'Content-Type': 'application/json',
#                 'Access-Control-Allow-Origin': '*'
#             }
#         }

# def process_quest_completion(player_state: PlayerState, quest_id: str, quest_data: dict):
#     """Process quest completion and rewards"""
#     rewards = quest_data.get('rewards', {})
#     player_state.complete_quest(quest_id, rewards)
    
#     # Add any special rewards from content manager
#     if random.random() < 0.3:  # 30% chance for special reward
#         special_item = content_manager.generate_item('artifacts')
#         player_state.add_item(special_item)
import json
import os
import random
import jwt
import requests
from story_generator import StoryGenerator
from game_data import GameState, PlayerState
from content_manager import ContentManager
from player_analytics import PlayerAnalytics
import boto3

# Initialize AWS resources
dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table(os.environ['GAME_TABLE'])
content_manager = ContentManager('game_content.json')
analytics = PlayerAnalytics(os.environ['GAME_TABLE'])

cors_headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': 'https://dev.d18jzwlw8rkuyv.amplifyapp.com',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
    'Access-Control-Allow-Credentials': 'true'
}

from jose import jwk, jwt
from jose.utils import base64url_decode
import json
import requests

def verify_cognito_token(token):
    try:
        print("Starting token verification")
        # Your Cognito pool details
        USER_POOL_ID = 'eu-west-2_EcJ4nZ9ST'
        CLIENT_ID = '2se9lr8i6tolb0ud39u32mvtt9'
        REGION = 'eu-west-2'

        # Get the key id from the header
        headers = jwt.get_unverified_headers(token)
        kid = headers['kid']
        print(f"Token kid: {kid}")

        # Get the public keys from Cognito
        keys_url = f'https://cognito-idp.{REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json'
        print(f"Fetching public keys from: {keys_url}")
        response = requests.get(keys_url)
        keys = response.json()['keys']
        print(f"Keys response status: {response.status_code}")

        # Find the key matching the kid from the token
        key = next((k for k in keys if k['kid'] == kid), None)
        if not key:
            print("No matching key found")
            return None
        print("Found matching key")

        # Get the public key
        public_key = jwk.construct(key)
        print("Constructed public key")

        # Get message and signature (undecoded)
        message, encoded_signature = str(token).rsplit('.', 1)

        # Decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
        print("Decoded signature")

        # Verify the signature
        if not public_key.verify(message.encode(), decoded_signature):
            print("Signature verification failed")
            return None

        # Get claims using jose.jwt
        claims = jwt.get_unverified_claims(token)
        print("Token claims:", claims)
        return claims.get('sub')

    except Exception as e:
        print(f"Token verification failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None
def load_player_state(user_id: str) -> PlayerState:
    """Load player state from DynamoDB"""
    try:
        response = game_table.get_item(Key={'userId': user_id})
        if 'Item' in response:
            return PlayerState.from_dict(response['Item'])
        return PlayerState(user_id=user_id)
    except Exception as e:
        print(f"Error loading player state: {str(e)}")
        return PlayerState(user_id=user_id)

def save_player_state(user_id: str, player_state: PlayerState):
    """Save player state to DynamoDB"""
    try:
        game_table.put_item(Item=player_state.to_dict())
    except Exception as e:
        print(f"Error saving player state: {str(e)}")

def process_consequences(player_state: PlayerState, consequences: dict):
    """Process consequences of player choices"""
    for stat, change in consequences.items():
        if stat in player_state.stats:
            player_state.stats[stat] += change

def handle_game_action(event, context):
    """Main handler for game actions"""
    try:
        # Add event logging
        print("Received event:", json.dumps(event))
        
        # Extract and verify token - Fix case sensitivity issue
        auth_header = event.get('headers', {}).get('Authorization', event.get('headers', {}).get('authorization'))
        if not auth_header or not auth_header.startswith('Bearer '):
            print("Authorization header missing or invalid")
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'No valid token provided'}),
                'headers': cors_headers
            }

        # Print token for debugging
        print("Token received:", auth_header)
        
        token = auth_header.split(' ')[1]
        user_id = verify_cognito_token(token)
        print("User ID from token:", user_id)
        
        if not user_id:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Invalid token'}),
                'headers': cors_headers
            }

        # Parse request body
        body = event.get('body')
        if body:
            body = json.loads(body)
        else:
            body = {}
        
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
                'headers': cors_headers
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
                'headers': cors_headers
            }
            
        elif action_type == 'get_player_analytics':
            # Get player preferences and stats
            preferences = analytics.get_player_preferences(user_id)
            return {
                'statusCode': 200,
                'body': json.dumps(preferences),
                'headers': cors_headers
            }
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': cors_headers
        }

def process_quest_completion(player_state: PlayerState, quest_id: str, quest_data: dict):
    """Process quest completion and rewards"""
    rewards = quest_data.get('rewards', {})
    player_state.complete_quest(quest_id, rewards)
    
    # Add any special rewards from content manager
    if random.random() < 0.3:  # 30% chance for special reward
        special_item = content_manager.generate_item('artifacts')
        player_state.add_item(special_item)