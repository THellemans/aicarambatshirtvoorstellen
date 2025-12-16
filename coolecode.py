#!/usr/bin/env python3
"""
Complex Python file about Pokémon: 
Simulates Pokémon management, battles, data analysis using OOP, 
decorators, generators, data classes, and advanced Python features.
"""

import random
import statistics
from dataclasses import dataclass, field
from typing import List, Dict, Generator, Callable
from functools import wraps
import itertools
import json

# ---------- Utilities ----------

def log_action(func: Callable) -> Callable:
    """Decorator to log function calls with arguments."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[DEBUG] Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[DEBUG] {func.__name__} returned {result}")
        return result
    return wrapper

def infinite_id_generator(prefix: str) -> Generator[str, None, None]:
    counter = 1
    while True:
        yield f"{prefix}{counter}"
        counter += 1

id_gen = infinite_id_generator("PKMN-")

# ---------- Pokémon Classes ----------

@dataclass(order=True)
class Pokemon:
    sort_index: int = field(init=False, repr=False)
    name: str
    type_: str
    hp: int
    attack: int
    defense: int
    speed: int
    moves: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.id: str = next(id_gen)
        self.sort_index = self.hp  # Default sort index
        print(f"[INFO] Created Pokémon {self.name} (ID: {self.id}) of type {self.type_}")

    def power_level(self) -> int:
        return self.attack + self.defense + self.speed

    def receive_damage(self, damage: int) -> None:
        self.hp = max(self.hp - damage, 0)
        print(f"{self.name} receives {damage} damage, HP is now {self.hp}.")

    @log_action
    def attack_opponent(self, opponent: 'Pokemon') -> None:
        move = random.choice(self.moves)
        damage = max(self.attack - opponent.defense // 2, 1)
        print(f"{self.name} uses {move}! Deals {damage} damage to {opponent.name}.")
        opponent.receive_damage(damage)

# ---------- Complex Battle Simulation ----------

class BattleArena:
    def __init__(self):
        self.history: List[Dict] = []

    @log_action
    def battle(self, pkmn1: Pokemon, pkmn2: Pokemon) -> str:
        print(f"Battle starts between {pkmn1.name} and {pkmn2.name}!")
        while pkmn1.hp > 0 and pkmn2.hp > 0:
            if pkmn1.speed >= pkmn2.speed:
                pkmn1.attack_opponent(pkmn2)
                if pkmn2.hp <= 0: break
                pkmn2.attack_opponent(pkmn1)
            else:
                pkmn2.attack_opponent(pkmn1)
                if pkmn1.hp <= 0: break
                pkmn1.attack_opponent(pkmn2)

        winner = pkmn1 if pkmn1.hp > 0 else pkmn2
        print(f"Winner is {winner.name}!")
        self.history.append({
            "pkmn1": pkmn1.name,
            "pkmn2": pkmn2.name,
            "winner": winner.name
        })
        return winner.name

    def export_history(self, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(self.history, f, indent=2)
        print(f"[INFO] Battle history exported to {filename}")

# ---------- Data Analysis ----------

@log_action
def pokemon_statistics(pokemon_list: List[Pokemon]) -> Dict[str, float]:
    hp_values = [p.hp for p in pokemon_list]
    stats = {
        "average_hp": statistics.mean(hp_values),
        "max_hp": max(hp_values),
        "min_hp": min(hp_values)
    }
    return stats

@log_action
def group_by_type(pokemon_list: List[Pokemon]) -> Dict[str, List[Pokemon]]:
    grouped = {}
    for type_, group in itertools.groupby(sorted(pokemon_list, key=lambda p: p.type_), key=lambda p: p.type_):
        grouped[type_] = list(group)
    return grouped

# ---------- Main Simulation ----------

def main():
    pokemons = [
        Pokemon(name="Pikachu", type_="Electric", hp=35, attack=55, defense=40, speed=90, moves=["Thunderbolt", "Quick Attack", "Iron Tail"]),
        Pokemon(name="Charmander", type_="Fire", hp=39, attack=52, defense=43, speed=65, moves=["Flamethrower", "Scratch", "Ember"]),
        Pokemon(name="Squirtle", type_="Water", hp=44, attack=48, defense=65, speed=43, moves=["Water Gun", "Tackle", "Bubble"]),
        Pokemon(name="Bulbasaur", type_="Grass", hp=45, attack=49, defense=49, speed=45, moves=["Vine Whip", "Tackle", "Seed Bomb"])
    ]

    stats = pokemon_statistics(pokemons)
    print(f"Stats: {stats}")

    grouped = group_by_type(pokemons)
    for type_, group in grouped.items():
        print(f"Type {type_}: {[p.name for p in group]}")

    arena = BattleArena()
    arena.battle(pokemons[0], pokemons[1])
    arena.battle(pokemons[2], pokemons[3])
    arena.export_history("battle_history.json")

if __name__ == "__main__":
    main()