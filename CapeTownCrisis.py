import random

class Household:
    def __init__(self, i):
        self.id = i
        self.priors = [1 / 3] * 3

    def chooseTap(self):
        bestI = 0
        bestP = self.priors[bestI]
        for i in range(len(self.priors)):
            prior = self.priors[i]
            if prior > bestP:
                bestI = i
                bestP = prior
            elif prior == bestP:
                if random.randint(0, 1) == 0:
                    bestI = i
                    bestP = prior
        return bestI

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
        string += 'visitors (' + str(len(self.visitors)) + '):\n'
        for visitor in self.visitors:
            string += '\t' + str(visitor) + '\n'
        return string

class CapeTown:
    def __init__(self):
        self.reset()

    def runPrivateOnly(self):
        self.reset()
        for household in self.households:
            self.chooseTap(household)
        return self.sequentialKnowledge

    def chooseTap(self, household):
        chosenTap = household.chooseTap()
        self.sequentialKnowledge.append(chosenTap)
        self.taps[chosenTap].visit(household)

    def reset(self):
        self.taps = [0] * 3
        for i in range(len(self.taps)):
            self.taps[i] = Tap(i)
        self.taps[0].isAvailable = True

        self.households = [0] * random.randint(20, 50)
        for i in range(len(self.households)):
            self.households[i] = Household(i)

        self.sequentialKnowledge = []

    def __str__(self):
        string = 'SEQUENTIAL KNOWLEDGE (' + str(len(self.sequentialKnowledge)) + '):\n\t' + str(self.sequentialKnowledge) + '\n'
        string += 'TAPS (' + str(len(self.taps)) + '):\n'
        for tap in self.taps:
            string += str(tap) + '\n'
        string += 'HOUSEHOLDS (' + str(len(self.households)) + '):\n'
        for household in self.households:
            string += str(household) + '\n'
        return string

capeTown = CapeTown()
print('-- BEFORE -------------------------------------------------------------------------------------')
print(capeTown)
print('-- PRIVATE ------------------------------------------------------------------------------------')
print(capeTown.runPrivateOnly())
print('-- AFTER --------------------------------------------------------------------------------------')
print(capeTown)
print()

capeTown.reset()
print('-- BEFORE -------------------------------------------------------------------------------------')
print(capeTown)
print('-- PRIVATE ------------------------------------------------------------------------------------')
print(capeTown.runPrivateOnly())
print('-- AFTER --------------------------------------------------------------------------------------')
print(capeTown)
print()

capeTown.reset()
print('-- BEFORE -------------------------------------------------------------------------------------')
print(capeTown)
print('-- PRIVATE ------------------------------------------------------------------------------------')
print(capeTown.runPrivateOnly())
print('-- AFTER --------------------------------------------------------------------------------------')
print(capeTown)
print()

