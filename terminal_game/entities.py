# LEGACY FILE: See terminal_game/entities.py and terminal_game/main.py for the current text-based game logic.
# This file is no longer used in the refactored project structure.

# entities.py
# Define your game entities here (Player, Enemy, etc.)
import random
from re import X

# --- Ability System ---
class Ability:
    def __init__(self, name, action, description=""):
        self.name = name
        self.action = action  # function(user, target)
        self.description = description

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

    def take_damage(self, amount):
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
def heavy_strike(user, target):
    damage = 15 + random.randint(5, 15)
    msg = f"{user.name} uses Heavy Strike! {target.name} takes {damage} damage."
    target.take_damage(damage)
    # 30% chance to stun
    if random.random() < 0.3:
        stun_effect = StatusEffect(
            name="Stunned",
            duration=1,
            on_apply=lambda c: setattr(c, 'stunned', True),
            on_turn=None,
            on_expire=lambda c: setattr(c, 'stunned', False)
        )
        msg += f"\n{target.add_status_effect(stun_effect)}"
    return msg

def fireball(user, target):
    damage = 20 + random.randint(10, 20)
    msg = f"{user.name} casts Fireball! {target.name} takes {damage} damage."
    target.take_damage(damage)
    # 40% chance to poison
    if random.random() < 0.4:
        poison_effect = StatusEffect(
            name="Poisoned",
            duration=3,
            on_apply=None,
            on_turn=lambda c: c.take_damage(5),
            on_expire=None
        )
        msg += f"\n{target.add_status_effect(poison_effect)}"
    return msg

def heal_spell(user, target):
    heal_amount = 25
    user.heal(heal_amount)
    return f"{user.name} casts Heal and restores {heal_amount} HP!"

def health_potion(user, target):
    heal_amount = 30
    user.heal(heal_amount)
    return f"{user.name} uses a Health Potion and restores {heal_amount} HP!"

def choose_ability(character, target):
    print(f"\n{character.name}'s turn!")
    print(f"Health: {character.health}/{character.max_health}")
    print("Abilities:")
    for idx, ability in enumerate(character.abilities):
        print(f"{idx}: {ability.name} - {ability.description}")
    while True:
        try:
            choice = int(input("Choose ability number for {character.name}: "))
            if 0 <= choice < len(character.abilities):
                print()
                return character.use_ability(choice, target)
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

# --- Create Characters and Add Abilities ---
def create_warrior():
    w = GameCharacter("Duncan", 120)
    w.add_ability(Ability("Heavy Strike", heavy_strike, "A powerful melee attack with a chance to stun."))
    w.add_ability(Ability("Health Potion", health_potion, "Restore health by 30 HP."))
    return w

def create_mage():
    m = GameCharacter("Gandalf", 80)
    m.add_ability(Ability("Fireball", fireball, "A fiery magical attack with a chance to poison."))
    m.add_ability(Ability("Heal", heal_spell, "Restore health to yourself."))
    m.add_ability(Ability("Health Potion", health_potion, "Restore health by 30 HP. "))
    return m

# Character selection
characters = {
    "warrior": create_warrior,
    "mage": create_mage
}

def select_character(player_num, taken=None):
    print(f"\nPlayer {player_num}, choose your character:")
    options = [name for name in characters if name != taken]
    for idx, name in enumerate(options):
        print(f"{idx}: {name.capitalize()}")
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 0 <= choice < len(options):
                chosen = options[choice]
                char = characters[chosen]()
                custom_name = input(f"Enter a custom name for your {chosen.capitalize()} (or press Enter to use default): ").strip()
                if custom_name:
                    char.name = custom_name
                else:
                    char.name = chosen.capitalize()
                print(f"Player {player_num} chose {char.name} the {chosen.capitalize()}!\n")
                return char, chosen
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")
            
player1, chosen1 = select_character(1)
player2, chosen2 = select_character(2, taken=chosen1)

# --- Battle Loop ---
print("Battle begins!")
turn = 0
while player1.is_alive() and player2.is_alive():
    print(f"--- Turn {turn+1} ---")
    # Each character processes their status effects at the start of their turn
    for char in [player1, player2]:
        for msg in char.process_status_effects():
            print(msg)
    if player1.is_alive():
        print(choose_ability(player1, player2))
    if player2.is_alive():
        print(choose_ability(player2, player1))
    print(f"{player1.name}: {player1.health} HP, {player2.name}: {player2.health} HP\n")
    input("Press Enter to continue...")
    turn += 1
winner = player1 if player1.is_alive() else player2
print(f"Battle ended! {winner.name} the {chosen1 if winner == player1 else chosen2} wins!")
