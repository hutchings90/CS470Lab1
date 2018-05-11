import random

class Household:
    def __init__(self, i, priors):
        self.id = i
        self.priors = priors

    def chooseTap(self):
        self.priors.sort()
        return self.priors[-1]

    def __str__(self):
        string = 'id:\n\t' + str(self.id) + '\npriors:\n'
        priorTotal = 0
        for prior in self.priors:
            string += '\t' + str(prior) + '\n'
            priorTotal += prior
        string += 'priorTotal:\n\t' + str(priorTotal) + '\n'
        string += 'functions:\n\tchooseTap'
        return string

class Tap:
    def __init__(self, i):
        self.id = i
        self.isAvailable = False
        self.visitors = []

    def visit(self, visitor):
        self.visitors.append(visitor.id)
        return self.visitors

    def __str__(self):
        string = 'id:\n\t' + str(self.id)
        string = 'isAvailable:\n\t' + str(self.isAvailable) + '\n'
        string += 'visitors (' + str(len(self.visitors)) + ':\n'
        for visitor in self.visitors:
            string += '\t' + str(visitor) + '\n'
        string += 'functions:\n\tvisit'
        return string

class CapeTown:
    def __init__(self, accuracy):
        self.taps = [0] * 3
        for i in range(len(self.taps)):
            self.taps[i] = Tap(i)
        availableTap = random.randint(0, len(self.taps) - 1)
        self.taps[availableTap].isAvailable = True

        self.households = [0] * random.randint(20, 50)
        if accuracy == 1:
            self.weightedHouseholds([availableTap])
        elif accuracy == 2:
            options = []
            for i in range(len(self.taps)):
                if i != availableTap:
                    options.append(i)
            self.weightedHouseholds(options)
        else:
            self.randomHouseholds(0, len(self.households))

        self.sequentialKnowledge = []

    def weightedHouseholds(self, tapIds):
        num = len(self.households)
        switchPoint = random.randint((num // 2) + 1, num)
        for i in range(0, switchPoint):
            self.households[i] = Household(i, self.weightedPriors(tapIds[random.randint(0, len(tapIds) - 1)]))
        self.randomHouseholds(switchPoint, num)
        random.shuffle(self.households)

    def weightedPriors(self, tapId):
        priors = [0] * 3
        others = []
        probability = 1
        priors[tapId] = random.uniform(.34, probability)
        probability = probability - priors[tapId]
        for i in range(len(priors)):
            if i != tapId:
                others.append(i)
        half = probability / 2
        priors[others[0]] = random.uniform(half, probability) - half
        probability = probability - priors[0]
        priors[others[1]] = probability
        return priors

    def randomHouseholds(self, start, end):
        for i in range(start, end):
            self.households[i] = Household(i, self.randomPriors())

    def randomPriors(self):
        priors = [0] * 3
        probability = 1
        priors[0] = random.uniform(0, probability)
        probability -= priors[0]
        priors[1] = random.uniform(0, probability)
        priors[2] = probability - priors[1]
        return priors

    def runPrivateOnly(self):
        for household in self.households:
            household.chooseTap()

    def __str__(self):
        string = 'HOUSEHOLDS (' + str(len(self.households)) + '):\n'
        for household in self.households:
            string += str(household) + '\n'
        string += 'TAPS (' + str(len(self.taps)) + '):\n'
        for tap in self.taps:
            string += str(tap) + '\n'
        string += 'SEQUENTIAL KNOWLEDGE (' + str(len(self.sequentialKnowledge)) + '):\n'
        for knowlege in self.sequentialKnowledge:
            string += '\t' + knowledge + '\n'
        return string

capeTown = CapeTown(1)
print(capeTown.runPrivateOnly())

capeTown = CapeTown(2)
print(capeTown.runPrivateOnly())

capeTown = CapeTown(3)
print(capeTown.runPrivateOnly())

