import logging

logger = logging.getLogger(__name__)

user_cities = {}

class UserCity:
    @staticmethod
    def get(user_id: int) -> str | None:
        return user_cities.get(user_id)
    
    @staticmethod
    def set(user_id: int, city: str):
        user_cities[user_id] = city
        
    @staticmethod
    def delete(user_id: int) -> bool:
        if user_id in user_cities:
            del user_cities[user_id]
            return True
        return False
    