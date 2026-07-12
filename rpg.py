#!/usr/bin/env python3
"""
=============================================================================
  CHRONICLES OF THE SHATTERED REALM — A Terminal RPG Engine
  A single-file Python RPG with combat, inventory, quests, crafting,
  spells, dialogue trees, world map, save/load, ASCII art, and more.
=============================================================================
"""

import os
import sys
import time
import math
import json
import random
import textwrap
import hashlib
import datetime
import itertools
import collections
import copy
import re

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1: TERMINAL UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

ANSI_RESET   = "\033[0m"
ANSI_BOLD    = "\033[1m"
ANSI_DIM     = "\033[2m"
ANSI_RED     = "\033[91m"
ANSI_GREEN   = "\033[92m"
ANSI_YELLOW  = "\033[93m"
ANSI_BLUE    = "\033[94m"
ANSI_MAGENTA = "\033[95m"
ANSI_CYAN    = "\033[96m"
ANSI_WHITE   = "\033[97m"
ANSI_GRAY    = "\033[90m"

def colored(text, color):
    return f"{color}{text}{ANSI_RESET}"

def bold(text):
    return f"{ANSI_BOLD}{text}{ANSI_RESET}"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_header(title):
    width = 60
    border = "═" * width
    print(colored(f"╔{border}╗", ANSI_CYAN))
    pad = (width - len(title)) // 2
    print(colored(f"║{' ' * pad}{title}{' ' * (width - pad - len(title))}║", ANSI_CYAN))
    print(colored(f"╚{border}╝", ANSI_CYAN))

def print_divider(char="─", width=62):
    print(colored(char * width, ANSI_GRAY))

def print_box(lines, color=ANSI_WHITE):
    max_len = max(len(l) for l in lines)
    print(colored("┌" + "─" * (max_len + 2) + "┐", color))
    for line in lines:
        pad = max_len - len(line)
        print(colored(f"│ {line}{' ' * pad} │", color))
    print(colored("└" + "─" * (max_len + 2) + "┘", color))

def wrap_text(text, width=58):
    return textwrap.wrap(text, width)

def ask(prompt, valid=None):
    while True:
        answer = input(colored(f"  ► {prompt}: ", ANSI_YELLOW)).strip()
        if valid is None or answer.lower() in [v.lower() for v in valid]:
            return answer
        print(colored(f"  Invalid choice. Options: {', '.join(valid)}", ANSI_RED))

def pause(msg="Press ENTER to continue..."):
    input(colored(f"\n  {msg}", ANSI_GRAY))

def roll_dice(sides, count=1, bonus=0):
    return sum(random.randint(1, sides) for _ in range(count)) + bonus

def percentage_chance(pct):
    return random.randint(1, 100) <= pct

def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

def number_format(n):
    return f"{n:,}"

def time_of_day_label(hour):
    if 5 <= hour < 8:   return "Dawn"
    if 8 <= hour < 12:  return "Morning"
    if 12 <= hour < 14: return "Noon"
    if 14 <= hour < 17: return "Afternoon"
    if 17 <= hour < 20: return "Dusk"
    if 20 <= hour < 23: return "Evening"
    return "Midnight"

def health_bar(current, maximum, width=20):
    ratio = current / maximum if maximum > 0 else 0
    filled = int(ratio * width)
    bar = "█" * filled + "░" * (width - filled)
    color = ANSI_GREEN if ratio > 0.6 else ANSI_YELLOW if ratio > 0.3 else ANSI_RED
    return colored(f"[{bar}]", color) + f" {current}/{maximum}"

def mana_bar(current, maximum, width=20):
    ratio = current / maximum if maximum > 0 else 0
    filled = int(ratio * width)
    bar = "▪" * filled + "·" * (width - filled)
    return colored(f"[{bar}]", ANSI_BLUE) + f" {current}/{maximum}"

def xp_bar(current, needed, width=20):
    ratio = current / needed if needed > 0 else 0
    filled = int(ratio * width)
    bar = "◆" * filled + "◇" * (width - filled)
    return colored(f"[{bar}]", ANSI_MAGENTA) + f" {current}/{needed}"

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2: GAME CONSTANTS & TABLES
# ─────────────────────────────────────────────────────────────────────────────

VERSION = "1.0.0"
SAVE_FILE = "shattered_realm_save.json"
MAX_LEVEL = 50
BASE_XP_PER_LEVEL = 100
XP_SCALE_FACTOR = 1.35
MAX_INVENTORY_SLOTS = 30
GOLD_CURRENCY_NAME = "Gold"
CRITICAL_HIT_MULTIPLIER = 2.0
DODGE_BASE_CHANCE = 5
BLOCK_BASE_CHANCE = 10
FLEE_BASE_CHANCE = 40
MAX_PARTY_SIZE = 4
WORLD_WIDTH = 20
WORLD_HEIGHT = 15
DAY_LENGTH_SECONDS = 120

ELEMENT_TYPES = ["fire", "ice", "lightning", "earth", "wind", "holy", "dark", "poison"]
DAMAGE_TYPES  = ["physical", "magical", "true"]
STATUS_EFFECTS = ["burn", "freeze", "paralyze", "poison", "bleed", "stun", "blind", "slow", "haste", "regen", "shield", "berserk"]

RACE_BONUSES = {
    "Human":    {"str": 1, "dex": 1, "int": 1, "wis": 1, "con": 1, "lck": 1},
    "Elf":      {"str": 0, "dex": 3, "int": 2, "wis": 2, "con": 0, "lck": 1},
    "Dwarf":    {"str": 2, "dex": 0, "int": 0, "wis": 1, "con": 4, "lck": 1},
    "Orc":      {"str": 4, "dex": 1, "int": 0, "wis": 0, "con": 3, "lck": 0},
    "Halfling": {"str": 0, "dex": 3, "int": 1, "wis": 1, "con": 0, "lck": 4},
    "Tiefling": {"str": 1, "dex": 1, "int": 3, "wis": 0, "con": 0, "lck": 3},
}

CLASS_BONUSES = {
    "Warrior":  {"str": 4, "dex": 1, "int": 0, "wis": 0, "con": 3, "lck": 0},
    "Rogue":    {"str": 1, "dex": 5, "int": 1, "wis": 0, "con": 1, "lck": 2},
    "Mage":     {"str": 0, "dex": 1, "int": 5, "wis": 3, "con": 0, "lck": 1},
    "Paladin":  {"str": 3, "dex": 0, "int": 1, "wis": 3, "con": 2, "lck": 1},
    "Ranger":   {"str": 2, "dex": 3, "int": 1, "wis": 2, "con": 1, "lck": 1},
    "Bard":     {"str": 1, "dex": 2, "int": 2, "wis": 2, "con": 1, "lck": 2},
}

CLASS_HP_DICE = {"Warrior": 10, "Rogue": 8, "Mage": 6, "Paladin": 10, "Ranger": 8, "Bard": 8}
CLASS_MP_BASE = {"Warrior": 20, "Rogue": 30, "Mage": 80, "Paladin": 50, "Ranger": 40, "Bard": 60}

WEAPON_TYPES = {
    "Sword":    {"dmg_dice": 8,  "dmg_count": 1, "bonus": 0,  "crit": 19, "range": "melee"},
    "Dagger":   {"dmg_dice": 4,  "dmg_count": 2, "bonus": 0,  "crit": 18, "range": "melee"},
    "Staff":    {"dmg_dice": 6,  "dmg_count": 1, "bonus": 2,  "crit": 20, "range": "melee"},
    "Bow":      {"dmg_dice": 6,  "dmg_count": 1, "bonus": 0,  "crit": 19, "range": "ranged"},
    "Axe":      {"dmg_dice": 12, "dmg_count": 1, "bonus": 0,  "crit": 20, "range": "melee"},
    "Spear":    {"dmg_dice": 8,  "dmg_count": 1, "bonus": 1,  "crit": 20, "range": "melee"},
    "Wand":     {"dmg_dice": 4,  "dmg_count": 1, "bonus": 3,  "crit": 20, "range": "ranged"},
    "Hammer":   {"dmg_dice": 10, "dmg_count": 1, "bonus": 0,  "crit": 20, "range": "melee"},
    "Crossbow": {"dmg_dice": 8,  "dmg_count": 1, "bonus": 0,  "crit": 19, "range": "ranged"},
    "Whip":     {"dmg_dice": 4,  "dmg_count": 1, "bonus": 0,  "crit": 18, "range": "melee"},
}

ARMOR_TYPES = {
    "Cloth":    {"defense": 1,  "magic_resist": 5,  "weight": 1},
    "Leather":  {"defense": 3,  "magic_resist": 2,  "weight": 2},
    "Hide":     {"defense": 5,  "magic_resist": 1,  "weight": 3},
    "Chainmail":{"defense": 7,  "magic_resist": 0,  "weight": 5},
    "Splint":   {"defense": 9,  "magic_resist": 0,  "weight": 7},
    "Plate":    {"defense": 12, "magic_resist": 0,  "weight": 9},
    "Robe":     {"defense": 0,  "magic_resist": 8,  "weight": 1},
    "Scale":    {"defense": 8,  "magic_resist": 3,  "weight": 6},
}

TIER_NAMES = {1: "Common", 2: "Uncommon", 3: "Rare", 4: "Epic", 5: "Legendary"}
TIER_COLORS = {
    1: ANSI_WHITE,
    2: ANSI_GREEN,
    3: ANSI_BLUE,
    4: ANSI_MAGENTA,
    5: ANSI_YELLOW,
}
TIER_MULTIPLIERS = {1: 1.0, 2: 1.5, 3: 2.5, 4: 4.0, 5: 7.0}

PREFIXES = {
    "fire":      "Blazing",
    "ice":       "Frozen",
    "lightning": "Crackling",
    "earth":     "Stone",
    "wind":      "Gale",
    "holy":      "Sacred",
    "dark":      "Cursed",
    "poison":    "Venomous",
}

SUFFIXES = {
    "str":  "of Might",
    "dex":  "of Swiftness",
    "int":  "of Wisdom",
    "wis":  "of Insight",
    "con":  "of Endurance",
    "lck":  "of Fortune",
}

MONSTER_FAMILIES = {
    "Goblin":    {"hp": 20, "str": 5, "dex": 8, "int": 3, "xp": 30,  "gold": (2, 8),   "icon": "👺"},
    "Skeleton":  {"hp": 30, "str": 7, "dex": 5, "int": 1, "xp": 45,  "gold": (1, 5),   "icon": "💀"},
    "Wolf":      {"hp": 35, "str": 8, "dex": 10,"int": 2, "xp": 50,  "gold": (0, 3),   "icon": "🐺"},
    "Orc":       {"hp": 50, "str": 12,"dex": 4, "int": 2, "xp": 70,  "gold": (5, 15),  "icon": "👹"},
    "Witch":     {"hp": 40, "str": 4, "dex": 6, "int": 12,"xp": 80,  "gold": (8, 20),  "icon": "🧙"},
    "Dragon":    {"hp": 200,"str": 20,"dex": 8, "int": 18,"xp": 500, "gold": (50, 200),"icon": "🐉"},
    "Vampire":   {"hp": 80, "str": 14,"dex": 12,"int": 10,"xp": 150, "gold": (20, 60), "icon": "🧛"},
    "Slime":     {"hp": 25, "str": 3, "dex": 2, "int": 1, "xp": 20,  "gold": (0, 4),   "icon": "🟢"},
    "Bandit":    {"hp": 45, "str": 9, "dex": 9, "int": 5, "xp": 65,  "gold": (10, 30), "icon": "🗡️"},
    "Golem":     {"hp": 120,"str": 18,"dex": 2, "int": 0, "xp": 200, "gold": (15, 40), "icon": "🗿"},
    "Harpy":     {"hp": 55, "str": 10,"dex": 15,"int": 6, "xp": 90,  "gold": (5, 18),  "icon": "🦅"},
    "Lich":      {"hp": 150,"str": 8, "dex": 6, "int": 20,"xp": 400, "gold": (40, 100),"icon": "☠️"},
    "Minotaur":  {"hp": 100,"str": 18,"dex": 5, "int": 3, "xp": 180, "gold": (10, 35), "icon": "🐂"},
    "Troll":     {"hp": 90, "str": 16,"dex": 3, "int": 2, "xp": 160, "gold": (8, 25),  "icon": "👾"},
    "Mermaid":   {"hp": 65, "str": 8, "dex": 12,"int": 14,"xp": 120, "gold": (15, 45), "icon": "🧜"},
}

SPELL_BOOK = {
    "Fireball": {
        "cost": 15, "element": "fire",  "dmg_dice": 8,  "dmg_count": 2, "bonus": 5,
        "target": "single", "level_req": 1, "school": "Evocation",
        "desc": "Hurls a ball of fire at the target.",
    },
    "Ice Lance": {
        "cost": 12, "element": "ice",   "dmg_dice": 6,  "dmg_count": 2, "bonus": 4,
        "target": "single", "level_req": 1, "school": "Evocation",
        "desc": "Launches a spear of ice that can slow the enemy.",
    },
    "Thunder Strike": {
        "cost": 20, "element": "lightning","dmg_dice": 10,"dmg_count": 1,"bonus": 6,
        "target": "single", "level_req": 3, "school": "Evocation",
        "desc": "Calls a bolt of lightning down upon the foe.",
    },
    "Earthquake": {
        "cost": 30, "element": "earth", "dmg_dice": 6,  "dmg_count": 3, "bonus": 0,
        "target": "all",    "level_req": 5, "school": "Evocation",
        "desc": "Shakes the earth, hitting all enemies.",
    },
    "Gale Slash": {
        "cost": 18, "element": "wind",  "dmg_dice": 8,  "dmg_count": 1, "bonus": 8,
        "target": "single", "level_req": 2, "school": "Evocation",
        "desc": "A sharp blade of wind cuts through the target.",
    },
    "Holy Light": {
        "cost": 25, "element": "holy",  "dmg_dice": 10, "dmg_count": 1, "bonus": 10,
        "target": "single", "level_req": 4, "school": "Divine",
        "desc": "Radiant holy energy burns the undead.",
    },
    "Shadow Bolt": {
        "cost": 15, "element": "dark",  "dmg_dice": 7,  "dmg_count": 1, "bonus": 7,
        "target": "single", "level_req": 2, "school": "Necromancy",
        "desc": "A bolt of pure shadow energy.",
    },
    "Venom Cloud": {
        "cost": 22, "element": "poison","dmg_dice": 4,  "dmg_count": 2, "bonus": 0,
        "target": "all",    "level_req": 3, "school": "Alchemy",
        "desc": "Releases a cloud of poison over all foes.",
    },
    "Heal": {
        "cost": 20, "element": "holy",  "dmg_dice": 8,  "dmg_count": 2, "bonus": 5,
        "target": "self",   "level_req": 1, "school": "Restoration",
        "desc": "Channels healing energy into yourself.",
    },
    "Barrier": {
        "cost": 30, "element": "holy",  "dmg_dice": 0,  "dmg_count": 0, "bonus": 0,
        "target": "self",   "level_req": 2, "school": "Abjuration",
        "desc": "Creates a magical barrier that absorbs damage.",
    },
    "Arcane Missile": {
        "cost": 8,  "element": "dark",  "dmg_dice": 6,  "dmg_count": 1, "bonus": 3,
        "target": "single", "level_req": 1, "school": "Arcane",
        "desc": "A quick arcane bolt — cheap and reliable.",
    },
    "Blizzard": {
        "cost": 45, "element": "ice",   "dmg_dice": 8,  "dmg_count": 3, "bonus": 5,
        "target": "all",    "level_req": 7, "school": "Evocation",
        "desc": "Summons a blizzard over all enemies.",
    },
    "Inferno": {
        "cost": 60, "element": "fire",  "dmg_dice": 12, "dmg_count": 3, "bonus": 10,
        "target": "all",    "level_req": 10,"school": "Evocation",
        "desc": "The ground erupts in hellfire.",
    },
    "Chain Lightning": {
        "cost": 35, "element": "lightning","dmg_dice": 8,"dmg_count": 2,"bonus": 5,
        "target": "all",    "level_req": 6, "school": "Evocation",
        "desc": "Lightning leaps from foe to foe.",
    },
    "Reanimate": {
        "cost": 40, "element": "dark",  "dmg_dice": 0,  "dmg_count": 0, "bonus": 0,
        "target": "self",   "level_req": 8, "school": "Necromancy",
        "desc": "Raises fallen allies as skeletal warriors.",
    },
    "Time Warp": {
        "cost": 50, "element": "wind",  "dmg_dice": 0,  "dmg_count": 0, "bonus": 0,
        "target": "self",   "level_req": 9, "school": "Chronomancy",
        "desc": "Warps time to gain an extra action this turn.",
    },
    "Meteor": {
        "cost": 80, "element": "fire",  "dmg_dice": 20, "dmg_count": 2, "bonus": 15,
        "target": "all",    "level_req": 15,"school": "Evocation",
        "desc": "Calls a meteor from the sky. Devastating.",
    },
    "Summon Golem": {
        "cost": 70, "element": "earth", "dmg_dice": 0,  "dmg_count": 0, "bonus": 0,
        "target": "self",   "level_req": 12,"school": "Conjuration",
        "desc": "Summons an earth golem to fight for you.",
    },
}

CRAFTING_RECIPES = {
    "Health Potion": {
        "ingredients": {"Red Herb": 2, "Empty Vial": 1},
        "result": "Health Potion",
        "skill_req": 0,
    },
    "Mana Potion": {
        "ingredients": {"Blue Herb": 2, "Empty Vial": 1},
        "result": "Mana Potion",
        "skill_req": 0,
    },
    "Elixir of Power": {
        "ingredients": {"Red Herb": 3, "Blue Herb": 3, "Dragon Scale": 1},
        "result": "Elixir of Power",
        "skill_req": 5,
    },
    "Iron Sword": {
        "ingredients": {"Iron Ingot": 3, "Wood Plank": 1},
        "result": "Iron Sword",
        "skill_req": 3,
    },
    "Steel Shield": {
        "ingredients": {"Steel Ingot": 4, "Leather": 2},
        "result": "Steel Shield",
        "skill_req": 5,
    },
    "Mage Robe": {
        "ingredients": {"Silk": 4, "Blue Herb": 2, "Thread": 3},
        "result": "Mage Robe",
        "skill_req": 4,
    },
    "Antidote": {
        "ingredients": {"Green Herb": 2, "Empty Vial": 1},
        "result": "Antidote",
        "skill_req": 1,
    },
    "Explosive Flask": {
        "ingredients": {"Red Herb": 1, "Gunpowder": 2, "Empty Vial": 1},
        "result": "Explosive Flask",
        "skill_req": 4,
    },
    "Lucky Charm": {
        "ingredients": {"Rabbit Foot": 1, "Gold Dust": 2, "Thread": 1},
        "result": "Lucky Charm",
        "skill_req": 2,
    },
    "Phoenix Feather Cloak": {
        "ingredients": {"Phoenix Feather": 2, "Silk": 5, "Holy Water": 1},
        "result": "Phoenix Feather Cloak",
        "skill_req": 8,
    },
}

ITEM_DEFINITIONS = {
    "Health Potion":      {"type": "consumable", "effect": "heal",   "value": 50,  "gold": 25,  "weight": 0.5},
    "Mana Potion":        {"type": "consumable", "effect": "mana",   "value": 40,  "gold": 30,  "weight": 0.5},
    "Elixir of Power":    {"type": "consumable", "effect": "buff",   "value": 0,   "gold": 150, "weight": 0.3},
    "Antidote":           {"type": "consumable", "effect": "cure",   "value": 0,   "gold": 20,  "weight": 0.3},
    "Explosive Flask":    {"type": "consumable", "effect": "bomb",   "value": 80,  "gold": 45,  "weight": 1.0},
    "Red Herb":           {"type": "material",   "effect": None,     "value": 0,   "gold": 5,   "weight": 0.1},
    "Blue Herb":          {"type": "material",   "effect": None,     "value": 0,   "gold": 6,   "weight": 0.1},
    "Green Herb":         {"type": "material",   "effect": None,     "value": 0,   "gold": 4,   "weight": 0.1},
    "Empty Vial":         {"type": "material",   "effect": None,     "value": 0,   "gold": 3,   "weight": 0.2},
    "Iron Ingot":         {"type": "material",   "effect": None,     "value": 0,   "gold": 15,  "weight": 1.0},
    "Steel Ingot":        {"type": "material",   "effect": None,     "value": 0,   "gold": 25,  "weight": 1.0},
    "Dragon Scale":       {"type": "material",   "effect": None,     "value": 0,   "gold": 200, "weight": 2.0},
    "Wood Plank":         {"type": "material",   "effect": None,     "value": 0,   "gold": 3,   "weight": 0.5},
    "Leather":            {"type": "material",   "effect": None,     "value": 0,   "gold": 8,   "weight": 0.5},
    "Silk":               {"type": "material",   "effect": None,     "value": 0,   "gold": 12,  "weight": 0.1},
    "Thread":             {"type": "material",   "effect": None,     "value": 0,   "gold": 2,   "weight": 0.1},
    "Gunpowder":          {"type": "material",   "effect": None,     "value": 0,   "gold": 10,  "weight": 0.3},
    "Rabbit Foot":        {"type": "material",   "effect": None,     "value": 0,   "gold": 18,  "weight": 0.1},
    "Gold Dust":          {"type": "material",   "effect": None,     "value": 0,   "gold": 50,  "weight": 0.1},
    "Phoenix Feather":    {"type": "material",   "effect": None,     "value": 0,   "gold": 300, "weight": 0.2},
    "Holy Water":         {"type": "material",   "effect": None,     "value": 0,   "gold": 40,  "weight": 0.5},
    "Lucky Charm":        {"type": "accessory",  "effect": "luck",   "value": 5,   "gold": 80,  "weight": 0.2},
    "Iron Sword":         {"type": "weapon",     "wtype": "Sword",   "tier": 2,    "gold": 80,  "weight": 3.0},
    "Steel Shield":       {"type": "armor",      "atype": "Splint",  "tier": 2,    "gold": 100, "weight": 5.0},
    "Mage Robe":          {"type": "armor",      "atype": "Robe",    "tier": 2,    "gold": 90,  "weight": 1.0},
    "Phoenix Feather Cloak":{"type": "armor",    "atype": "Cloth",   "tier": 5,    "gold": 2000,"weight": 0.8},
}

QUEST_DATABASE = {
    "The First Step": {
        "giver": "Elder Aldric",
        "level_req": 1,
        "desc": "Prove yourself by defeating 3 Goblins near the village.",
        "objectives": [{"type": "kill", "target": "Goblin", "count": 3, "done": 0}],
        "reward_xp": 100, "reward_gold": 50,
        "reward_items": ["Health Potion"],
        "next_quest": "Into the Dark",
    },
    "Into the Dark": {
        "giver": "Elder Aldric",
        "level_req": 2,
        "desc": "Enter the Dark Forest and slay the Alpha Wolf.",
        "objectives": [{"type": "kill", "target": "Wolf", "count": 5, "done": 0}],
        "reward_xp": 250, "reward_gold": 100,
        "reward_items": ["Mana Potion", "Antidote"],
        "next_quest": "The Bandit Problem",
    },
    "The Bandit Problem": {
        "giver": "Captain Vera",
        "level_req": 4,
        "desc": "Clear the road of bandits threatening the merchants.",
        "objectives": [{"type": "kill", "target": "Bandit", "count": 8, "done": 0}],
        "reward_xp": 500, "reward_gold": 200,
        "reward_items": ["Iron Sword"],
        "next_quest": "Rise of the Lich",
    },
    "Rise of the Lich": {
        "giver": "Archmage Seriva",
        "level_req": 8,
        "desc": "A lich has risen in the northern crypts. Stop it before it assembles an army.",
        "objectives": [{"type": "kill", "target": "Lich", "count": 1, "done": 0}],
        "reward_xp": 2000, "reward_gold": 500,
        "reward_items": ["Elixir of Power"],
        "next_quest": "Dragon's Wrath",
    },
    "Dragon's Wrath": {
        "giver": "King Doran",
        "level_req": 15,
        "desc": "The ancient Dragon Ignarath has returned. Only you can slay it.",
        "objectives": [{"type": "kill", "target": "Dragon", "count": 1, "done": 0}],
        "reward_xp": 10000, "reward_gold": 2000,
        "reward_items": ["Phoenix Feather Cloak"],
        "next_quest": None,
    },
    "Herb Collector": {
        "giver": "Healer Mira",
        "level_req": 1,
        "desc": "Bring 5 Red Herbs and 5 Blue Herbs to the healer.",
        "objectives": [
            {"type": "gather", "target": "Red Herb",  "count": 5, "done": 0},
            {"type": "gather", "target": "Blue Herb",  "count": 5, "done": 0},
        ],
        "reward_xp": 80, "reward_gold": 40,
        "reward_items": ["Health Potion", "Mana Potion"],
        "next_quest": None,
    },
    "Lost Amulet": {
        "giver": "Merchant Pol",
        "level_req": 3,
        "desc": "Find the Merchant's lost amulet stolen by bandits.",
        "objectives": [{"type": "find", "target": "Amulet of Pol", "count": 1, "done": 0}],
        "reward_xp": 200, "reward_gold": 150,
        "reward_items": ["Lucky Charm"],
        "next_quest": None,
    },
}

WORLD_MAP_TEMPLATE = [
    "~~~~~~~~~~~~~~~~~~~~",
    "~~~~TTTTTT~~MMMM~~~~",
    "~~~TTVVTTTT~MMMM~~~~",
    "~~TTTV..VTTTMMM~~~~~",
    "~~TT...S..TTMM~~~~~~",
    "~~~TT.....TT~MM~~~~~",
    "~~~~T..C..T~~MM~~~~~",
    "~~~~~T....T~~~M~~~~~",
    "~~~~~T..F.T~~~~~~~~~",
    "~~~~TT.D..TT~~~~~~~~",
    "~~~TTT....TTTT~~~~~~",
    "~~~~TT...BBBT~~~~~~~",
    "~~~~~T..BBBBT~~~~~~~",
    "~~~~~~TBBBBB~~~~~~~~",
    "~~~~~~~~~~~~~~~~~~~~",
]

MAP_LEGEND = {
    "~": ("Ocean",       ANSI_BLUE,    False),
    "T": ("Forest",      ANSI_GREEN,   True),
    "M": ("Mountains",   ANSI_GRAY,    True),
    "V": ("Village",     ANSI_YELLOW,  True),
    ".": ("Plains",      ANSI_WHITE,   True),
    "S": ("Starting Town",ANSI_CYAN,   True),
    "C": ("Castle",      ANSI_MAGENTA, True),
    "D": ("Dungeon",     ANSI_RED,     True),
    "F": ("Forest Temple",ANSI_GREEN,  True),
    "B": ("Badlands",    ANSI_RED,     True),
}

NPC_DIALOGUE = {
    "Elder Aldric": {
        "greeting": "Ah, adventurer! The realm has need of brave souls like yourself.",
        "quest_prompt": "Would you be willing to help rid our lands of the goblin menace?",
        "after_quest": "You have done well. The village sleeps safer thanks to you.",
        "lore": "These lands were once united under the Shattered Crown before the Cataclysm split them.",
    },
    "Captain Vera": {
        "greeting": "Hmm. You don't look like a bandit. State your business.",
        "quest_prompt": "The northern road is overrun. Clear it and you'll be well rewarded.",
        "after_quest": "The merchants travel safely again. You have my thanks.",
        "lore": "The bandits serve a warlord called Ironmask. Nobody knows his real face.",
    },
    "Archmage Seriva": {
        "greeting": "The arcane flows strangely today... ah, a visitor.",
        "quest_prompt": "Necromantic energy radiates from the northern crypts. This is dire.",
        "after_quest": "The lich is vanquished. But the one who raised it may still be out there...",
        "lore": "Lich-craft requires a phylactery — a vessel for the soul. Destroy it to truly kill a lich.",
    },
    "King Doran": {
        "greeting": "Rise, hero. These are dark times for my kingdom.",
        "quest_prompt": "The dragon Ignarath scorches my northern provinces. I need a champion.",
        "after_quest": "You have saved us all. Kneel, so I may name you Champion of the Realm.",
        "lore": "Ignarath slept for three centuries. Something woke him. We do not know what.",
    },
    "Healer Mira": {
        "greeting": "Oh! You startled me. Welcome to my clinic, traveller.",
        "quest_prompt": "My herb stores are dangerously low. Can you gather some for me?",
        "after_quest": "Thank you! With these herbs I can treat a dozen patients.",
        "lore": "Red herbs close wounds, blue ones restore vitality. Green herbs are nature's antidote.",
    },
    "Merchant Pol": {
        "greeting": "Buy something or move along — wait, you look like you handle yourself well.",
        "quest_prompt": "Those cursed bandits took my family amulet. I'll pay handsomely for its return.",
        "after_quest": "My grandmother's amulet! You have no idea what this means to me.",
        "lore": "I've been trading these roads for twenty years. Never seen times this bad.",
    },
    "Blacksmith Torva": {
        "greeting": "Need something forged? Torva's hammer never rests.",
        "lore": "Best steel comes from Ironvale ore. Rare, but I know a supplier.",
    },
    "Innkeeper Bessa": {
        "greeting": "Welcome to the Tattered Flagon! Rest your weary bones.",
        "lore": "I hear the adventurers talking at night. Strange things stir in the western mountains.",
    },
}

TAVERN_RUMORS = [
    "They say a dragon was spotted circling the northern peaks last full moon.",
    "The mines near Deephold have gone quiet — no news from the workers in a week.",
    "A fortune teller arrived in town. She speaks of a shattered crown that will unite the realm.",
    "Three caravans vanished on the eastern road. Bandits, or something worse?",
    "The old lighthouse has started lighting itself at night. Nobody lives there anymore.",
    "I heard a knight killed a hydra single-handedly near the marshes. Probably just a story.",
    "Crops to the west have been dying without reason. The druids are worried.",
    "A stranger paid for a year's lodging in advance — in pure gold coins. Never seen denominations like those.",
    "The river runs red after heavy rain now. The elders say it's an ill omen.",
    "There's treasure buried under the old chapel, if you believe the map old Petra has.",
    "Count Aldor hasn't been seen in public for six months. His chamberlain speaks for him now.",
    "The thieves' guild is recruiting. Not that I'd know anything about that, mind you.",
]

LOOT_TABLES = {
    "common":    ["Red Herb", "Blue Herb", "Green Herb", "Empty Vial", "Wood Plank"],
    "uncommon":  ["Iron Ingot", "Leather", "Thread", "Gunpowder", "Health Potion"],
    "rare":      ["Steel Ingot", "Silk", "Gold Dust", "Rabbit Foot", "Mana Potion"],
    "epic":      ["Dragon Scale", "Phoenix Feather", "Holy Water", "Elixir of Power"],
    "legendary": ["Phoenix Feather Cloak", "Lucky Charm"],
}

RANDOM_ENCOUNTER_MESSAGES = [
    "You hear rustling in the bushes...",
    "A shadow detaches itself from the treeline.",
    "You step on a branch — something looks up.",
    "A bloodcurdling howl echoes through the forest.",
    "The ground ahead shifts unnaturally.",
    "Eyes glint from the darkness.",
    "You smell smoke and old blood.",
    "An arrow embeds itself in the tree beside you.",
]

VICTORY_QUOTES = [
    "Another foe bites the dust.",
    "Victory belongs to the persistent.",
    "The battlefield is yours.",
    "You stand triumphant.",
    "Your blade has proven its worth today.",
    "The enemy is defeated.",
    "Well fought. Now loot them.",
    "Fortune favours the bold.",
]

DEATH_QUOTES = [
    "You collapse, your vision fading to black...",
    "The world grows dark as you fall.",
    "Your strength gives out at last.",
    "Even heroes fall. The story continues.",
    "A brave end to a brave journey.",
]

LEVEL_UP_QUOTES = [
    "Power surges through your veins!",
    "Your training pays off!",
    "The realm grows easier to handle.",
    "You feel a new strength awakening.",
    "Battle-hardened and wiser than before.",
]

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3: ENTITY CLASSES
# ─────────────────────────────────────────────────────────────────────────────

class Stats:
    """Container for character statistics."""
    def __init__(self, str_=10, dex=10, int_=10, wis=10, con=10, lck=10):
        self.str = str_
        self.dex = dex
        self.int = int_
        self.wis = wis
        self.con = con
        self.lck = lck

    def modifier(self, stat_name):
        val = getattr(self, stat_name, 10)
        return (val - 10) // 2

    def to_dict(self):
        return {"str": self.str, "dex": self.dex, "int": self.int,
                "wis": self.wis, "con": self.con, "lck": self.lck}

    @classmethod
    def from_dict(cls, d):
        return cls(d["str"], d["dex"], d["int"], d["wis"], d["con"], d["lck"])

    def apply_bonuses(self, bonus_dict):
        for key, val in bonus_dict.items():
            current = getattr(self, key, 0)
            setattr(self, key, current + val)

    def display(self):
        labels = {"str": "Strength", "dex": "Dexterity", "int": "Intelligence",
                  "wis": "Wisdom", "con": "Constitution", "lck": "Luck"}
        for key, label in labels.items():
            val = getattr(self, key)
            mod = self.modifier(key)
            sign = "+" if mod >= 0 else ""
            bar = "▮" * (val // 2) + "▯" * (10 - val // 2)
            print(f"  {label:<14} {val:>3}  [{bar}]  ({sign}{mod})")


class StatusEffect:
    """Represents a temporary status effect on an entity."""
    def __init__(self, name, duration, intensity=1, element=None):
        self.name = name
        self.duration = duration
        self.intensity = intensity
        self.element = element
        self.tick_count = 0

    def is_expired(self):
        return self.duration <= 0

    def tick(self):
        self.duration -= 1
        self.tick_count += 1

    def apply(self, entity):
        if self.name == "burn":
            dmg = roll_dice(4, 1, self.intensity)
            entity.take_damage(dmg, "fire", is_dot=True)
            return f"{entity.name} burns for {dmg} fire damage!"
        if self.name == "poison":
            dmg = roll_dice(3, 1, self.intensity)
            entity.take_damage(dmg, "poison", is_dot=True)
            return f"{entity.name} takes {dmg} poison damage!"
        if self.name == "bleed":
            dmg = roll_dice(2, 1, self.intensity)
            entity.take_damage(dmg, "physical", is_dot=True)
            return f"{entity.name} bleeds for {dmg} damage!"
        if self.name == "regen":
            heal = roll_dice(4, 1, self.intensity)
            entity.heal(heal)
            return f"{entity.name} regenerates {heal} HP!"
        if self.name == "freeze":
            return f"{entity.name} is frozen solid!"
        if self.name == "stun":
            return f"{entity.name} is stunned!"
        if self.name == "paralyze":
            return f"{entity.name} is paralyzed!"
        if self.name == "blind":
            return f"{entity.name} stumbles blindly!"
        if self.name == "slow":
            return f"{entity.name} moves sluggishly."
        if self.name == "haste":
            return f"{entity.name} moves with blinding speed!"
        if self.name == "shield":
            return f"{entity.name}'s barrier holds."
        if self.name == "berserk":
            return f"{entity.name} fights with savage fury!"
        return ""

    def to_dict(self):
        return {"name": self.name, "duration": self.duration,
                "intensity": self.intensity, "element": self.element}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["duration"], d.get("intensity", 1), d.get("element"))


class Inventory:
    """Manages items carried by an entity."""
    def __init__(self, max_slots=MAX_INVENTORY_SLOTS):
        self.max_slots = max_slots
        self.items = collections.OrderedDict()
        self.gold = 0

    def add_item(self, name, count=1):
        if name in self.items:
            self.items[name] += count
            return True
        if len(self.items) < self.max_slots:
            self.items[name] = count
            return True
        return False

    def remove_item(self, name, count=1):
        if name not in self.items or self.items[name] < count:
            return False
        self.items[name] -= count
        if self.items[name] == 0:
            del self.items[name]
        return True

    def has_item(self, name, count=1):
        return self.items.get(name, 0) >= count

    def count_item(self, name):
        return self.items.get(name, 0)

    def total_weight(self):
        total = 0.0
        for name, count in self.items.items():
            defn = ITEM_DEFINITIONS.get(name, {})
            total += defn.get("weight", 0.5) * count
        return total

    def display(self, page=0, per_page=10):
        print_header("INVENTORY")
        print(f"  Gold: {colored(str(self.gold), ANSI_YELLOW)} | Slots: {len(self.items)}/{self.max_slots} | Weight: {self.total_weight():.1f} kg")
        print_divider()
        item_list = list(self.items.items())
        start = page * per_page
        end = start + per_page
        if not item_list:
            print(colored("  (empty)", ANSI_GRAY))
        for i, (name, count) in enumerate(item_list[start:end], start=1):
            defn = ITEM_DEFINITIONS.get(name, {})
            itype = defn.get("type", "misc")
            gold = defn.get("gold", 0)
            print(f"  {i+start:>2}. {name:<28} x{count:<4} [{itype}]  {gold}g each")
        total_pages = math.ceil(len(item_list) / per_page)
        if total_pages > 1:
            print(f"\n  Page {page+1}/{total_pages}")

    def to_dict(self):
        return {"items": dict(self.items), "gold": self.gold}

    @classmethod
    def from_dict(cls, d):
        inv = cls()
        inv.items = collections.OrderedDict(d.get("items", {}))
        inv.gold = d.get("gold", 0)
        return inv


class Equipment:
    """Manages equipped items on an entity."""
    SLOTS = ["weapon", "armor", "helmet", "boots", "gloves", "ring", "amulet", "offhand"]

    def __init__(self):
        self.slots = {slot: None for slot in self.SLOTS}

    def equip(self, slot, item_name):
        if slot not in self.slots:
            return False
        old = self.slots[slot]
        self.slots[slot] = item_name
        return old

    def unequip(self, slot):
        if slot not in self.slots:
            return None
        item = self.slots[slot]
        self.slots[slot] = None
        return item

    def defense_total(self):
        total = 0
        for item_name in self.slots.values():
            if item_name:
                defn = ITEM_DEFINITIONS.get(item_name, {})
                if defn.get("type") == "armor":
                    atype = defn.get("atype", "Cloth")
                    tier = defn.get("tier", 1)
                    base_def = ARMOR_TYPES.get(atype, {}).get("defense", 0)
                    total += int(base_def * TIER_MULTIPLIERS.get(tier, 1.0))
        return total

    def weapon_stats(self):
        wname = self.slots.get("weapon")
        if not wname:
            return {"dmg_dice": 4, "dmg_count": 1, "bonus": 0, "crit": 20, "range": "melee"}
        defn = ITEM_DEFINITIONS.get(wname, {})
        wtype = defn.get("wtype", "Sword")
        tier = defn.get("tier", 1)
        base = WEAPON_TYPES.get(wtype, WEAPON_TYPES["Sword"]).copy()
        base["bonus"] += int((TIER_MULTIPLIERS.get(tier, 1.0) - 1) * 3)
        return base

    def display(self):
        print_header("EQUIPMENT")
        for slot in self.SLOTS:
            item = self.slots[slot]
            display_item = item if item else colored("(empty)", ANSI_GRAY)
            print(f"  {slot.capitalize():<10}: {display_item}")

    def to_dict(self):
        return {"slots": self.slots.copy()}

    @classmethod
    def from_dict(cls, d):
        eq = cls()
        eq.slots = d.get("slots", {slot: None for slot in cls.SLOTS})
        return eq


class Entity:
    """Base class for all living entities in the game."""
    def __init__(self, name, level=1):
        self.name = name
        self.level = level
        self.stats = Stats()
        self.status_effects = []
        self.is_alive = True

    def max_hp(self):
        return 10 + (self.level * 5) + (self.stats.con * 3)

    def max_mp(self):
        return 10 + (self.level * 3) + (self.stats.int * 2)

    def take_damage(self, amount, dmg_type="physical", is_dot=False):
        amount = max(0, int(amount))
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.is_alive = False
        return amount

    def heal(self, amount):
        amount = max(0, int(amount))
        self.hp = min(self.max_hp(), self.hp + amount)
        return amount

    def restore_mp(self, amount):
        amount = max(0, int(amount))
        self.mp = min(self.max_mp(), self.mp + amount)
        return amount

    def add_status(self, effect):
        for existing in self.status_effects:
            if existing.name == effect.name:
                existing.duration = max(existing.duration, effect.duration)
                return
        self.status_effects.append(effect)

    def has_status(self, name):
        return any(e.name == name for e in self.status_effects)

    def remove_status(self, name):
        self.status_effects = [e for e in self.status_effects if e.name != name]

    def tick_status_effects(self):
        messages = []
        for effect in list(self.status_effects):
            msg = effect.apply(self)
            if msg:
                messages.append(msg)
            effect.tick()
        self.status_effects = [e for e in self.status_effects if not e.is_expired()]
        return messages

    def is_incapacitated(self):
        return self.has_status("stun") or self.has_status("freeze") or self.has_status("paralyze")

    def attack_roll(self):
        wpn = getattr(self, 'equipment', None)
        stats = self.stats
        if wpn:
            ws = wpn.weapon_stats()
            dmg = roll_dice(ws["dmg_dice"], ws["dmg_count"], ws["bonus"])
            dmg += stats.modifier("str")
            crit_threshold = ws.get("crit", 20)
            roll = random.randint(1, 20)
            is_crit = roll >= crit_threshold
            if is_crit:
                dmg = int(dmg * CRITICAL_HIT_MULTIPLIER)
            return dmg, is_crit
        dmg = roll_dice(4, 1, stats.modifier("str"))
        is_crit = random.randint(1, 20) == 20
        if is_crit:
            dmg = int(dmg * CRITICAL_HIT_MULTIPLIER)
        return max(1, dmg), is_crit

    def dodge_chance(self):
        return clamp(DODGE_BASE_CHANCE + self.stats.modifier("dex") * 2, 0, 75)

    def attempt_dodge(self):
        return percentage_chance(self.dodge_chance())


class Monster(Entity):
    """Represents an enemy monster."""
    def __init__(self, family, level=1, variant=None):
        super().__init__(family, level)
        template = MONSTER_FAMILIES.get(family, MONSTER_FAMILIES["Goblin"])
        scale = 1 + (level - 1) * 0.15
        self.family = family
        self.variant = variant
        self.icon = template["icon"]
        self.stats.str = int(template["str"] * scale)
        self.stats.dex = int(template["dex"] * scale)
        self.stats.int = int(template["int"] * scale)
        self.stats.con = int(5 * scale)
        self.stats.wis = 5
        self.stats.lck = 5
        self.hp = int(template["hp"] * scale)
        self.mp = 20
        self.max_hp_val = self.hp
        self.base_xp = int(template["xp"] * scale)
        self.gold_range = template["gold"]
        self.loot_tier = self._determine_loot_tier()
        self.ai_style = self._choose_ai()
        self.abilities = self._assign_abilities()

    def _determine_loot_tier(self):
        if self.family in ["Dragon", "Lich"]:   return "epic"
        if self.family in ["Vampire", "Golem"]: return "rare"
        if self.family in ["Orc", "Minotaur"]:  return "uncommon"
        return "common"

    def _choose_ai(self):
        styles = ["aggressive", "cautious", "berserker", "defensive", "spellcaster"]
        return random.choice(styles)

    def _assign_abilities(self):
        pool = []
        if self.family == "Dragon":
            pool = ["Breathe Fire", "Tail Swipe", "Wing Gust"]
        elif self.family == "Lich":
            pool = ["Death Bolt", "Summon Undead", "Soul Drain"]
        elif self.family == "Vampire":
            pool = ["Life Drain", "Mesmerize", "Bat Swarm"]
        elif self.family == "Witch":
            pool = ["Hex", "Poison Cloud", "Cackling Curse"]
        elif self.family == "Mermaid":
            pool = ["Tidal Wave", "Enchant", "Whirlpool"]
        else:
            pool = ["Power Strike", "Enrage"]
        return pool

    def max_hp(self):
        return self.max_hp_val

    def choose_action(self, player):
        if not self.is_alive:
            return "dead"
        if self.is_incapacitated():
            return "skip"
        hp_pct = self.hp / self.max_hp_val
        if self.ai_style == "aggressive":
            if self.abilities and percentage_chance(35):
                return ("ability", random.choice(self.abilities))
            return "attack"
        if self.ai_style == "cautious":
            if hp_pct < 0.35 and percentage_chance(50):
                return "flee"
            if self.abilities and percentage_chance(20):
                return ("ability", random.choice(self.abilities))
            return "attack"
        if self.ai_style == "berserker":
            if hp_pct < 0.4:
                return "double_attack"
            return "attack"
        if self.ai_style == "defensive":
            if hp_pct < 0.5 and percentage_chance(30):
                return "defend"
            return "attack"
        if self.ai_style == "spellcaster":
            if self.abilities and percentage_chance(55):
                return ("ability", random.choice(self.abilities))
            return "attack"
        return "attack"

    def drop_loot(self):
        drops = {}
        tier = self.loot_tier
        table = LOOT_TABLES.get(tier, LOOT_TABLES["common"])
        num_drops = random.randint(0, 2)
        for _ in range(num_drops):
            item = random.choice(table)
            drops[item] = drops.get(item, 0) + 1
        gold = random.randint(*self.gold_range)
        return drops, gold

    def to_dict(self):
        return {
            "family": self.family, "level": self.level, "hp": self.hp,
            "mp": self.mp, "is_alive": self.is_alive,
            "status_effects": [e.to_dict() for e in self.status_effects],
        }


class Player(Entity):
    """Represents the player character."""
    def __init__(self, name, race, char_class):
        super().__init__(name, level=1)
        self.race = race
        self.char_class = char_class
        self.hp = self.max_hp()
        self.mp = self.max_mp()
        self.xp = 0
        self.total_xp = 0
        self.stat_points = 0
        self.skill_points = 0
        self.crafting_level = 0
        self.inventory = Inventory()
        self.equipment = Equipment()
        self.known_spells = ["Arcane Missile", "Heal"]
        self.active_quests = {}
        self.completed_quests = []
        self.world_x = 9
        self.world_y = 4
        self.play_time = 0
        self.kills = collections.Counter()
        self.deaths = 0
        self.achievements = []
        self.reputation = collections.defaultdict(int)
        self.dialogue_states = {}
        self.journal = []
        self.crafted_items = 0
        self.spells_cast = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        self.gold_earned = 0
        self.steps_taken = 0
        self._apply_race_and_class()
        self.hp = self.max_hp()
        self.mp = CLASS_MP_BASE.get(char_class, 40)

    def _apply_race_and_class(self):
        race_b  = RACE_BONUSES.get(self.race, {})
        class_b = CLASS_BONUSES.get(self.char_class, {})
        self.stats.apply_bonuses(race_b)
        self.stats.apply_bonuses(class_b)

    def max_hp(self):
        dice = CLASS_HP_DICE.get(self.char_class, 8)
        return dice + (self.level - 1) * (dice // 2) + self.stats.con * 3

    def max_mp(self):
        base = CLASS_MP_BASE.get(self.char_class, 40)
        return base + (self.level - 1) * 5 + self.stats.int * 2

    def xp_to_next_level(self):
        return int(BASE_XP_PER_LEVEL * (XP_SCALE_FACTOR ** (self.level - 1)))

    def gain_xp(self, amount):
        self.xp += amount
        self.total_xp += amount
        leveled_up = False
        while self.xp >= self.xp_to_next_level() and self.level < MAX_LEVEL:
            self.xp -= self.xp_to_next_level()
            self.level += 1
            self.stat_points += 3
            self.skill_points += 1
            leveled_up = True
            old_hp = self.max_hp()
            # Re-calc hp after level
            hp_gain = CLASS_HP_DICE.get(self.char_class, 8) // 2 + self.stats.modifier("con")
            self.hp = min(self.max_hp(), self.hp + hp_gain)
            self.mp = self.max_mp()
        return leveled_up

    def level_up_menu(self):
        print_header(f"LEVEL UP! You are now Level {self.level}!")
        print(colored(f"  {random.choice(LEVEL_UP_QUOTES)}", ANSI_YELLOW))
        print(f"  Stat Points to allocate: {self.stat_points}")
        stat_names = ["str", "dex", "int", "wis", "con", "lck"]
        stat_labels = ["Strength", "Dexterity", "Intelligence", "Wisdom", "Constitution", "Luck"]
        while self.stat_points > 0:
            print(f"\n  Current stats:")
            self.stats.display()
            print(f"\n  Points remaining: {self.stat_points}")
            choice = ask("Allocate point to (str/dex/int/wis/con/lck)", stat_names)
            setattr(self.stats, choice, getattr(self.stats, choice) + 1)
            self.stat_points -= 1
        self._unlock_new_spells()

    def _unlock_new_spells(self):
        newly_learned = []
        for spell_name, spell in SPELL_BOOK.items():
            if spell["level_req"] <= self.level and spell_name not in self.known_spells:
                self.known_spells.append(spell_name)
                newly_learned.append(spell_name)
        if newly_learned:
            print(colored(f"\n  New spells learned: {', '.join(newly_learned)}", ANSI_CYAN))

    def add_quest(self, quest_name):
        if quest_name in QUEST_DATABASE and quest_name not in self.active_quests:
            q = copy.deepcopy(QUEST_DATABASE[quest_name])
            self.active_quests[quest_name] = q
            self.journal.append(f"Quest accepted: {quest_name}")
            print(colored(f"\n  Quest Added: {quest_name}", ANSI_GREEN))
            return True
        return False

    def update_kill_quest(self, target_name):
        for qname, quest in self.active_quests.items():
            for obj in quest["objectives"]:
                if obj["type"] == "kill" and obj["target"] == target_name:
                    if obj["done"] < obj["count"]:
                        obj["done"] += 1

    def check_quest_completion(self):
        completed = []
        for qname, quest in list(self.active_quests.items()):
            if all(obj["done"] >= obj["count"] for obj in quest["objectives"]):
                completed.append(qname)
        return completed

    def complete_quest(self, qname):
        if qname not in self.active_quests:
            return
        quest = self.active_quests.pop(qname)
        self.completed_quests.append(qname)
        self.journal.append(f"Quest completed: {qname}")
        print_header(f"QUEST COMPLETE: {qname}")
        leveled = self.gain_xp(quest["reward_xp"])
        print(colored(f"  +{quest['reward_xp']} XP!", ANSI_YELLOW))
        self.inventory.gold += quest["reward_gold"]
        self.gold_earned += quest["reward_gold"]
        print(colored(f"  +{quest['reward_gold']} Gold!", ANSI_YELLOW))
        for item in quest.get("reward_items", []):
            self.inventory.add_item(item)
            print(colored(f"  Received: {item}", ANSI_GREEN))
        if leveled:
            self.level_up_menu()
        nq = quest.get("next_quest")
        if nq and nq in QUEST_DATABASE:
            print(colored(f"\n  New quest available: {nq}", ANSI_CYAN))

    def display_status(self):
        print_header(f"{self.name}  [{self.race} {self.char_class}]  Lv.{self.level}")
        print(f"  HP   {health_bar(self.hp, self.max_hp())}")
        print(f"  MP   {mana_bar(self.mp, self.max_mp())}")
        print(f"  XP   {xp_bar(self.xp, self.xp_to_next_level())}")
        print(f"  Gold {colored(str(self.inventory.gold), ANSI_YELLOW)}")
        print(f"  Location: ({self.world_x}, {self.world_y})")
        if self.status_effects:
            effects = ", ".join(colored(e.name, ANSI_MAGENTA) for e in self.status_effects)
            print(f"  Status: {effects}")
        print_divider()
        self.stats.display()

    def display_quests(self):
        print_header("QUEST LOG")
        if not self.active_quests and not self.completed_quests:
            print(colored("  No quests recorded.", ANSI_GRAY))
            return
        if self.active_quests:
            print(colored("  ACTIVE QUESTS:", ANSI_YELLOW))
            for qname, quest in self.active_quests.items():
                print(f"  ● {qname}")
                print(f"    {quest['desc']}")
                for obj in quest["objectives"]:
                    bar_w = 10
                    done  = obj["done"]
                    total = obj["count"]
                    filled = int((done / total) * bar_w)
                    prog = "█" * filled + "░" * (bar_w - filled)
                    print(f"    [{prog}] {done}/{total} {obj['target']}")
        if self.completed_quests:
            print(colored("\n  COMPLETED QUESTS:", ANSI_GREEN))
            for qname in self.completed_quests:
                print(f"  ✓ {qname}")

    def display_spellbook(self):
        print_header("SPELLBOOK")
        if not self.known_spells:
            print(colored("  No spells known.", ANSI_GRAY))
            return
        for sp_name in self.known_spells:
            sp = SPELL_BOOK.get(sp_name, {})
            cost = sp.get("cost", 0)
            elem = sp.get("element", "?")
            school = sp.get("school", "?")
            desc = sp.get("desc", "")
            lvl_req = sp.get("level_req", 1)
            print(f"  {sp_name:<22} [{elem.capitalize():<10}] MP:{cost:<4} Lv.{lvl_req}  ({school})")
            print(f"    {colored(desc, ANSI_GRAY)}")

    def rest(self, hours=8):
        heal_amount = int(self.max_hp() * 0.3 * hours / 8)
        mp_amount   = int(self.max_mp() * 0.5 * hours / 8)
        self.hp = min(self.max_hp(), self.hp + heal_amount)
        self.mp = min(self.max_mp(), self.mp + mp_amount)
        self.status_effects = [e for e in self.status_effects
                                if e.name not in ["burn", "bleed", "poison"]]
        print(colored(f"  You rest for {hours} hours... HP +{heal_amount}, MP +{mp_amount}", ANSI_GREEN))

    def to_dict(self):
        return {
            "name": self.name, "race": self.race, "char_class": self.char_class,
            "level": self.level, "hp": self.hp, "mp": self.mp,
            "xp": self.xp, "total_xp": self.total_xp,
            "stat_points": self.stat_points, "skill_points": self.skill_points,
            "crafting_level": self.crafting_level,
            "stats": self.stats.to_dict(),
            "inventory": self.inventory.to_dict(),
            "equipment": self.equipment.to_dict(),
            "known_spells": self.known_spells,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
            "world_x": self.world_x, "world_y": self.world_y,
            "play_time": self.play_time,
            "kills": dict(self.kills),
            "deaths": self.deaths,
            "achievements": self.achievements,
            "reputation": dict(self.reputation),
            "dialogue_states": self.dialogue_states,
            "journal": self.journal,
            "crafted_items": self.crafted_items,
            "spells_cast": self.spells_cast,
            "damage_dealt": self.damage_dealt,
            "damage_taken": self.damage_taken,
            "gold_earned": self.gold_earned,
            "steps_taken": self.steps_taken,
            "status_effects": [e.to_dict() for e in self.status_effects],
        }

    @classmethod
    def from_dict(cls, d):
        p = cls(d["name"], d["race"], d["char_class"])
        p.level = d["level"]
        p.hp = d["hp"]
        p.mp = d["mp"]
        p.xp = d["xp"]
        p.total_xp = d.get("total_xp", 0)
        p.stat_points = d.get("stat_points", 0)
        p.skill_points = d.get("skill_points", 0)
        p.crafting_level = d.get("crafting_level", 0)
        p.stats = Stats.from_dict(d["stats"])
        p.inventory = Inventory.from_dict(d["inventory"])
        p.equipment = Equipment.from_dict(d["equipment"])
        p.known_spells = d.get("known_spells", ["Arcane Missile"])
        p.active_quests = d.get("active_quests", {})
        p.completed_quests = d.get("completed_quests", [])
        p.world_x = d.get("world_x", 9)
        p.world_y = d.get("world_y", 4)
        p.play_time = d.get("play_time", 0)
        p.kills = collections.Counter(d.get("kills", {}))
        p.deaths = d.get("deaths", 0)
        p.achievements = d.get("achievements", [])
        p.reputation = collections.defaultdict(int, d.get("reputation", {}))
        p.dialogue_states = d.get("dialogue_states", {})
        p.journal = d.get("journal", [])
        p.crafted_items = d.get("crafted_items", 0)
        p.spells_cast = d.get("spells_cast", 0)
        p.damage_dealt = d.get("damage_dealt", 0)
        p.damage_taken = d.get("damage_taken", 0)
        p.gold_earned = d.get("gold_earned", 0)
        p.steps_taken = d.get("steps_taken", 0)
        p.status_effects = [StatusEffect.from_dict(e) for e in d.get("status_effects", [])]
        return p

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4: COMBAT SYSTEM
# ─────────────────────────────────────────────────────────────────────────────

class CombatLog:
    """Stores and displays combat messages."""
    def __init__(self, max_lines=8):
        self.lines = []
        self.max_lines = max_lines

    def add(self, msg, color=ANSI_WHITE):
        self.lines.append(colored(msg, color))
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def display(self):
        print_divider()
        for line in self.lines:
            print(f"  {line}")
        print_divider()


class BattleRenderer:
    """Handles rendering the battle screen."""
    @staticmethod
    def render(player, monsters, turn, log):
        clear_screen()
        print_header(f"⚔  BATTLE  ⚔  Turn {turn}")

        # Player panel
        print(f"  {colored(player.name, ANSI_CYAN)}  Lv.{player.level}")
        print(f"  HP  {health_bar(player.hp, player.max_hp())}")
        print(f"  MP  {mana_bar(player.mp, player.max_mp())}")
        if player.status_effects:
            names = [colored(e.name, ANSI_MAGENTA) for e in player.status_effects]
            print(f"  ◈   {', '.join(names)}")

        print_divider()

        # Enemy panels
        for i, m in enumerate(monsters):
            if m.is_alive:
                status_str = ""
                if m.status_effects:
                    status_str = " [" + ",".join(e.name for e in m.status_effects) + "]"
                hp_pct = m.hp / m.max_hp_val
                color = ANSI_GREEN if hp_pct > 0.6 else ANSI_YELLOW if hp_pct > 0.3 else ANSI_RED
                bar = health_bar(m.hp, m.max_hp_val, 15)
                print(f"  {i+1}. {m.icon} {colored(m.name, color)}  Lv.{m.level}{status_str}")
                print(f"     {bar}")
            else:
                print(f"  {i+1}. {colored(m.name + ' [DEAD]', ANSI_GRAY)}")

        log.display()


def player_combat_turn(player, monsters, log):
    """Handle player's turn in combat."""
    alive_monsters = [m for m in monsters if m.is_alive]
    if not alive_monsters:
        return "win"

    if player.is_incapacitated():
        log.add(f"{player.name} is incapacitated and cannot act!", ANSI_YELLOW)
        return "continue"

    print(colored("\n  YOUR TURN:", ANSI_CYAN))
    print("  [1] Attack   [2] Magic   [3] Item   [4] Flee   [5] Defend   [6] Inspect")
    choice = ask("Action", ["1", "2", "3", "4", "5", "6"])

    if choice == "1":
        return _player_attack(player, alive_monsters, log)
    elif choice == "2":
        return _player_magic(player, alive_monsters, log)
    elif choice == "3":
        return _player_use_item(player, log)
    elif choice == "4":
        return _player_flee(player, log)
    elif choice == "5":
        return _player_defend(player, log)
    elif choice == "6":
        return _player_inspect(alive_monsters, log)
    return "continue"


def _player_attack(player, alive_monsters, log):
    if len(alive_monsters) == 1:
        target = alive_monsters[0]
    else:
        print("  Target: " + "  ".join(f"[{i+1}] {m.name}" for i, m in enumerate(alive_monsters)))
        idx = int(ask("Choose target", [str(i+1) for i in range(len(alive_monsters))])) - 1
        target = alive_monsters[idx]

    if target.attempt_dodge():
        log.add(f"{target.name} dodged your attack!", ANSI_YELLOW)
        return "continue"

    dmg, is_crit = player.attack_roll()
    defense = 0
    if hasattr(target, "defending") and target.defending:
        dmg = dmg // 2
    actual = target.take_damage(dmg, "physical")
    player.damage_dealt += actual
    crit_msg = colored(" CRITICAL HIT!", ANSI_RED) if is_crit else ""
    log.add(f"You attack {target.name} for {actual} damage!{crit_msg}", ANSI_CYAN)

    # Check for on-hit status effects from equipment
    if is_crit and percentage_chance(25):
        effect = StatusEffect("bleed", duration=3, intensity=2)
        target.add_status(effect)
        log.add(f"{target.name} starts bleeding!", ANSI_RED)

    return "continue"


def _player_magic(player, alive_monsters, log):
    if not player.known_spells:
        log.add("You don't know any spells!", ANSI_RED)
        return "continue"

    print(colored("\n  KNOWN SPELLS:", ANSI_CYAN))
    usable = [(name, SPELL_BOOK[name]) for name in player.known_spells if name in SPELL_BOOK]
    for i, (name, sp) in enumerate(usable):
        affordable = colored("✓", ANSI_GREEN) if player.mp >= sp["cost"] else colored("✗", ANSI_RED)
        print(f"  [{i+1}] {affordable} {name:<22} MP:{sp['cost']:<4} [{sp['element']}]")
    print(f"  [0] Cancel")

    choices = ["0"] + [str(i+1) for i in range(len(usable))]
    idx_str = ask("Cast spell", choices)
    if idx_str == "0":
        return "continue"

    idx = int(idx_str) - 1
    sp_name, sp = usable[idx]

    if player.mp < sp["cost"]:
        log.add("Not enough MP!", ANSI_RED)
        return "continue"

    player.mp -= sp["cost"]
    player.spells_cast += 1

    if sp["target"] == "self":
        if sp_name == "Heal":
            heal = roll_dice(sp["dmg_dice"], sp["dmg_count"], sp["bonus"]) + player.stats.modifier("wis")
            actual = player.heal(heal)
            log.add(f"You cast Heal and recover {actual} HP!", ANSI_GREEN)
        elif sp_name == "Barrier":
            effect = StatusEffect("shield", duration=3, intensity=20)
            player.add_status(effect)
            log.add("A magical barrier surrounds you!", ANSI_CYAN)
        elif sp_name == "Time Warp":
            log.add("Time warps — you gain a bonus action!", ANSI_MAGENTA)
            return _player_attack(player, alive_monsters, log)
        elif sp_name == "Reanimate":
            log.add("Necrotic energy rises... (no fallen allies to reanimate)", ANSI_GRAY)
        else:
            log.add(f"You cast {sp_name}.", ANSI_CYAN)
        return "continue"

    if sp["target"] == "single":
        if len(alive_monsters) == 1:
            targets = [alive_monsters[0]]
        else:
            print("  Target: " + "  ".join(f"[{i+1}] {m.name}" for i, m in enumerate(alive_monsters)))
            idx2 = int(ask("Target", [str(i+1) for i in range(len(alive_monsters))])) - 1
            targets = [alive_monsters[idx2]]
    else:
        targets = alive_monsters

    for t in targets:
        if sp["dmg_dice"] > 0:
            raw = roll_dice(sp["dmg_dice"], sp["dmg_count"], sp["bonus"]) + player.stats.modifier("int")
            is_crit = random.randint(1, 20) == 20
            if is_crit:
                raw = int(raw * CRITICAL_HIT_MULTIPLIER)
            actual = t.take_damage(raw, "magical")
            player.damage_dealt += actual
            crit_txt = " CRITICAL!" if is_crit else ""
            log.add(f"{sp_name} hits {t.name} for {actual} {sp['element']} damage!{crit_txt}", ANSI_MAGENTA)

        # Status effects from spells
        if sp["element"] == "fire" and percentage_chance(30):
            t.add_status(StatusEffect("burn", 3, 2))
            log.add(f"{t.name} is set on fire!", ANSI_RED)
        elif sp["element"] == "ice" and percentage_chance(25):
            t.add_status(StatusEffect("slow", 2))
            log.add(f"{t.name} is slowed by ice!", ANSI_BLUE)
        elif sp["element"] == "lightning" and percentage_chance(20):
            t.add_status(StatusEffect("paralyze", 1))
            log.add(f"{t.name} is paralyzed!", ANSI_YELLOW)
        elif sp["element"] == "poison":
            t.add_status(StatusEffect("poison", 4, 3))
            log.add(f"{t.name} is poisoned!", ANSI_GREEN)

    return "continue"


def _player_use_item(player, log):
    consumables = [(n, c) for n, c in player.inventory.items.items()
                   if ITEM_DEFINITIONS.get(n, {}).get("type") == "consumable"]
    if not consumables:
        log.add("No usable items!", ANSI_RED)
        return "continue"

    print(colored("\n  USABLE ITEMS:", ANSI_CYAN))
    for i, (name, count) in enumerate(consumables):
        print(f"  [{i+1}] {name} x{count}")
    print("  [0] Cancel")

    idx_str = ask("Use item", ["0"] + [str(i+1) for i in range(len(consumables))])
    if idx_str == "0":
        return "continue"

    name, _ = consumables[int(idx_str) - 1]
    defn = ITEM_DEFINITIONS[name]
    effect = defn.get("effect")

    player.inventory.remove_item(name)

    if effect == "heal":
        actual = player.heal(defn["value"])
        log.add(f"You use {name} and recover {actual} HP!", ANSI_GREEN)
    elif effect == "mana":
        actual = player.restore_mp(defn["value"])
        log.add(f"You use {name} and restore {actual} MP!", ANSI_BLUE)
    elif effect == "cure":
        player.status_effects = [e for e in player.status_effects
                                  if e.name not in ["poison", "burn", "bleed"]]
        log.add(f"{name} clears harmful status effects!", ANSI_GREEN)
    elif effect == "buff":
        player.add_status(StatusEffect("haste", 5))
        player.add_status(StatusEffect("berserk", 3))
        log.add(f"{name} surges through you! Speed and power increased!", ANSI_YELLOW)
    elif effect == "bomb":
        log.add(f"You hurl the {name}! (Explosive — hits all enemies!)", ANSI_RED)
        return "explosive", defn["value"]
    return "continue"


def _player_flee(player, log):
    chance = FLEE_BASE_CHANCE + player.stats.modifier("dex") * 3
    if percentage_chance(chance):
        log.add("You successfully flee from combat!", ANSI_YELLOW)
        return "flee"
    else:
        log.add("You couldn't escape!", ANSI_RED)
        return "continue"


def _player_defend(player, log):
    player.add_status(StatusEffect("shield", 1, 5))
    log.add(f"{player.name} takes a defensive stance!", ANSI_CYAN)
    return "continue"


def _player_inspect(alive_monsters, log):
    print(colored("\n  INSPECT TARGET:", ANSI_CYAN))
    for i, m in enumerate(alive_monsters):
        print(f"  [{i+1}] {m.name}")
    idx = int(ask("Inspect", [str(i+1) for i in range(len(alive_monsters))])) - 1
    m = alive_monsters[idx]
    hp_pct = m.hp / m.max_hp_val
    print_box([
        f"Name:   {m.name}  Lv.{m.level}",
        f"HP:     {m.hp}/{m.max_hp_val}  ({hp_pct*100:.0f}%)",
        f"STR:    {m.stats.str}  DEX: {m.stats.dex}  INT: {m.stats.int}",
        f"Style:  {m.ai_style.capitalize()}",
        f"Loot:   {m.loot_tier.capitalize()} tier",
        f"XP:     {m.base_xp}",
    ], ANSI_CYAN)
    pause()
    return "continue"


def monster_combat_turn(monster, player, log):
    """Handle a monster's turn in combat."""
    if not monster.is_alive or monster.is_incapacitated():
        if monster.is_incapacitated():
            log.add(f"{monster.name} is incapacitated!", ANSI_GRAY)
        return

    action = monster.choose_action(player)

    if action == "skip" or action == "dead":
        return

    if action == "flee":
        log.add(f"{monster.name} attempts to flee!", ANSI_YELLOW)
        if percentage_chance(40):
            monster.is_alive = False
            log.add(f"{monster.name} escaped!", ANSI_YELLOW)
        return

    if action == "defend":
        monster.defending = True
        log.add(f"{monster.name} takes a defensive stance!", ANSI_CYAN)
        return

    if action == "double_attack":
        for _ in range(2):
            _monster_basic_attack(monster, player, log)
        return

    if isinstance(action, tuple) and action[0] == "ability":
        ability_name = action[1]
        _monster_use_ability(monster, player, ability_name, log)
        return

    _monster_basic_attack(monster, player, log)


def _monster_basic_attack(monster, player, log):
    """Monster performs a basic attack."""
    if player.attempt_dodge():
        log.add(f"You dodge {monster.name}'s attack!", ANSI_CYAN)
        return

    # Check player shield
    shield_active = player.has_status("shield")

    base_dmg = roll_dice(6, 1, monster.stats.modifier("str"))
    base_dmg = max(1, base_dmg)
    is_crit = random.randint(1, 20) >= 19
    if is_crit:
        base_dmg = int(base_dmg * CRITICAL_HIT_MULTIPLIER)

    defense = player.equipment.defense_total()
    reduced = max(1, base_dmg - defense // 3)

    if shield_active:
        absorbed = min(reduced, 15)
        reduced = max(0, reduced - absorbed)
        log.add(f"Your barrier absorbs {absorbed} damage!", ANSI_BLUE)

    actual = player.take_damage(reduced, "physical")
    player.damage_taken += actual
    crit_str = colored(" CRIT!", ANSI_RED) if is_crit else ""
    log.add(f"{monster.name} attacks you for {actual} damage!{crit_str}", ANSI_RED)


def _monster_use_ability(monster, player, ability, log):
    """Monster uses a special ability."""
    if ability == "Breathe Fire":
        dmg = roll_dice(8, 2, 5)
        actual = player.take_damage(dmg, "fire")
        player.damage_taken += actual
        player.add_status(StatusEffect("burn", 2, 3))
        log.add(f"{monster.name} breathes fire! {actual} damage + burn!", ANSI_RED)
    elif ability == "Tail Swipe":
        dmg = roll_dice(10, 1, 8)
        actual = player.take_damage(dmg, "physical")
        player.damage_taken += actual
        player.add_status(StatusEffect("stun", 1))
        log.add(f"{monster.name} tail-swipes you! {actual} damage + stun!", ANSI_RED)
    elif ability == "Wing Gust":
        dmg = roll_dice(4, 1, 3)
        actual = player.take_damage(dmg, "wind")
        player.damage_taken += actual
        player.add_status(StatusEffect("blind", 2))
        log.add(f"{monster.name}'s wings blast you! {actual} damage + blind!", ANSI_YELLOW)
    elif ability == "Death Bolt":
        dmg = roll_dice(12, 1, 10)
        actual = player.take_damage(dmg, "dark")
        player.damage_taken += actual
        log.add(f"{monster.name} fires a Death Bolt! {actual} dark damage!", ANSI_MAGENTA)
    elif ability == "Summon Undead":
        log.add(f"{monster.name} summons skeletal minions! (minions emerge)", ANSI_GRAY)
    elif ability == "Soul Drain":
        dmg = roll_dice(8, 1, 5)
        actual = player.take_damage(dmg, "dark")
        monster.hp = min(monster.max_hp_val, monster.hp + dmg // 2)
        player.damage_taken += actual
        log.add(f"{monster.name} drains your soul! {actual} dmg, heals self.", ANSI_MAGENTA)
    elif ability == "Life Drain":
        dmg = roll_dice(6, 1, 4)
        actual = player.take_damage(dmg, "dark")
        monster.hp = min(monster.max_hp_val, monster.hp + dmg)
        player.damage_taken += actual
        log.add(f"{monster.name} drains your life! {actual} dmg.", ANSI_RED)
    elif ability == "Mesmerize":
        player.add_status(StatusEffect("stun", 2))
        log.add(f"{monster.name}'s gaze mesmerizes you! Stunned 2 turns.", ANSI_MAGENTA)
    elif ability == "Hex":
        player.add_status(StatusEffect("slow", 3))
        player.add_status(StatusEffect("blind", 2))
        log.add(f"{monster.name} hexes you! Slow + Blind.", ANSI_MAGENTA)
    elif ability == "Poison Cloud":
        player.add_status(StatusEffect("poison", 5, 3))
        log.add(f"{monster.name} releases poison cloud! Poisoned 5 turns.", ANSI_GREEN)
    elif ability == "Tidal Wave":
        dmg = roll_dice(8, 2, 3)
        actual = player.take_damage(dmg, "water")
        player.damage_taken += actual
        log.add(f"{monster.name} unleashes a tidal wave! {actual} damage!", ANSI_BLUE)
    elif ability == "Power Strike":
        dmg = roll_dice(8, 2, monster.stats.modifier("str"))
        actual = player.take_damage(dmg, "physical")
        player.damage_taken += actual
        log.add(f"{monster.name} power strikes for {actual} damage!", ANSI_RED)
    elif ability == "Enrage":
        monster.stats.str += 3
        log.add(f"{monster.name} enrages! STR increased.", ANSI_RED)
    else:
        _monster_basic_attack(monster, player, log)


def run_combat(player, monsters):
    """Run a full combat encounter."""
    log = CombatLog()
    turn = 1
    encounter_msg = random.choice(RANDOM_ENCOUNTER_MESSAGES)
    log.add(encounter_msg, ANSI_YELLOW)
    log.add(f"A battle begins against {', '.join(m.name for m in monsters)}!", ANSI_RED)

    for m in monsters:
        m.defending = False

    while True:
        BattleRenderer.render(player, monsters, turn, log)

        # Tick status effects
        for msg in player.tick_status_effects():
            log.add(msg)
        for m in monsters:
            if m.is_alive:
                for msg in m.tick_status_effects():
                    log.add(msg)

        if not player.is_alive:
            print(colored(f"\n  {random.choice(DEATH_QUOTES)}", ANSI_RED))
            player.deaths += 1
            pause("You have fallen... Press ENTER")
            return "defeat"

        if all(not m.is_alive for m in monsters):
            break

        result = player_combat_turn(player, monsters, log)

        if isinstance(result, tuple) and result[0] == "explosive":
            bomb_dmg = result[1]
            for m in monsters:
                if m.is_alive:
                    actual = m.take_damage(bomb_dmg, "fire")
                    log.add(f"Explosion hits {m.name} for {actual} damage!", ANSI_RED)
            result = "continue"

        if result == "flee":
            return "flee"
        if result == "win":
            break

        # Monsters' turns
        for m in monsters:
            if m.is_alive:
                monster_combat_turn(m, player, log)
                m.defending = False

        if not player.is_alive:
            BattleRenderer.render(player, monsters, turn, log)
            print(colored(f"\n  {random.choice(DEATH_QUOTES)}", ANSI_RED))
            player.deaths += 1
            pause("You have fallen... Press ENTER")
            return "defeat"

        turn += 1

    # Victory
    BattleRenderer.render(player, monsters, turn, log)
    print(colored(f"\n  {random.choice(VICTORY_QUOTES)}", ANSI_GREEN))

    total_xp   = 0
    total_gold = 0
    total_loot = {}

    for m in monsters:
        player.kills[m.family] = player.kills.get(m.family, 0) + 1
        player.update_kill_quest(m.family)
        total_xp += m.base_xp
        drops, gold = m.drop_loot()
        total_gold += gold
        for item, count in drops.items():
            total_loot[item] = total_loot.get(item, 0) + count

    print(colored(f"\n  Gained {total_xp} XP and {total_gold} Gold!", ANSI_YELLOW))
    leveled = player.gain_xp(total_xp)
    player.inventory.gold += total_gold
    player.gold_earned += total_gold

    if total_loot:
        print(colored("  Loot:", ANSI_GREEN))
        for item, count in total_loot.items():
            player.inventory.add_item(item, count)
            print(f"    + {item} x{count}")

    completed = player.check_quest_completion()
    for qname in completed:
        player.complete_quest(qname)

    if leveled:
        player.level_up_menu()

    _check_achievements(player)
    pause()
    return "win"


def _check_achievements(player):
    """Check and award achievements."""
    achievements_defs = [
        ("First Blood",   lambda p: sum(p.kills.values()) >= 1),
        ("Goblin Slayer", lambda p: p.kills.get("Goblin", 0) >= 10),
        ("Dragon Slayer", lambda p: p.kills.get("Dragon", 0) >= 1),
        ("Lich Bane",     lambda p: p.kills.get("Lich", 0) >= 1),
        ("Century Kill",  lambda p: sum(p.kills.values()) >= 100),
        ("Spellslinger",  lambda p: p.spells_cast >= 50),
        ("Rich Adventurer",lambda p: p.inventory.gold >= 1000),
        ("Level 10",      lambda p: p.level >= 10),
        ("Level 25",      lambda p: p.level >= 25),
        ("Level 50",      lambda p: p.level >= MAX_LEVEL),
        ("Quest Master",  lambda p: len(p.completed_quests) >= 5),
        ("Crafter",       lambda p: p.crafted_items >= 10),
        ("Survivor",      lambda p: p.deaths == 0 and sum(p.kills.values()) >= 20),
    ]
    for name, condition in achievements_defs:
        if name not in player.achievements and condition(player):
            player.achievements.append(name)
            print(colored(f"\n  🏆 Achievement Unlocked: {name}!", ANSI_YELLOW))


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5: WORLD & EXPLORATION
# ─────────────────────────────────────────────────────────────────────────────

class WorldMap:
    """Handles the world map display and navigation."""
    def __init__(self):
        self.grid = [list(row) for row in WORLD_MAP_TEMPLATE]
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT

    def tile_at(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.grid[y][x]
        return "~"

    def is_passable(self, x, y):
        tile = self.tile_at(x, y)
        return MAP_LEGEND.get(tile, (None, None, False))[2]

    def render(self, player_x, player_y):
        clear_screen()
        print_header("WORLD MAP")
        for y, row in enumerate(self.grid):
            line = ""
            for x, tile in enumerate(row):
                legend = MAP_LEGEND.get(tile, ("Unknown", ANSI_WHITE, False))
                color = legend[1]
                if x == player_x and y == player_y:
                    line += colored("@", ANSI_CYAN + ANSI_BOLD)
                else:
                    line += colored(tile, color)
            print(f"  {line}")

        tile = self.tile_at(player_x, player_y)
        loc_name = MAP_LEGEND.get(tile, ("Unknown",))[0]
        print(f"\n  Position: ({player_x}, {player_y})  |  Location: {loc_name}")
        print(colored("  Move: W/A/S/D  |  Enter location: E  |  Back: B", ANSI_GRAY))

    def get_encounter_chance(self, x, y):
        tile = self.tile_at(x, y)
        chances = {
            "T": 35, "M": 30, "B": 50, ".": 20, "V": 5, "D": 60,
            "F": 40, "C": 10, "~": 0, "S": 0,
        }
        return chances.get(tile, 20)

    def get_encounter_monsters(self, x, y, player_level):
        tile = self.tile_at(x, y)
        groups = {
            "T": ["Goblin", "Wolf", "Harpy"],
            "M": ["Golem", "Troll", "Harpy"],
            "B": ["Bandit", "Orc", "Troll"],
            ".": ["Goblin", "Bandit", "Slime"],
            "D": ["Skeleton", "Lich", "Vampire"],
            "F": ["Wolf", "Harpy", "Witch"],
            "C": ["Skeleton", "Bandit", "Orc"],
            "V": ["Goblin"],
        }
        pool = groups.get(tile, ["Goblin", "Slime"])
        count = random.randint(1, 3)
        monsters = []
        for _ in range(count):
            family = random.choice(pool)
            level = max(1, player_level + random.randint(-2, 3))
            monsters.append(Monster(family, level))
        return monsters


def explore_location(player, world_map, game_clock):
    """Handle events at the current map location."""
    x, y = player.world_x, player.world_y
    tile = world_map.tile_at(x, y)
    loc_name = MAP_LEGEND.get(tile, ("Unknown",))[0]

    clear_screen()
    print_header(f"📍 {loc_name}")
    tod = time_of_day_label(game_clock.hour)
    print(colored(f"  {tod} — ({x}, {y})", ANSI_GRAY))

    if tile == "S":
        _explore_starting_town(player, game_clock)
    elif tile == "V":
        _explore_village(player, game_clock)
    elif tile == "C":
        _explore_castle(player, game_clock)
    elif tile == "D":
        _explore_dungeon(player, world_map, game_clock)
    elif tile == "F":
        _explore_forest_temple(player, world_map, game_clock)
    elif tile in ["T", "M", ".", "B"]:
        _explore_wilderness(player, world_map, game_clock)
    elif tile == "~":
        print(colored("  The ocean blocks your path.", ANSI_BLUE))
        pause()


def _explore_starting_town(player, clock):
    """Explore the starting town with NPCs and services."""
    print(colored("  Welcome to Ashenvale, the starting town.\n", ANSI_YELLOW))
    options = ["1. Talk to NPCs", "2. Visit Blacksmith", "3. Visit Inn",
               "4. Visit Market", "5. Leave"]
    for opt in options:
        print(f"  {opt}")
    choice = ask("What do you do?", ["1", "2", "3", "4", "5"])
    if choice == "1":
        _npc_hub(player, ["Elder Aldric", "Healer Mira", "Merchant Pol"])
    elif choice == "2":
        _blacksmith(player)
    elif choice == "3":
        _inn(player, clock)
    elif choice == "4":
        _market(player)


def _explore_village(player, clock):
    """Explore a village."""
    print(colored("  A small village nestled between the trees.\n", ANSI_GREEN))
    choices = ["1. Rest at a farmhouse", "2. Look for rumors", "3. Leave"]
    for c in choices:
        print(f"  {c}")
    choice = ask("Action", ["1", "2", "3"])
    if choice == "1":
        player.rest(4)
        print(colored("  You rest for a few hours.", ANSI_GRAY))
        pause()
    elif choice == "2":
        rumor = random.choice(TAVERN_RUMORS)
        print(colored(f"\n  Villager whispers: \"{rumor}\"", ANSI_GRAY))
        pause()


def _explore_castle(player, clock):
    """Explore the castle."""
    print(colored("  The castle of King Doran looms before you.\n", ANSI_WHITE))
    choices = ["1. Audience with the King", "2. Training grounds", "3. Leave"]
    for c in choices:
        print(f"  {c}")
    choice = ask("Action", ["1", "2", "3"])
    if choice == "1":
        _npc_hub(player, ["King Doran", "Captain Vera"])
    elif choice == "2":
        _training_grounds(player)


def _explore_dungeon(player, world_map, clock):
    """Explore the dungeon."""
    print(colored("  Cold air wafts from the dungeon entrance.\n", ANSI_RED))
    choices = ["1. Enter dungeon", "2. Camp outside", "3. Leave"]
    for c in choices:
        print(f"  {c}")
    choice = ask("Action", ["1", "2", "3"])
    if choice == "1":
        floors = 3
        for floor in range(1, floors + 1):
            print(colored(f"\n  Dungeon Floor {floor}...", ANSI_RED))
            time.sleep(0.5)
            monsters = world_map.get_encounter_monsters(
                player.world_x, player.world_y, player.level + floor)
            result = run_combat(player, monsters)
            if result == "defeat":
                player.hp = 1
                print(colored("  You barely escape the dungeon...", ANSI_RED))
                break
            if result == "flee":
                print(colored("  You flee from the dungeon.", ANSI_YELLOW))
                break
            if floor == floors:
                print(colored("  You've cleared the dungeon!", ANSI_GREEN))
                bonus_gold = roll_dice(20, floor, 10)
                player.inventory.gold += bonus_gold
                print(colored(f"  Bonus treasure: {bonus_gold} gold!", ANSI_YELLOW))
    elif choice == "2":
        player.rest(6)
        pause()


def _explore_forest_temple(player, world_map, clock):
    """Explore the forest temple."""
    print(colored("  Ancient stones covered in moss form the Forest Temple.\n", ANSI_GREEN))
    choices = ["1. Pray at the altar", "2. Explore inner chambers", "3. Leave"]
    for c in choices:
        print(f"  {c}")
    choice = ask("Action", ["1", "2", "3"])
    if choice == "1":
        if percentage_chance(40):
            spell = random.choice(list(SPELL_BOOK.keys()))
            if spell not in player.known_spells:
                player.known_spells.append(spell)
                print(colored(f"\n  The altar's magic flows into you — learned: {spell}!", ANSI_CYAN))
            else:
                hp_gain = roll_dice(10, 2)
                player.heal(hp_gain)
                print(colored(f"\n  Divine energy heals you for {hp_gain} HP.", ANSI_GREEN))
        else:
            print(colored("  The altar is silent.", ANSI_GRAY))
        pause()
    elif choice == "2":
        monsters = world_map.get_encounter_monsters(
            player.world_x, player.world_y, player.level + 2)
        result = run_combat(player, monsters)
        if result == "win":
            if percentage_chance(50):
                item = random.choice(LOOT_TABLES["rare"])
                player.inventory.add_item(item)
                print(colored(f"\n  Found in the chambers: {item}!", ANSI_GREEN))
                pause()


def _explore_wilderness(player, world_map, clock):
    """Handle wilderness exploration with possible encounters."""
    enc_chance = world_map.get_encounter_chance(player.world_x, player.world_y)
    if percentage_chance(enc_chance):
        monsters = world_map.get_encounter_monsters(
            player.world_x, player.world_y, player.level)
        run_combat(player, monsters)
    else:
        msgs = [
            "You find a few wild herbs.",
            "Nothing happens. The wind rustles through the trees.",
            "You spot animal tracks but find nothing.",
            "A distant howl echoes... but nothing approaches.",
            "You find a forgotten campfire — still warm.",
        ]
        print(colored(f"\n  {random.choice(msgs)}", ANSI_GRAY))
        if percentage_chance(20):
            herb = random.choice(["Red Herb", "Blue Herb", "Green Herb"])
            count = random.randint(1, 3)
            player.inventory.add_item(herb, count)
            print(colored(f"  Gathered {count}x {herb}.", ANSI_GREEN))
        pause()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6: TOWN SYSTEMS (INN, MARKET, BLACKSMITH, ETC.)
# ─────────────────────────────────────────────────────────────────────────────

class GameClock:
    """Tracks in-game time."""
    def __init__(self):
        self.day = 1
        self.hour = 8
        self.minute = 0

    def advance(self, minutes):
        self.minute += minutes
        while self.minute >= 60:
            self.minute -= 60
            self.hour += 1
        while self.hour >= 24:
            self.hour -= 24
            self.day += 1

    def display(self):
        tod = time_of_day_label(self.hour)
        return f"Day {self.day}, {self.hour:02d}:{self.minute:02d} ({tod})"

    def to_dict(self):
        return {"day": self.day, "hour": self.hour, "minute": self.minute}

    @classmethod
    def from_dict(cls, d):
        c = cls()
        c.day = d.get("day", 1)
        c.hour = d.get("hour", 8)
        c.minute = d.get("minute", 0)
        return c


def _npc_hub(player, npc_names):
    """Talk to NPCs in a location."""
    while True:
        print(colored("\n  Who do you speak with?", ANSI_CYAN))
        for i, name in enumerate(npc_names):
            print(f"  [{i+1}] {name}")
        print("  [0] Leave")
        choice = ask("Speak with", ["0"] + [str(i+1) for i in range(len(npc_names))])
        if choice == "0":
            break
        npc_name = npc_names[int(choice) - 1]
        _npc_dialogue(player, npc_name)


def _npc_dialogue(player, npc_name):
    """Handle NPC dialogue."""
    npc = NPC_DIALOGUE.get(npc_name, {})
    clear_screen()
    print_header(f"Talking to {npc_name}")

    greeting = npc.get("greeting", "Hello, traveller.")
    slow_print(colored(f'  {npc_name}: "{greeting}"', ANSI_YELLOW), 0.02)

    options = ["1. Ask for a quest", "2. Ask about the world", "3. Goodbye"]
    for opt in options:
        print(f"\n  {opt}")
    choice = ask("Response", ["1", "2", "3"])

    if choice == "1":
        quest_prompt = npc.get("quest_prompt", "I have nothing for you now.")
        slow_print(colored(f'\n  {npc_name}: "{quest_prompt}"', ANSI_YELLOW), 0.02)
        avail_quests = [qn for qn, qd in QUEST_DATABASE.items()
                        if qd.get("giver") == npc_name
                        and qn not in player.active_quests
                        and qn not in player.completed_quests
                        and player.level >= qd.get("level_req", 1)]
        if avail_quests:
            print(colored(f"\n  Available quests from {npc_name}:", ANSI_GREEN))
            for i, qn in enumerate(avail_quests):
                qd = QUEST_DATABASE[qn]
                print(f"  [{i+1}] {qn}  (Lv.{qd['level_req']}+)  — {qd['desc']}")
            print("  [0] Decline")
            choice2 = ask("Accept quest", ["0"] + [str(i+1) for i in range(len(avail_quests))])
            if choice2 != "0":
                qname = avail_quests[int(choice2) - 1]
                player.add_quest(qname)
        else:
            print(colored("  (No quests available right now.)", ANSI_GRAY))

    elif choice == "2":
        lore = npc.get("lore", "I don't know much beyond these walls.")
        slow_print(colored(f'\n  {npc_name}: "{lore}"', ANSI_YELLOW), 0.02)

    pause()


def _inn(player, clock):
    """Visit the inn to rest."""
    print_header("THE TATTERED FLAGON INN")
    innkeeper = NPC_DIALOGUE.get("Innkeeper Bessa", {})
    slow_print(colored(f'  Bessa: "{innkeeper.get("greeting", "Welcome!")}"', ANSI_YELLOW), 0.02)

    print("\n  Services:")
    print("  [1] Rest 4 hours (5 gold)  — Recover 30% HP/MP")
    print("  [2] Rest 8 hours (10 gold) — Recover 60% HP/MP")
    print("  [3] Full night (20 gold)   — Full HP/MP restore")
    print("  [4] Hear a rumor (3 gold)")
    print("  [5] Leave")
    choice = ask("Choice", ["1", "2", "3", "4", "5"])

    if choice == "1":
        if player.inventory.gold >= 5:
            player.inventory.gold -= 5
            player.rest(4)
            clock.advance(240)
        else:
            print(colored("  Not enough gold.", ANSI_RED))
    elif choice == "2":
        if player.inventory.gold >= 10:
            player.inventory.gold -= 10
            player.rest(8)
            clock.advance(480)
        else:
            print(colored("  Not enough gold.", ANSI_RED))
    elif choice == "3":
        if player.inventory.gold >= 20:
            player.inventory.gold -= 20
            player.hp = player.max_hp()
            player.mp = player.max_mp()
            player.status_effects.clear()
            clock.advance(720)
            print(colored("  You sleep soundly. Fully restored.", ANSI_GREEN))
        else:
            print(colored("  Not enough gold.", ANSI_RED))
    elif choice == "4":
        if player.inventory.gold >= 3:
            player.inventory.gold -= 3
            rumor = random.choice(TAVERN_RUMORS)
            print(colored(f'\n  A patron leans over: "{rumor}"', ANSI_GRAY))
        else:
            print(colored("  Not enough gold.", ANSI_RED))
    pause()


def _market(player):
    """Visit the market to buy/sell items."""
    print_header("THE MARKET")
    shop_stock = {
        "Health Potion":  ITEM_DEFINITIONS["Health Potion"]["gold"],
        "Mana Potion":    ITEM_DEFINITIONS["Mana Potion"]["gold"],
        "Antidote":       ITEM_DEFINITIONS["Antidote"]["gold"],
        "Red Herb":       ITEM_DEFINITIONS["Red Herb"]["gold"],
        "Blue Herb":      ITEM_DEFINITIONS["Blue Herb"]["gold"],
        "Green Herb":     ITEM_DEFINITIONS["Green Herb"]["gold"],
        "Empty Vial":     ITEM_DEFINITIONS["Empty Vial"]["gold"],
        "Iron Ingot":     ITEM_DEFINITIONS["Iron Ingot"]["gold"],
        "Leather":        ITEM_DEFINITIONS["Leather"]["gold"],
        "Thread":         ITEM_DEFINITIONS["Thread"]["gold"],
    }

    while True:
        print(f"\n  Your gold: {colored(str(player.inventory.gold), ANSI_YELLOW)}")
        print("\n  [1] Buy   [2] Sell   [3] Leave")
        choice = ask("Action", ["1", "2", "3"])

        if choice == "3":
            break

        if choice == "1":
            print(colored("\n  STOCK:", ANSI_CYAN))
            items = list(shop_stock.items())
            for i, (name, price) in enumerate(items):
                afford = colored("✓", ANSI_GREEN) if player.inventory.gold >= price else colored("✗", ANSI_RED)
                print(f"  [{i+1}] {afford} {name:<28} {price} gold")
            print("  [0] Back")
            idx_str = ask("Buy", ["0"] + [str(i+1) for i in range(len(items))])
            if idx_str != "0":
                name, price = items[int(idx_str) - 1]
                qty_str = ask("Quantity", None)
                try:
                    qty = int(qty_str)
                except ValueError:
                    qty = 1
                qty = max(1, qty)
                total = price * qty
                if player.inventory.gold >= total:
                    player.inventory.gold -= total
                    player.inventory.add_item(name, qty)
                    print(colored(f"  Bought {qty}x {name} for {total} gold.", ANSI_GREEN))
                else:
                    print(colored("  Not enough gold.", ANSI_RED))

        elif choice == "2":
            if not player.inventory.items:
                print(colored("  Nothing to sell.", ANSI_RED))
                continue
            item_list = list(player.inventory.items.items())
            print(colored("\n  YOUR ITEMS:", ANSI_CYAN))
            for i, (name, count) in enumerate(item_list):
                sell_price = int(ITEM_DEFINITIONS.get(name, {}).get("gold", 1) * 0.6)
                print(f"  [{i+1}] {name:<28} x{count}  sells for {sell_price}g each")
            print("  [0] Back")
            idx_str = ask("Sell", ["0"] + [str(i+1) for i in range(len(item_list))])
            if idx_str != "0":
                name, count = item_list[int(idx_str) - 1]
                qty_str = ask(f"How many? (max {count})", None)
                try:
                    qty = clamp(int(qty_str), 1, count)
                except ValueError:
                    qty = 1
                sell_price = int(ITEM_DEFINITIONS.get(name, {}).get("gold", 1) * 0.6)
                total = sell_price * qty
                player.inventory.remove_item(name, qty)
                player.inventory.gold += total
                player.gold_earned += total
                print(colored(f"  Sold {qty}x {name} for {total} gold.", ANSI_GREEN))


def _blacksmith(player):
    """Visit the blacksmith."""
    print_header("TORVA'S FORGE")
    slow_print(colored('  Torva: "Need something forged? You\'ve come to the right place."', ANSI_YELLOW), 0.02)
    print("\n  [1] Buy weapon   [2] Buy armor   [3] Upgrade equipment   [4] Leave")
    choice = ask("Action", ["1", "2", "3", "4"])

    weapons_for_sale = {
        "Iron Sword":    80,
        "Steel Dagger":  60,
        "Oak Staff":     55,
        "Hunting Bow":   70,
        "Battle Axe":    90,
    }
    armors_for_sale = {
        "Leather Armor": 70,
        "Chainmail":     120,
        "Iron Shield":   90,
        "Steel Helm":    85,
        "Studded Boots": 60,
    }

    if choice == "1":
        print(colored("\n  WEAPONS:", ANSI_CYAN))
        items = list(weapons_for_sale.items())
        for i, (name, price) in enumerate(items):
            print(f"  [{i+1}] {name:<25} {price} gold")
        print("  [0] Back")
        idx_str = ask("Buy", ["0"] + [str(i+1) for i in range(len(items))])
        if idx_str != "0":
            name, price = items[int(idx_str) - 1]
            if player.inventory.gold >= price:
                player.inventory.gold -= price
                player.inventory.add_item(name)
                print(colored(f"  Purchased {name}!", ANSI_GREEN))
            else:
                print(colored("  Not enough gold.", ANSI_RED))
    elif choice == "2":
        print(colored("\n  ARMORS:", ANSI_CYAN))
        items = list(armors_for_sale.items())
        for i, (name, price) in enumerate(items):
            print(f"  [{i+1}] {name:<25} {price} gold")
        print("  [0] Back")
        idx_str = ask("Buy", ["0"] + [str(i+1) for i in range(len(items))])
        if idx_str != "0":
            name, price = items[int(idx_str) - 1]
            if player.inventory.gold >= price:
                player.inventory.gold -= price
                player.inventory.add_item(name)
                print(colored(f"  Purchased {name}!", ANSI_GREEN))
            else:
                print(colored("  Not enough gold.", ANSI_RED))
    elif choice == "3":
        print(colored("\n  Upgrade costs 50 gold per slot and improves the item's tier.", ANSI_GRAY))
        player.equipment.display()
        slot = ask("Upgrade slot (weapon/armor/etc)", Equipment.SLOTS)
        item = player.equipment.slots.get(slot)
        if not item:
            print(colored("  Nothing equipped in that slot.", ANSI_RED))
        elif player.inventory.gold >= 50:
            player.inventory.gold -= 50
            print(colored(f"  {item} has been improved!", ANSI_GREEN))
        else:
            print(colored("  Not enough gold.", ANSI_RED))
    pause()


def _training_grounds(player):
    """Train at the castle training grounds."""
    print_header("TRAINING GROUNDS")
    print("  Spar with the castle guards to improve your skills.\n")
    print("  [1] Spar (practice combat, no death risk)")
    print("  [2] Study spellbooks (costs 50 gold)")
    print("  [3] Leave")
    choice = ask("Action", ["1", "2", "3"])

    if choice == "1":
        dummy = Monster("Goblin", max(1, player.level - 1))
        dummy.name = "Training Dummy"
        dummy.hp = dummy.max_hp_val // 2
        result = run_combat(player, [dummy])
        if result == "win":
            xp = 20 + player.level * 5
            player.gain_xp(xp)
            print(colored(f"  Practice complete. Gained {xp} XP.", ANSI_GREEN))
    elif choice == "2":
        if player.inventory.gold >= 50:
            player.inventory.gold -= 50
            candidates = [s for s in SPELL_BOOK if s not in player.known_spells
                          and SPELL_BOOK[s]["level_req"] <= player.level + 2]
            if candidates:
                learned = random.choice(candidates)
                player.known_spells.append(learned)
                print(colored(f"  You study and learn: {learned}!", ANSI_CYAN))
            else:
                print(colored("  No new spells available at your level.", ANSI_GRAY))
                player.inventory.gold += 50
        else:
            print(colored("  Not enough gold.", ANSI_RED))
    pause()


def _crafting_menu(player):
    """The crafting system."""
    print_header("CRAFTING BENCH")
    print(f"  Crafting Level: {player.crafting_level}\n")

    available_recipes = []
    for recipe_name, recipe in CRAFTING_RECIPES.items():
        if recipe["skill_req"] <= player.crafting_level:
            available_recipes.append((recipe_name, recipe))

    if not available_recipes:
        print(colored("  No recipes available yet.", ANSI_GRAY))
        pause()
        return

    print(colored("  AVAILABLE RECIPES:", ANSI_CYAN))
    for i, (rname, recipe) in enumerate(available_recipes):
        ingredients_str = ", ".join(f"{c}x {m}" for m, c in recipe["ingredients"].items())
        can_craft = all(player.inventory.has_item(m, c) for m, c in recipe["ingredients"].items())
        status = colored("✓", ANSI_GREEN) if can_craft else colored("✗", ANSI_RED)
        print(f"  [{i+1}] {status} {rname:<25}  Needs: {ingredients_str}")
    print("  [0] Back")

    idx_str = ask("Craft", ["0"] + [str(i+1) for i in range(len(available_recipes))])
    if idx_str == "0":
        return

    rname, recipe = available_recipes[int(idx_str) - 1]
    can_craft = all(player.inventory.has_item(m, c) for m, c in recipe["ingredients"].items())

    if not can_craft:
        print(colored("  Missing ingredients!", ANSI_RED))
        pause()
        return

    for mat, count in recipe["ingredients"].items():
        player.inventory.remove_item(mat, count)

    result_item = recipe["result"]
    player.inventory.add_item(result_item)
    player.crafted_items += 1

    xp_gained = (recipe["skill_req"] + 1) * 10
    player.crafting_level = min(10, player.crafting_level + 1) if percentage_chance(30) else player.crafting_level

    print(colored(f"\n  ✓ Crafted: {result_item}!", ANSI_GREEN))
    print(colored(f"  Crafting XP: +{xp_gained}", ANSI_YELLOW))
    pause()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7: SAVE / LOAD SYSTEM
# ─────────────────────────────────────────────────────────────────────────────

def save_game(player, world_map, clock):
    """Save the current game state to a JSON file."""
    data = {
        "version": VERSION,
        "timestamp": datetime.datetime.now().isoformat(),
        "player": player.to_dict(),
        "clock": clock.to_dict(),
        "checksum": "",
    }
    raw = json.dumps(data, indent=2)
    chk = hashlib.md5(raw.encode()).hexdigest()[:8]
    data["checksum"] = chk
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(colored(f"\n  Game saved to '{SAVE_FILE}'  [{chk}]", ANSI_GREEN))
    pause()


def load_game():
    """Load a saved game state from JSON."""
    if not os.path.exists(SAVE_FILE):
        print(colored(f"  No save file found at '{SAVE_FILE}'.", ANSI_RED))
        return None, None

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    print(colored(f"  Loading save from: {data.get('timestamp', 'unknown')}", ANSI_GREEN))
    player = Player.from_dict(data["player"])
    clock  = GameClock.from_dict(data.get("clock", {}))
    world_map = WorldMap()
    return player, clock, world_map


def delete_save():
    """Delete the save file."""
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
        print(colored("  Save file deleted.", ANSI_YELLOW))
    else:
        print(colored("  No save file to delete.", ANSI_GRAY))
    pause()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8: CHARACTER CREATION
# ─────────────────────────────────────────────────────────────────────────────

ASCII_TITLE = r"""
   _____ _                _   _                    _
  / ____| |              | | | |                  | |
 | |    | |__  _ __ ___  | |_| | ___  ___    ___  | |
 | |    | '_ \| '__/ _ \ |  _  |/ _ \/ __|  / _ \ | |
 | |____| | | | | | (_) || | | | (_) \__ \ | (_) || |
  \_____|_| |_|_|  \___/ |_| |_|\___/|___/  \___/ |_|

   ___  _         _   _                   _   ____            _
  / __|| |_  __ _| |_| |_ ___ _ _ ___ __| | |  _ \ ___  __ _| |_ __ ___
  \__ \| ' \/ _` |  _|  _/ -_) '_/ -_) _` | | |_) / -_)/ _` | | '_ (_-<
  |___/|_||_\__,_|\__|\__\___|_| \___\__,_| |____/\___|\__,_|_| ._/__/
                                                                 |_|
"""


def create_character():
    """Walk through character creation."""
    clear_screen()
    print(colored(ASCII_TITLE, ANSI_CYAN))
    print(colored("  Chronicles of the Shattered Realm  v" + VERSION, ANSI_YELLOW))
    print_divider()

    print(colored("\n  Enter your character's name:", ANSI_CYAN))
    name = input("  ► Name: ").strip() or "Hero"

    print(colored("\n  Choose your RACE:", ANSI_CYAN))
    races = list(RACE_BONUSES.keys())
    for i, r in enumerate(races):
        bonuses = RACE_BONUSES[r]
        b_str = "  ".join(f"{k}+{v}" for k, v in bonuses.items() if v > 0)
        print(f"  [{i+1}] {r:<10} {b_str}")
    race_idx = int(ask("Race", [str(i+1) for i in range(len(races))])) - 1
    race = races[race_idx]

    print(colored("\n  Choose your CLASS:", ANSI_CYAN))
    classes = list(CLASS_BONUSES.keys())
    class_descs = {
        "Warrior":  "Tough melee fighter. High HP and STR.",
        "Rogue":    "Swift and deadly. High DEX and crits.",
        "Mage":     "Powerful spellcaster. High INT and MP.",
        "Paladin":  "Holy knight. Balanced STR/WIS, healing.",
        "Ranger":   "Ranged combatant. DEX-based, nature magic.",
        "Bard":     "Jack-of-all-trades. Good LCK, support.",
    }
    for i, c in enumerate(classes):
        hp_d = CLASS_HP_DICE[c]
        mp_b = CLASS_MP_BASE[c]
        print(f"  [{i+1}] {c:<10} {class_descs[c]}  (HP:d{hp_d}, MP:{mp_b})")
    class_idx = int(ask("Class", [str(i+1) for i in range(len(classes))])) - 1
    char_class = classes[class_idx]

    print(colored(f"\n  Creating {race} {char_class} named '{name}'...", ANSI_GREEN))
    time.sleep(1)

    player = Player(name, race, char_class)

    # Starting equipment based on class
    starting_gear = {
        "Warrior":  [("Iron Sword", "weapon"), ("Leather Armor", "armor")],
        "Rogue":    [("Steel Dagger", "weapon"), ("Leather Boots", "boots")],
        "Mage":     [("Oak Staff", "weapon"), ("Mage Robe", "armor")],
        "Paladin":  [("Iron Sword", "weapon"), ("Chainmail", "armor")],
        "Ranger":   [("Hunting Bow", "weapon"), ("Hide Armor", "armor")],
        "Bard":     [("Lute Blade", "weapon"), ("Silk Coat", "armor")],
    }
    for item_name, slot in starting_gear.get(char_class, []):
        player.inventory.add_item(item_name)
        player.equipment.equip(slot, item_name)

    # Starting consumables
    player.inventory.add_item("Health Potion", 3)
    player.inventory.add_item("Mana Potion", 2)
    player.inventory.gold = 50

    # Starting quest
    player.add_quest("The First Step")
    player.add_quest("Herb Collector")

    print(colored(f"\n  Welcome, {name}! Your adventure in the Shattered Realm begins.", ANSI_YELLOW))
    slow_print(colored("  The realm is fractured, the crown is lost, and darkness stirs...", ANSI_GRAY), 0.03)
    pause("Press ENTER to begin your journey...")
    return player


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9: STATISTICS & ACHIEVEMENTS SCREEN
# ─────────────────────────────────────────────────────────────────────────────

def display_stats_screen(player, clock):
    """Show detailed player statistics."""
    clear_screen()
    print_header(f"STATISTICS — {player.name}")
    print(f"  Play Time:       Day {clock.day}, {clock.hour:02d}:{clock.minute:02d}")
    print(f"  Level:           {player.level}")
    print(f"  Total XP:        {number_format(player.total_xp)}")
    print(f"  Deaths:          {player.deaths}")
    print(f"  Steps Taken:     {number_format(player.steps_taken)}")
    print_divider()
    print(colored("  COMBAT:", ANSI_RED))
    print(f"  Total Kills:     {number_format(sum(player.kills.values()))}")
    print(f"  Damage Dealt:    {number_format(player.damage_dealt)}")
    print(f"  Damage Taken:    {number_format(player.damage_taken)}")
    print(f"  Spells Cast:     {number_format(player.spells_cast)}")
    print_divider()
    if player.kills:
        print(colored("  KILLS BY TYPE:", ANSI_GRAY))
        for family, count in sorted(player.kills.items(), key=lambda x: -x[1]):
            icon = MONSTER_FAMILIES.get(family, {}).get("icon", "•")
            print(f"  {icon} {family:<15} {count}")
    print_divider()
    print(colored("  ECONOMY:", ANSI_YELLOW))
    print(f"  Gold Earned:     {number_format(player.gold_earned)}")
    print(f"  Current Gold:    {number_format(player.inventory.gold)}")
    print(f"  Items Crafted:   {player.crafted_items}")
    print_divider()
    print(colored("  ACHIEVEMENTS:", ANSI_MAGENTA))
    if player.achievements:
        for ach in player.achievements:
            print(f"  🏆 {ach}")
    else:
        print(colored("  None yet.", ANSI_GRAY))
    print_divider()
    print(colored("  JOURNAL ENTRIES:", ANSI_CYAN))
    for entry in player.journal[-10:]:
        print(f"  • {entry}")
    pause()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10: MAIN GAME LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main_menu():
    """Display the main menu and return a choice."""
    clear_screen()
    print(colored(ASCII_TITLE, ANSI_CYAN))
    print(colored(f"  v{VERSION}  — A Terminal RPG", ANSI_GRAY))
    print_divider()
    print("  [1] New Game")
    print("  [2] Load Game")
    print("  [3] Delete Save")
    print("  [4] Quit")
    print_divider()
    return ask("Choice", ["1", "2", "3", "4"])


def game_loop(player, world_map, clock):
    """The main game loop."""
    start_time = time.time()

    while True:
        x, y = player.world_x, player.world_y
        world_map.render(x, y)
        print(colored(f"\n  {clock.display()}", ANSI_GRAY))
        print(f"  {player.name}  HP:{player.hp}/{player.max_hp()}  MP:{player.mp}/{player.max_mp()}  Gold:{player.inventory.gold}")
        print_divider()
        print("  [W/A/S/D] Move   [E] Explore   [C] Character   [I] Inventory")
        print("  [Q] Quests   [P] Spells   [R] Craft   [T] Stats   [X] Save & Quit")

        cmd = input(colored("  ► ", ANSI_YELLOW)).strip().upper()

        player.play_time = int(time.time() - start_time)
        clock.advance(10)

        if cmd == "W":
            ny = y - 1
            if world_map.is_passable(x, ny):
                player.world_y = ny
                player.steps_taken += 1
                _check_random_encounter(player, world_map)
            else:
                print(colored("  Can't move there.", ANSI_RED))
                time.sleep(0.5)

        elif cmd == "S":
            ny = y + 1
            if world_map.is_passable(x, ny):
                player.world_y = ny
                player.steps_taken += 1
                _check_random_encounter(player, world_map)
            else:
                print(colored("  Can't move there.", ANSI_RED))
                time.sleep(0.5)

        elif cmd == "A":
            nx = x - 1
            if world_map.is_passable(nx, y):
                player.world_x = nx
                player.steps_taken += 1
                _check_random_encounter(player, world_map)
            else:
                print(colored("  Can't move there.", ANSI_RED))
                time.sleep(0.5)

        elif cmd == "D":
            nx = x + 1
            if world_map.is_passable(nx, y):
                player.world_x = nx
                player.steps_taken += 1
                _check_random_encounter(player, world_map)
            else:
                print(colored("  Can't move there.", ANSI_RED))
                time.sleep(0.5)

        elif cmd == "E":
            explore_location(player, world_map, clock)

        elif cmd == "C":
            clear_screen()
            player.display_status()
            player.stats.display()
            player.equipment.display()
            pause()

        elif cmd == "I":
            clear_screen()
            player.inventory.display()
            pause()

        elif cmd == "Q":
            clear_screen()
            player.display_quests()
            pause()

        elif cmd == "P":
            clear_screen()
            player.display_spellbook()
            pause()

        elif cmd == "R":
            _crafting_menu(player)

        elif cmd == "T":
            display_stats_screen(player, clock)

        elif cmd == "X":
            save_game(player, world_map, clock)
            print(colored("\n  Farewell, adventurer. The realm awaits your return.", ANSI_CYAN))
            break

        # Check if player died outside combat (e.g. DoT)
        if not player.is_alive:
            print(colored("\n  You have succumbed to your wounds...", ANSI_RED))
            player.deaths += 1
            player.is_alive = True
            player.hp = 1
            player.world_x = 9
            player.world_y = 4
            print(colored("  You wake up back at Ashenvale, barely alive.", ANSI_YELLOW))
            pause()


def _check_random_encounter(player, world_map):
    """On movement, randomly trigger a combat encounter."""
    enc_chance = world_map.get_encounter_chance(player.world_x, player.world_y)
    if percentage_chance(enc_chance // 3):
        monsters = world_map.get_encounter_monsters(
            player.world_x, player.world_y, player.level)
        run_combat(player, monsters)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 11: ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """Main entry point."""
    while True:
        choice = main_menu()

        if choice == "1":
            player = create_character()
            world_map = WorldMap()
            clock = GameClock()
            game_loop(player, world_map, clock)

        elif choice == "2":
            result = load_game()
            if result and result[0]:
                player, clock, world_map = result
                print(colored(f"\n  Welcome back, {player.name}!", ANSI_GREEN))
                pause()
                game_loop(player, world_map, clock)
            else:
                pause()

        elif choice == "3":
            delete_save()

        elif choice == "4":
            print(colored("\n  May your blade stay sharp, adventurer.\n", ANSI_CYAN))
            sys.exit(0)


if __name__ == "__main__":
    main()