# LEGACY FILE: See terminal_game/entities.py and terminal_game/main.py for the current text-based game logic.
# This file is no longer used in the refactored project structure.

# entities.py
# Define your game entities here (Player, Enemy, etc.)
import random
from re import X

# --- Ability System ---
class Ability:
    def __init__(self, name, action, description="", is_damage=False, blocking=False):
        self.name = name
        self.action = action  # function(user, target)
        self.description = description
        self.is_damage = is_damage
        self.blocking = False

    def use(self, user, target):
        return self.action(user, target)

# --- Status Effect System ---
class StatusEffect:
    def __init__(self, name, duration, on_apply=None, on_turn=None, on_expire=None):
        self.name = name
        self.duration = duration
        self.on_apply = on_apply
        self.on_turn = on_turn
        self.on_expire = on_expire

    def apply(self, character):
        if self.on_apply:
            self.on_apply(character)

    def turn(self, character):
        if self.on_turn:
            before = character.health
            self.on_turn(character)
            after = character.health
            if before != after:
                print(f"{character.name} suffers from {self.name}! Health: {character.health}")

    def expire(self, character):
        if self.on_expire:
            self.on_expire(character)

# --- Character Classes ---
class GameCharacter:
    def __init__(self, name, health=100, x=0, y=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.abilities = []
        self.status_effects = []  # List of (StatusEffect, turns_left)
        self.stunned = False
        self.x = x
        self.y = y
        self.blocking = False
        self.extra_turn = False  # Used for abilities that grant extra turns
        self.health_potions = 2  # Limited health potions
        self.healing_uses = 2  # Limited healing ability uses
        self.confusion_animation_triggered = False  # Flag for confusion animation

    def take_damage(self, amount):
        if self.blocking:
            self.blocking = False
            return f"{self.name} blocks the attack!"
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.on_defeat()

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def is_alive(self):
        return self.health > 0
    
    def on_defeat(self):
        pass

    def add_ability(self, ability):
        self.abilities.append(ability)

    def use_ability(self, index, target):
        if self.stunned:
            self.stunned = False  # Stun wears off after missing a turn
            return f"{self.name} is stunned and misses their turn!"
        if 0 <= index < len(self.abilities):
            # Check if target is blocking - this should happen for ANY move that targets the blocking character
            # The block should be consumed by the next move, regardless of what it is
            if hasattr(target, 'blocking') and target.blocking:
                target.blocking = False
                # Only block damage-dealing abilities, but still consume the block
                if self.abilities[index].is_damage:
                    return f"{target.name} blocks the move!"
            return self.abilities[index].use(self, target)
        else:
            return f"{self.name} tried to use an unknown ability!"
        
    def add_status_effect(self, effect):
        # If effect already present, refresh duration
        for i, (e, turns) in enumerate(self.status_effects):
            if e.name == effect.name:
                self.status_effects[i] = (effect, effect.duration)
                return f"{self.name} is already affected by {effect.name}, refreshing duration."
        self.status_effects.append((effect, effect.duration))
        effect.apply(self)
        return f"{self.name} is now affected by {effect.name}!"

    def process_status_effects(self):
        messages = []
        new_effects = []
        for effect, turns_left in self.status_effects:
            effect.turn(self)
            if turns_left > 1:
                new_effects.append((effect, turns_left - 1))
            else:
                effect.expire(self)
                messages.append(f"{self.name} is no longer affected by {effect.name}.")
        self.status_effects = new_effects
        return messages

# --- Ability Functions ---
def light_attack(user, target):
    damage = 8 + random.randint(2, 6)
    block_msg = target.take_damage(damage)
    if block_msg:
        return f"{user.name} uses Light Attack!\n{block_msg}"
    msg = f"{user.name} uses Light Attack! {target.name} takes {damage} damage."
    return msg


def heavy_strike(user, target):
    # Check for stun first to determine damage
    stun_occurs = random.random() < 0.25  # 25% chance to stun
    
    if stun_occurs:
        damage = 30  # Fixed 30 damage when stun occurs
    else:
        damage = 20  # Fixed 20 damage when no stun
    
    block_msg = target.take_damage(damage)
    if block_msg:
        return f"{user.name} uses Heavy Strike!\n{block_msg}"
    msg = f"{user.name} uses Heavy Strike! {target.name} takes {damage} damage."
    
    # Apply stun effect if it occurred
    if stun_occurs:
        stun_effect = StatusEffect(
            name="Stunned",
            duration=1,
            on_apply=lambda c: setattr(c, 'stunned', True),
            on_turn=None,
            on_expire=lambda c: setattr(c, 'stunned', False)
        )
        msg += f"\n{target.add_status_effect(stun_effect)}"
    return msg

def block_ability(user, target):
    if user.blocking:
        return f"{user.name} is already ready to block the next attack!"
    user.blocking = True
    return f"{user.name} is ready to block the next attack!"

def fireball(user, target):
    damage = 20 + random.randint(0, 5)
    block_msg = target.take_damage(damage)
    if block_msg:
        return f"{user.name} casts Fireball!\n{block_msg}"
    msg = f"{user.name} casts Fireball! {target.name} takes {damage} damage."
    # 25% chance to poison
    if random.random() < 0.25:
        poison_effect = StatusEffect(
            name="Poisoned",
            duration=3,
            on_apply=None,
            on_turn=lambda c: c.take_damage(random.randint(1, 5)),
            on_expire=None
        )
        msg += f"\n{target.add_status_effect(poison_effect)}"
    return msg

def heal_spell(user, target):
    # Check if user has healing uses remaining
    if user.healing_uses <= 0:
        return f"{user.name} has no healing uses remaining!"
    
    heal_amount = 25
    user.heal(heal_amount)
    user.healing_uses -= 1  # Consume one healing use
    return f"{user.name} casts Heal and restores {heal_amount} HP! ({user.healing_uses} healing uses remaining)"

def health_potion(user, target):
    # Check if user has health potions remaining
    if user.health_potions <= 0:
        return f"{user.name} has no health potions remaining!"
    
    heal_amount = 30
    user.heal(heal_amount)
    user.health_potions -= 1  # Consume one potion
    return f"{user.name} uses a Health Potion and restores {heal_amount} HP! ({user.health_potions} potions remaining)"

def slash_attack(user, target):
    damage = 10 + random.randint(5, 10)
    block_msg = target.take_damage(damage)
    if block_msg:
        return f"{user.name} uses Slash!\n{block_msg}"
    msg = f"{user.name} uses Slash! {target.name} takes {damage} damage."
    # 25% chance to bleed
    if random.random() < 0.25:
        bleed_effect = StatusEffect(
            name="Bleeding",
            duration=5,
            on_apply=None,
            on_turn=lambda c: c.take_damage(1),
            on_expire=None
        )
        msg += f"\n{target.add_status_effect(bleed_effect)}"
    return msg

def confusion(user, target):
    damage = 10
    block_msg = target.take_damage(damage)
    if block_msg:
        return f"{user.name} uses Confusion!\n{block_msg}"
    msg = f"{user.name} uses Confusion! {target.name} takes {damage} damage."
    # 20% chance for extra turn
    if random.random() < 0.2:
        user.stunned = False  # Ensure not stunned
        msg += f"\n{user.name} is empowered by confusion and gets another turn!"
        user.extra_turn = True
        # Set flag to trigger confusion animation (will be handled in main loop)
        user.confusion_animation_triggered = True
    else:
        user.extra_turn = False
    return msg

def souls(user, target):
    # Check if user has healing uses remaining
    if user.healing_uses <= 0:
        return f"{user.name} has no healing uses remaining!"
    
    heal_amount = 30
    user.heal(heal_amount)
    user.healing_uses -= 1  # Consume one healing use
    return f"{user.name} uses Souls! {user.name} steals the enemy's soul and heals for {heal_amount} HP! ({user.healing_uses} healing uses remaining)"

# --- Create Characters and Add Abilities ---
def create_warrior():
    w = GameCharacter("Duncan", 120)
    w.add_ability(Ability("Light Attack", light_attack, "A quick, reliable attack", is_damage=True))
    w.add_ability(Ability("Heavy Strike", heavy_strike, "A powerful melee attack with a chance to stun.", is_damage=True))
    w.add_ability(Ability("Block", block_ability, "Block the next attack.", blocking=True))
    w.add_ability(Ability("Health Potion", health_potion, "Restore health by 30 HP."))
    return w

def create_mage():
    m = GameCharacter("Gandalf", 80)
    m.add_ability(Ability("Light Attack", light_attack, "A quick, reliable attack", is_damage=True))
    m.add_ability(Ability("Fireball", fireball, "A fiery magical attack with a chance to poison.", is_damage=True))
    m.add_ability(Ability("Heal", heal_spell, "Restore health to yourself."))
    m.add_ability(Ability("Health Potion", health_potion, "Restore health by 30 HP. "))
    return m

def create_ghost():
    g = GameCharacter("Ghost", 100)
    g.add_ability(Ability("Light Attack", light_attack, "A quick, reliable attack", is_damage=True))
    g.add_ability(Ability("Slash", slash_attack, "A powerful slash with a chance to cause bleeding.", is_damage=True))
    g.add_ability(Ability("Confusion", confusion, "A confusing attack that may grant another turn."))
    g.add_ability(Ability("Souls", souls, "Steal the enemy's soul and heal yourself."))
    g.extra_turn = False  # Used for Confusion ability
    return g

def draw_health_bar(screen, x, y, current_health, max_health, width=200, height=20):
    # Implementation of draw_health_bar function
    pass
