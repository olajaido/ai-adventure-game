# import boto3
# from datetime import datetime
# from typing import Dict, List

# class PlayerAnalytics:
#     def __init__(self, table_name: str):
#         self.dynamodb = boto3.resource('dynamodb')
#         self.table = self.dynamodb.Table(table_name)
        
#     def track_choice(self, player_id: str, scene_id: str, choice: str, consequences: Dict):
#         """Track a player's choice and its consequences"""
#         self.table.put_item(
#             Item={
#                 'userId': player_id,
#                 'timestamp': datetime.utcnow().isoformat(),
#                 'type': 'choice',
#                 'sceneId': scene_id,
#                 'choice': choice,
#                 'consequences': consequences
#             }
#         )
        
#     def track_quest_completion(self, player_id: str, quest_id: str, time_taken: int):
#         """Track quest completion metrics"""
#         self.table.put_item(
#             Item={
#                 'userId': player_id,
#                 'timestamp': datetime.utcnow().isoformat(),
#                 'type': 'quest_completion',
#                 'questId': quest_id,
#                 'timeTaken': time_taken
#             }
#         )
        
#     def track_item_usage(self, player_id: str, item_id: str, context: str):
#         """Track how and when items are used"""
#         self.table.put_item(
#             Item={
#                 'userId': player_id,
#                 'timestamp': datetime.utcnow().isoformat(),
#                 'type': 'item_usage',
#                 'itemId': item_id,
#                 'context': context
#             }
#         )
        
#     def get_player_preferences(self, player_id: str) -> Dict:
#         """Analyze player's preferred play style"""
#         response = self.table.query(
#             KeyConditionExpression='userId = :pid',
#             ExpressionAttributeValues={
#                 ':pid': player_id
#             }
#         )
        
#         choices = []
#         quests = []
#         items = []
        
#         for item in response['Items']:
#             if item['type'] == 'choice':
#                 choices.append(item['choice'])
#             elif item['type'] == 'quest_completion':
#                 quests.append(item['questId'])
#             elif item['type'] == 'item_usage':
#                 items.append(item['itemId'])
                
#         return {
#             'preferred_choices': self._analyze_choices(choices),
#             'quest_completion_rate': len(quests),
#             'item_usage_patterns': self._analyze_items(items)
#         }
        
#     def _analyze_choices(self, choices: List[str]) -> Dict:
#         """Analyze patterns in player choices"""
#         # Simple analysis - could be more sophisticated
#         choice_counts = {}
#         for choice in choices:
#             choice_counts[choice] = choice_counts.get(choice, 0) + 1
            
#         return {
#             'most_common': max(choice_counts.items(), key=lambda x: x[1])[0] if choice_counts else None,
#             'total_choices': len(choices),
#             'choice_distribution': choice_counts
#         }
        
#     def _analyze_items(self, items: List[str]) -> Dict:
#         """Analyze patterns in item usage"""
#         item_counts = {}
#         for item in items:
#             item_counts[item] = item_counts.get(item, 0) + 1
            
#         return {
#             'favorite_items': sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:3],
#             'total_items_used': len(items)
#         }
        
#     def get_popular_content(self) -> Dict:
#         """Get most popular content across all players"""
#         # This would be better implemented with a proper analytics service
#         # but this is a simple example
#         response = self.table.scan()
        
#         choices = []
#         quests = []
#         items = []
        
#         for item in response['Items']:
#             if item['type'] == 'choice':
#                 choices.append(item['choice'])
#             elif item['type'] == 'quest_completion':
#                 quests.append(item['questId'])
#             elif item['type'] == 'item_usage':
#                 items.append(item['itemId'])
                
#         return {
#             'popular_choices': self._analyze_choices(choices),
#             'popular_quests': self._analyze_quests(quests),
#             'popular_items': self._analyze_items(items)
#         }
        
#     def _analyze_quests(self, quests: List[str]) -> Dict:
#         """Analyze patterns in quest completion"""
#         quest_counts = {}
#         for quest in quests:
#             quest_counts[quest] = quest_counts.get(quest, 0) + 1
            
#         return {
#             'most_completed': sorted(quest_counts.items(), key=lambda x: x[1], reverse=True)[:5],
#             'total_completions': len(quests)
#         }

import boto3
from datetime import datetime
from typing import Dict, List

class PlayerAnalytics:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        
    def track_choice(self, player_id: str, scene_id: str, choice: str, consequences: Dict):
        """Track a player's choice and its consequences"""
        timestamp = datetime.utcnow().isoformat()
        try:
            self.table.put_item(
                Item={
                    'userId': player_id,
                    'gameId': f'analytics_{timestamp}',  # Unique gameId for each analytics entry
                    'type': 'choice',
                    'sceneId': scene_id,
                    'choice': choice,
                    'consequences': consequences,
                    'timestamp': timestamp
                }
            )
            print(f"Successfully tracked choice for player {player_id}")
        except Exception as e:
            print(f"Error tracking choice: {str(e)}")
        
    def track_quest_completion(self, player_id: str, quest_id: str, time_taken: int):
        """Track quest completion metrics"""
        timestamp = datetime.utcnow().isoformat()
        try:
            self.table.put_item(
                Item={
                    'userId': player_id,
                    'gameId': f'analytics_quest_{timestamp}',
                    'type': 'quest_completion',
                    'questId': quest_id,
                    'timeTaken': time_taken,
                    'timestamp': timestamp
                }
            )
            print(f"Successfully tracked quest completion for player {player_id}")
        except Exception as e:
            print(f"Error tracking quest completion: {str(e)}")
        
    def track_item_usage(self, player_id: str, item_id: str, context: str):
        """Track how and when items are used"""
        timestamp = datetime.utcnow().isoformat()
        try:
            self.table.put_item(
                Item={
                    'userId': player_id,
                    'gameId': f'analytics_item_{timestamp}',
                    'type': 'item_usage',
                    'itemId': item_id,
                    'context': context,
                    'timestamp': timestamp
                }
            )
            print(f"Successfully tracked item usage for player {player_id}")
        except Exception as e:
            print(f"Error tracking item usage: {str(e)}")
        
    def get_player_preferences(self, player_id: str) -> Dict:
        """Analyze player's preferred play style"""
        try:
            response = self.table.query(
                KeyConditionExpression='userId = :pid',
                ExpressionAttributeValues={
                    ':pid': player_id
                },
                ScanIndexForward=False  # Get most recent first
            )
            
            choices = []
            quests = []
            items = []
            
            for item in response.get('Items', []):
                if item.get('type') == 'choice':
                    choices.append(item.get('choice'))
                elif item.get('type') == 'quest_completion':
                    quests.append(item.get('questId'))
                elif item.get('type') == 'item_usage':
                    items.append(item.get('itemId'))
                    
            return {
                'preferred_choices': self._analyze_choices(choices),
                'quest_completion_rate': len(quests),
                'quest_history': quests[-5:] if quests else [],  # Last 5 completed quests
                'item_usage_patterns': self._analyze_items(items)
            }
        except Exception as e:
            print(f"Error getting player preferences: {str(e)}")
            return {
                'preferred_choices': {},
                'quest_completion_rate': 0,
                'quest_history': [],
                'item_usage_patterns': {}
            }
        
    def _analyze_choices(self, choices: List[str]) -> Dict:
        """Analyze patterns in player choices"""
        try:
            choice_counts = {}
            for choice in choices:
                if choice:  # Check for None
                    choice_counts[choice] = choice_counts.get(choice, 0) + 1
                
            most_common = None
            if choice_counts:
                most_common = max(choice_counts.items(), key=lambda x: x[1])[0]
                
            return {
                'most_common': most_common,
                'total_choices': len(choices),
                'choice_distribution': choice_counts
            }
        except Exception as e:
            print(f"Error analyzing choices: {str(e)}")
            return {
                'most_common': None,
                'total_choices': 0,
                'choice_distribution': {}
            }
        
    def _analyze_items(self, items: List[str]) -> Dict:
        """Analyze patterns in item usage"""
        try:
            item_counts = {}
            for item in items:
                if item:  # Check for None
                    item_counts[item] = item_counts.get(item, 0) + 1
                
            favorite_items = []
            if item_counts:
                favorite_items = sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                
            return {
                'favorite_items': favorite_items,
                'total_items_used': len(items)
            }
        except Exception as e:
            print(f"Error analyzing items: {str(e)}")
            return {
                'favorite_items': [],
                'total_items_used': 0
            }

    def get_popular_content(self) -> Dict:
        """Get most popular content across all players"""
        try:
            response = self.table.scan()
            
            choices = []
            quests = []
            items = []
            
            for item in response.get('Items', []):
                if item.get('type') == 'choice':
                    choices.append(item.get('choice'))
                elif item.get('type') == 'quest_completion':
                    quests.append(item.get('questId'))
                elif item.get('type') == 'item_usage':
                    items.append(item.get('itemId'))
                    
            return {
                'popular_choices': self._analyze_choices(choices),
                'popular_quests': self._analyze_quests(quests),
                'popular_items': self._analyze_items(items)
            }
        except Exception as e:
            print(f"Error getting popular content: {str(e)}")
            return {
                'popular_choices': {},
                'popular_quests': {},
                'popular_items': {}
            }
        
    def _analyze_quests(self, quests: List[str]) -> Dict:
        """Analyze patterns in quest completion"""
        try:
            quest_counts = {}
            for quest in quests:
                if quest:  # Check for None
                    quest_counts[quest] = quest_counts.get(quest, 0) + 1
                    
            most_completed = []
            if quest_counts:
                most_completed = sorted(quest_counts.items(), key=lambda x: x[1], reverse=True)[:5]
                
            return {
                'most_completed': most_completed,
                'total_completions': len(quests)
            }
        except Exception as e:
            print(f"Error analyzing quests: {str(e)}")
            return {
                'most_completed': [],
                'total_completions': 0
            }