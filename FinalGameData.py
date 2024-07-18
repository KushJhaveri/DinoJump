from DinosaurGame import player, obstacles, Score

class GameData:
    HIGHEST_SCORE = float('-inf') 
    
    @classmethod
    def get_normalized_data(cls): 
        return GameData.min_max_normalize_collection(GameData.get_distances() + GameData.get_obstacle_heights() + Score.game_speed)
    
    @classmethod
    def get_distances(cls):
        return [abs(player.sprite_rect.x - obstacle.rect.x) for obstacle in obstacles]

    @classmethod
    def get_obstacle_heights(cls):
        return [obstacle.rect.height for obstacle in obstacles]

    @staticmethod
    def min_max_normalize(number, minimum_value, maximum_value):
        return (number - minimum_value) / (maximum_value - minimum_value)

    @staticmethod
    def min_max_normalize_collection(collection):
        min_value = min(collection)
        max_value = max(collection)
        return [GameData.min_max_normalize(value, min_value, max_value) for value in collection]
