class GameData(): 
    
    def __init__(self): 
        self.DISTANCES = [] 
        self.OBSTACLE_HEIGHTS = [] 
        self.GAME_SPEEDS = [] 
    
    def update(self) -> None: 
        self.DISTANCES.append(self.get_distances())
        self.OBSTACLE_HEIGHTS.append(self.get_obstacle_heights())
        self.GAME_SPEEDS.append(Score.game_speed)

    def normalize_data(self) -> None: 
        self.NORMALIZED_DISTANCES = GameData.min_max_normalize_collection(self.DISTANCES)
        self.NORMALIZED_OBSTACLE_HEIGHTS = GameData.min_max_normalize_collection(self.OBSTACLE_HEIGHTS)
        self.NORMALIZED_GAME_SPEEDS = GameData.min_max_normalize_collection(self.NORMALIZED_GAME_SPEEDS)

    def get_distances(cls) -> tuple[float]: 
        return (abs(player.sprite_rect.x - obstacle.rect.x) for obstacle in obstacles)
        
    def get_obstacle_heights(cls) -> tuple[float]: 
        return (obstacle.rect.height for obstacle in obstacles)  
    
    @classmethod
    def min_max_normalize(cls, number, minimum_value, maximum_value) -> float:
        return (number - minimum_value) / (maximum_value - minimum_value)
    
    @classmethod
    def min_max_normalize_collection(cls, collection) -> list[float]: 
        min_value = min(collection)
        max_value = max(collection)
        return (GameData.min_max_normalize(value, min_value, max_value) for value in collection)
