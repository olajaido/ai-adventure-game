import boto3
from datetime import datetime
from typing import Dict, List

class PlayerAnalytics:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
        
    def track_choice(self, player_id: str, scene_id: str, choice: str, consequences: Dict):
        """Track a player's choice and its consequences"""
        self.table.put_item(
            Item={
                'userId': player_id,
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'choice',
                'sceneId': scene_id,
                'choice': choice,
                'consequences': consequences
            }
        )
        
    def track_quest_completion(self, player_id: str, quest_id: str, time_taken: int):
        """Track quest completion metrics"""
        self.table.put_item(
            Item={
                'userId': player_id,
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'quest_completion',
                'questId': quest_id,
                'timeTaken': time_taken
            }
        )
        
    def track_item_usage(self, player_id: str, item_id: str, context: str):
        """Track how and when items are used"""
        self.table.put_item(
            Item={
                'userId': player_id,
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'item_usage',
                'itemId': item_id,
                'context': context
            }
        )
        
    def get_player_preferences(self, player_id: str) -> Dict:
        """Analyze player's preferred play style"""
        response = self.table.query(
            KeyConditionExpression='userId = :pid',
            ExpressionAttributeValues={
                ':pid': player_id
            }
        )
        
        choices = []
        quests = []
        items = []
        
        for item in response['Items']:
            if item['type'] == 'choice':
                choices.append(item['choice'])
            elif item['type'] == 'quest_completion':
                quests.append(item['questId'])
            elif item['type'] == 'item_usage':
                items.append(item['itemId'])
                
        return {
            'preferred_choices': self._analyze_choices(choices),
            'quest_completion_rate': len(quests),
            'item_usage_patterns': self._analyze_items(items)
        }
        
    def _analyze_choices(self, choices: List[str]) -> Dict:
        """Analyze patterns in player choices"""
        # Simple analysis - could be more sophisticated
        choice_counts = {}
        for choice in choices:
            choice_counts[choice] = choice_counts.get(choice, 0) + 1
            
        return {
            'most_common': max(choice_counts.items(), key=lambda x: x[1])[0] if choice_counts else None,
            'total_choices': len(choices),
            'choice_distribution': choice_counts
        }
        
    def _analyze_items(self, items: List[str]) -> Dict:
        """Analyze patterns in item usage"""
        item_counts = {}
        for item in items:
            item_counts[item] = item_counts.get(item, 0) + 1
            
        return {
            'favorite_items': sorted(item_counts.items(), key=lambda x: x[1], reverse=True)[:3],
            'total_items_used': len(items)
        }
        
    def get_popular_content(self) -> Dict:
        """Get most popular content across all players"""
        # This would be better implemented with a proper analytics service
        # but this is a simple example
        response = self.table.scan()
        
        choices = []
        quests = []
        items = []
        
        for item in response['Items']:
            if item['type'] == 'choice':
                choices.append(item['choice'])
            elif item['type'] == 'quest_completion':
                quests.append(item['questId'])
            elif item['type'] == 'item_usage':
                items.append(item['itemId'])
                
        return {
            'popular_choices': self._analyze_choices(choices),
            'popular_quests': self._analyze_quests(quests),
            'popular_items': self._analyze_items(items)
        }
        
    def _analyze_quests(self, quests: List[str]) -> Dict:
        """Analyze patterns in quest completion"""
        quest_counts = {}
        for quest in quests:
            quest_counts[quest] = quest_counts.get(quest, 0) + 1
            
        return {
            'most_completed': sorted(quest_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            'total_completions': len(quests)
        }