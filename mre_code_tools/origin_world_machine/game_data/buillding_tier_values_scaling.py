from dataclasses import dataclass
from functools import reduce
from typing import List, Union

# thanks S.O.
fib = lambda n: reduce(lambda x, _: x+[x[-1]+x[-2]],range(n-2), [0, 1])


# build time:
# tier * 180
# energy upkeep: add previous tier 
# jobs: tier * 2
# minerals build cost: ( tier * 200 ) + 200
# rare cost: tier * 50 , but for tier 1, dont charge any 
# rare upkeep: tier - 1


def calc_rare_upkeep(tier: int) -> int:
    return tier - 1

def calc_energy_upkeep(tier: int) -> int:
    return sum(fib(tier+1))+1

def calc_build_time(tier: int) -> int:
    return 180 + tier * 180

def calc_minerals_cost(tier: int) -> int:
    return 200 + tier * 200

def calc_rare_cost(tier: int) -> int:
    return (-50 + tier * 50) if tier > 1 else 0

def increment_arbitrary_per_tier(resource: str, amount_per_tier: int, tier: int) -> str:
    return f"{resource} = {amount_per_tier * tier}"


def return_vanilla_resources_for_tier(tier: int):

    return {
        "cost": {
            "minerals": calc_minerals_cost(tier),
            "rare": calc_rare_cost(tier)
        },
        "upkeep": {
            "energy": calc_energy_upkeep(tier),
            "rare": calc_rare_upkeep(tier)
        }
    }


def resource_condition_with_scope(
        category: str, resource: str, tier: int, amount_per_tier,
        scope: str='', condition: str='',
        tier_math_function=None
):
    """Generate code for inside a building 'resource' block

    :param category: One of "cost", "upkeep", "produces"
    :type category: str
    :param scope: The scope of the trigger (planet, owner, etc)
    :type scope: str
    :param condition: The trigger and value, in Clausewitz script
    :type condition: str
    :param resource: What resource to produce/cost/upkeep
    :type resource: str
    :param amount_per_tier: How much should this resource scale per tier
    :type amount_per_tier: _type_
    :param tier: What tier to calculate
    :type tier: int
    :param tier_math_function: A function to use to calculate a custom value with the tier
    :return: String of Clausewitz script
    :rtype: str
    """

    condition_block = f"""
    trigger = {{
        exists = {scope}
        {scope} = {{ {condition} }}
    }
"""
    final_amount = tier_math_function(tier) if tier_math_function else (amount_per_tier * tier)

    return f"""
{category} = {{
    {condition_block if condition else ''}
    {resource} = {final_amount}
}}
"""


@dataclass
class ScopedTrigger:
    scope: str
    trigger: str
    operand: str = '='
    value: str

@dataclass
class ScopedTriggerList:
    scope: str
    conditions: List[ScopedTrigger]

@dataclass
class InlineScriptParam:
    var: str
    value: Union[str, int]

@dataclass
class InlineScriptBlock:
    script: str
    params: List[InlineScriptParam]

@dataclass
class ListBlock:
    """Any block that expresses a list of items"""
    items: List[str]
