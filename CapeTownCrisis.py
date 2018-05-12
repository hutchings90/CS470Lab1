import random

class Household:
    def __init__(self, i):
        self.id = i
        self.priors = [1 / 3] * 3

    def chooseTap(self):
        bestP = max(self.priors)
        bestIndices = []
        for i in range(3):
            if self.priors[i] == bestP:
                bestIndices.append(i)
        random.shuffle(bestIndices)
        return bestIndices[random.randint(0, len(bestIndices) - 1)]

    def __str__(self):
        string = 'id:\n\t' + str(self.id) + '\npriors:\n'
        priorTotal = 0
        for prior in self.priors:
            string += '\t' + str(prior) + '\n'
            priorTotal += prior
        string += 'priorTotal:\n\t' + str(priorTotal) + '\n'
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
        string = 'id:\n\t' + str(self.id) + '\n'
        string += 'isAvailable:\n\t' + str(self.isAvailable) + '\n'
        string += 'visitors (' + str(len(self.visitors)) + '):\n\t' + str(self.visitors)
        return string

class CapeTown:
    def __init__(self):
        self.reset()

    def run(self, accuracy, bound):
        self.reset()
        self.setPriors(accuracy, bound)
        for household in self.households:
            self.chooseTap(household)
        string = ''
        for i in range(len(self.taps)):
            string += '\t' + str(i) + '\t' + str(len(self.taps[i].visitors)) + '\n'
        return string

    def cascadeRun(self):
        pass

    def setPriors(self, accuracy, bound):
        if accuracy == 1:
            self.accuratePriors(bound)
        elif accuracy == 2:
            self.inaccuratePriors(bound)
        elif accuracy == 3:
            self.randomPriors()

    def accuratePriors(self, bound):
        inc = random.uniform(.01, bound)
        stop = random.randint(int(len(self.households) * .55), int(len(self.households) * .85))
        for i in range(stop):
            household = self.households[i]
            household.priors[0] += inc
            household.priors[1] -= random.uniform(0, inc / 2)
            household.priors[2] = 1 - household.priors[0] - household.priors[1]

    def inaccuratePriors(self, bound):
        inc = random.uniform(.01, bound)
        stop = random.randint(int(len(self.households) * .55), int(len(self.households) * .85))
        for i in range(stop):
            household = self.households[i]
            household.priors[0] -= inc
            household.priors[1] += random.uniform(0, inc / 2)
            household.priors[2] = 1 - household.priors[0] - household.priors[1]

    def randomPriors(self):
        for household in self.households:
            priors = [0] * 3
            probability = 1
            priors[0] = random.uniform(0, probability)
            probability -= priors[0]
            priors[1] = random.uniform(0, probability)
            priors[2] = probability - priors[1]
            household.priors = priors

    def chooseTap(self, household):
        chosenTap = household.chooseTap()
        self.sequentialKnowledge.append(chosenTap)
        self.taps[chosenTap].visit(household)

    def reset(self):
        self.taps = [0] * 3
        for i in range(3):
            self.taps[i] = Tap(i)
        self.taps[0].isAvailable = True

        self.households = [0] * random.randint(20, 50)
        for i in range(len(self.households)):
            self.households[i] = Household(i)

        self.sequentialKnowledge = []

    def __str__(self):
        string = 'SEQUENTIAL KNOWLEDGE (' + str(len(self.sequentialKnowledge)) + '):\n\t' + str(self.sequentialKnowledge) + '\n'
        string += 'TAPS (' + str(3) + '):\n'
        for tap in self.taps:
            string += str(tap) + '\n'
        string += 'HOUSEHOLDS (' + str(len(self.households)) + '):\n'
        for household in self.households:
            string += str(household) + '\n'
        return string

capeTown = CapeTown()
r = range(5)
print('-- FIXED --------------------------------------------------------------------')
for i in r:
    print(str(i) + capeTown.run(None, None))
    print()

print('-- ACCURATE -----------------------------------------------------------------')
for i in r:
    print(str(i) + capeTown.run(1, .1))
    print()

print('-- INACCURATE ---------------------------------------------------------------')
for i in r:
    print(str(i) + capeTown.run(2, .1))
    print()

print('-- RANDOM -------------------------------------------------------------------')
for i in r:
    print(str(i) + capeTown.run(3, None))
    print()

