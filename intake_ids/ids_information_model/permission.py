from .rule import Rule
from .duty import Duty

class Permission(Rule):
    pre_duty: list[Duty] = []
    post_duty: list[Duty] = []
