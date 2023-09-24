
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

class Questionnaire(StatesGroup):
    howMuchCoins = State()
    Message_ToSend = State()