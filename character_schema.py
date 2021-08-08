#dependencies: pymongo, decouple

'''
client = pymongo.MongoClient(config("MONGO_CONNECTION"), connect=False)
db = client['avalon']
collection = db['characters']
'''

class Character:
    def __init__(self):
        # Info
        self.nome = "default"
        self.jogador = "default_player"

        # Attributes
        self.strength = 10
        self.dextery = 10
        self.constitution = 10
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10

        self.speed = 30

        self.first_class = "artificer" # Initial Health Die

        self.pv_max = 10

        self.exp = 0
        self.gold = 0

        self.items = []

        self.level = {
            "artificer": 0,
            "barbarian": 0,
            "bard": 0,
            "cleric": 0,
            "druid": 0,
            "fighter": 0,
            "monk": 0,
            "paladin": 0,
            "ranger": 0,
            "rogue": 0,
            "sorcerer": 0,
            "warlock": 0,
            "wizard": 0,
        }

        self.saving_throw_proficiency = {
            "strength": False,
            "dextery": False,
            "constitution": False,
            "intelligence": False,
            "wisdom": False,
            "charisma": False,
        }

        self.skill_proficiency = {
            'athletics': False,
            'acrobatics': False,
            'sleight of hand': False,
            'stealth': False,
            'arcana': False,
            'history': False,
            'investigation': False,
            'nature': False,
            'religion': False,
            'animal handling': False,
            'insight': False,
            'medicine': False,
            'perception': False,
            'survival': False,
            'deception': False,
            'intimidation': False,
            'performance': False,
            'persuasion': False,
        }

        self.skill_expertise = {
            'athletics': False,
            'acrobatics': False,
            'sleight of hand': False,
            'stealth': False,
            'arcana': False,
            'history': False,
            'investigation': False,
            'nature': False,
            'religion': False,
            'animal handling': False,
            'insight': False,
            'medicine': False,
            'perception': False,
            'survival': False,
            'deception': False,
            'intimidation': False,
            'performance': False,
            'persuasion': False,
        }

    # Proficiency bonus
    def prof(self):
        return (total_level()-1)//4 + 2

    # Total level
    def total_level(self):
        return sum(self.level.values())

    # Returns the attribute modifier of the attribute value
    def mod(self, attr):
        value = 0
        if attr.lower() == "str":
            value = self.strength
        elif attr.lower() == "dex":
            value = self.dextery
        elif attr.lower() == "con":
            value = self.constitution
        elif attr.lower() == "int":
            value = self.intelligence
        elif attr.lower() == "wis":
            value = self.wisdom
        elif attr.lower() == "chr":
            value = self.charisma
        else:
            return -10
        return (value-10)//2

    # Calculates the bonus in the correlated skill
    def skill_bonus(self, skill):
        value = 0
        skill = skill.lower()

        if self.skill_proficiency[skill]:
            value += self.prof()
        if self.skill_expertise[skill]:
            value += self.prof()

        if skill in ["athletics"]:
            value += self.mod('str')
        elif skill in ["acrobatics", "sleight of hand", "stealth"]:
            value += self.mod('dex')
        elif skill in ["arcana", "history", "investigation", "nature", "religion"]:
            value += self.mod('int')
        elif skill in ["animal handling", "insight", "medicine", "perception", "survival"]:
            value += self.mod('wis')
        elif skill in ["deception", "intimidation", "performance", "persuasion"]:
            value += self.mod('chr')

        return value

    # Convert to dictionary
    def dictify(self):
        dic = {
            "nome": self.nome,
            "jogador": self.jogador,

            "strength": self.strength,
            "dextery": self.dextery,
            "constitution": self.constitution,
            "intelligence": self.intelligence,
            "wisdom": self.wisdom,
            "charisma": self.charisma,

            "speed": self.speed,
            "first_class": self.first_class,

            "pv_max": self.pv_max,

            "exp": self.exp,
            "gold": self.gold,

            "items": self.items,

            "level": self.level,

            "saving_throw_proficiency": self.saving_throw_proficiency,
            "skill_proficiency": self.skill_proficiency,
            "skill_expertise": self.skill_expertise,
        }
        print(type(dic))
        return dic

    def _pre_save(self, collection):
        return True

    def save(self, collection):
        if not self._pre_save(collection):
            print("ERROR SAVING CHARACTER OBJECT\n", self)
            return False

        collection.insert_one(self.dictify())
