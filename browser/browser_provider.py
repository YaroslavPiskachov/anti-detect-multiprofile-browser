import os
from abc import ABC, abstractmethod

class BrowserProvider(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def start_with_context(self, user_data):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def create_context(self, profile):
        pass

    @abstractmethod
    def close_context(self):
        pass

    @abstractmethod
    def new_page(self):
        pass