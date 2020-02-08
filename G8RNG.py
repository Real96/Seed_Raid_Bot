class PMString:
    natures = ["HARDY", "LONELY", "BRAVE", "ADAMANT", "NAUGHTY", "BOLD", "DOCILE",
           "RELAXED", "IMPISH", "LAX", "TIMID", "HASTY", "SERIOUS", "JOLLY",
           "NAIVE", "MODEST", "MILD", "QUIET", "BASHFUL", "RASH", "CALM",
           "GENTLE", "SASSY", "CAREFUL", "QUIRKY"]

class XOROSHIRO:
    ulongmask = 2 ** 64 - 1
    uintmask = 2 ** 32 - 1

    def __init__(self, seed, seed2 = 0x82A2B175229D6A5B):
            self.seed = [seed, seed2]

    @staticmethod
    def rotl(x, k):
        return ((x << k) | (x >> (64 - k))) & XOROSHIRO.ulongmask

    def next(self):
        s0, s1 = self.seed
        result = (s0 + s1) & XOROSHIRO.ulongmask
        s1 ^= s0
        self.seed = [XOROSHIRO.rotl(s0, 24) ^ s1 ^ ((s1 << 16) & XOROSHIRO.ulongmask), XOROSHIRO.rotl(s1, 37)]
        return result
    
    def randRoll(self, thresh, mask):
        res = self.next() & mask
        while res >= thresh:
            res = self.next() & mask
        return res

    def rand(self, mask):
        return self.next() & mask

class Raid:
    def __init__(self,seed,isToxtricity,flawlessiv, HA = 0, RandomGender = 1):
        self.seed = seed

        r = XOROSHIRO(seed)
        self.EC = r.randRoll(0xffffffff, 0xffffffff)
        OTID = r.randRoll(0xffffffff, 0xffffffff)
        self.PID = r.randRoll(0xffffffff, 0xffffffff)

        
        toxtricityAmpedNatures = [3, 4, 2, 8, 9, 19, 22, 11, 13, 14, 0, 6, 24]
        toxtricityLowKeyNatures = [1, 5, 7, 10, 12, 15, 16, 17, 18, 20, 21, 23]

        self.XOR = (self.PID >> 16) ^ (self.PID & 0xFFFF) ^ (OTID >> 16) ^ (OTID & 0xFFFF)
        if self.XOR >= 16:
            self.ShinyType = 'None'
        else:
            self.ShinyType = 'Star' if self.XOR else 'Square'

        i = 0
        self.IVs = [0,0,0,0,0,0]
        while i < flawlessiv:
            stat = r.randRoll(6, 7)
            if self.IVs[stat] == 0:
                self.IVs[stat] = 31
                i += 1
        for i in range(6):
            if self.IVs[i] == 0:
                self.IVs[i] = r.rand(31)

        if HA:
            self.Ability = r.randRoll(3, 3) + 1
        else:
            self.Ability = r.rand(1) + 1
        if self.Ability == 3:
            self.Ability = 'H'
        if RandomGender:
            self.Gender = r.randRoll(253, 255) + 1
        else:
            self.Gender = 0

        if isToxtricity == 0:
            self.Nature_pointer = r.randRoll(25, 31)
        elif isToxtricity == 1:
            self.Nature_pointer = toxtricityAmpedNatures[r.randRoll(13, 15)]
        else:
            self.Nature_pointer = toxtricityLowKeyNatures[r.randRoll(12, 15)]

        self.Nature = PMString.natures[self.Nature_pointer]

    def print(self):
        print(f"Seed:{self.seed:016X}\tShinyType:{self.ShinyType}\tEC:{self.EC:08X}\tPID:{self.PID:08X}\tAbility:{self.Ability}\tGender:{self.Gender}\tNature:{PMString.natures[self.Nature_pointer]}\tIVs:{self.IVs}")
