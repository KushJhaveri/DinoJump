
class GameData(): 
    ENDING_GAME_SPEED = None
    
    @classmethod 
    def min_max_normalize(cls, number, minimum_value, maximum_value):
        return (number - minimum_value) / (maximum_value - minimum_value)

    @classmethod 
    def get_normalized_distances(cls) -> tuple[float]: 
        distances = (abs(player.sprite_rect.x - obstacle.rect.x) for obstacle in obstacles) 
        return (GameData.min_max_normalize(distance, min(distances), max(distances)) for distance in distances)    

    @classmethod 
    def get_normalized_obstacle_heights(cls) -> tuple[float]: 
        heights = (obstacle.rect.height for obstacle in obstacles)  
        return (GameData.min_max_normalize(height, min(height), max(height)) for height in heights)
    
    @classmethod 
    def get_obstacle_velocity(cls) -> float: 
        return Score.game_speed
    
    @classmethod
    def set_ending_game_speed(cls, ending_game_speed: int) -> None: 
        GameData.ENDING_GAME_SPEED = ending_game_speed 
    
    @classmethod
    def get_normalized_game_speeds(cls) -> tuple[float]: 
        game_speeds = range(Score.STARTING_GAME_SPEED, GameData.ENDING_GAME_SPEED + 1)
        return (GameData.min_max_normalize(game_speed, Score.STARTING_GAME_SPEED, GameData.ENDING_GAME_SPEED) 
                for game_speed in game_speeds)
