from abc import ABC, abstractmethod


class AbstractRepo(ABC):
    @abstractmethod
    async def create(self):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_one(self):
        raise NotImplementedError
    
    @abstractmethod
    async def find_all(self):
        raise NotImplementedError
    

