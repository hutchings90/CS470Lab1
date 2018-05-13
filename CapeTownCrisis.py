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
        self.utilityVisitors = []

    def visit(self, visitor):
        self.visitors.append(visitor.id)
        return self.visitors

    def utilityVisit(self, visitor):
        self.utilityVisitors.append(visitor.id)
        return self.visitors

    def __str__(self):
        string = 'id:\n\t' + str(self.id) + '\n'
        string += 'isAvailable:\n\t' + str(self.isAvailable) + '\n'
        string += 'visitors (' + str(len(self.visitors)) + '):\n\t' + str(self.visitors) + '\n'
        string += 'utilityVisitors (' + str(len(self.utilityVisitors)) + '):\n\t' + str(self.utilityVisitors)
        return string

class CapeTown:
    likelihoodOptions = [
        [[1 / 3, 1 / 3, 1 / 3], [1 / 3, 1 / 3, 1 / 3], [1 / 3, 1 / 3, 1 / 3]],
        # [[, , ], [, , ], [, , ]],
        [[10.2 / 36.2, 8.6 / 36.2, 17.4 / 36.2], [17.4 / 36.2, 10.2 / 36.2, 8.6 / 36.2], [8.6 / 36.2, 17.4 / 36.2, 10.2 / 36.2]],
        [[17.4 / 36.2, 10.2 / 36.2, 8.6 / 36.2], [8.6 / 36.2, 17.4 / 36.2, 10.2 / 36.2], [10.2 / 36.2, 8.6 / 36.2, 17.4 / 36.2]],
        [[8.6 / 36.2, 17.4 / 36.2, 10.2 / 36.2], [10.2 / 36.2, 8.6 / 36.2, 17.4 / 36.2],[17.4 / 36.2, 10.2 / 36.2, 8.6 / 36.2]]
    ]
    utilities = [[100, -70, -70], [-70, 100, -70], [-70, -70, 100]]

    numAgentOptions = [.5, .15, .25, .35, .45]
    accuracyOptions = ['fixed', 'accurate', 'inaccurate', 'random']
    boundOptions = [.05, .1, .15, .2]

    def __init__(self):
        self.run()
        self.cascadeAndUtilityRun()

    def run(self):
        print('Run')
        for accuracy in CapeTown.accuracyOptions:
            for bound in CapeTown.boundOptions:
                self.reset(CapeTown.likelihoodOptions[0])
                lowerBound = int(len(self.households) * .55)
                upperBound = int(len(self.households) * .85)
                numAgents = random.randint(lowerBound, upperBound)
                self.setPriors(accuracy, bound, numAgents)
                for household in self.households:
                    self.chooseTap(household)
                print('\t(' + str(accuracy) + ', ' + str(bound) + ')')
                for i in range(len(self.taps)):
                    print('\t\t' + str(i) + ':\t' + str(len(self.taps[i].visitors)))
        print('Done\n')

    def cascadeAndUtilityRun(self):
        print('Cascade Run')
        for likelihoods in CapeTown.likelihoodOptions:
            for numAgents in CapeTown.numAgentOptions:
                for accuracy in CapeTown.accuracyOptions:
                    for bound in CapeTown.boundOptions:
                        print(likelihoods, numAgents, accuracy, bound)
                        self.reset(likelihoods)
                        self.setPriors(accuracy, bound, int(numAgents * len(self.households)))
                        self.chooseTap(self.households[0])
                        self.chooseTapUtility(self.households[0])
                        tapChosen = self.sequentialKnowledge[0]
                        for i in range(1, len(self.households)):
                            self.calculatePosterior(i,tapChosen)
                            self.chooseTap(self.households[i])
                            self.chooseTapUtility(self.households[i])
                            tapChosen= self.sequentialKnowledge[i]
                    for i in range(len(self.taps)):
                        print('\t\tTap', i)
                        print('\t\t\tvisitors:\t' + str(len(self.taps[i].visitors)))
                        print('\t\t\tutility visitors:\t' + str(len(self.taps[i].utilityVisitors)))
        print('Done\n')

    def calculatePosterior(self,count, tapChosen):
        for x in range(count, len(self.households)):
            sum = 0
            postProb= [0]*3
            for i in range(3):  # i is index for working tap number
                pos = self.likelihoods[tapChosen][i]
                postProb[i] = self.households[x].priors[i] * pos
                sum += postProb[i]
            alpha = 1 / sum
            for j in range(3):
                self.households[x].priors[j] = postProb[j]*alpha

    def chooseTapUtility(self, household):
        utilityValues = [0] * 3
        for i in range(3):
            for j in range(3):
                utilityValues[i] += self.utilities[i][j] * household.priors[j]
        bestUtility = max(utilityValues)
        bestUtilityIndices = []
        for i in range(3):
            if (utilityValues[i]== bestUtility):
                bestUtilityIndices.append(i)
        self.visitTapUtility(bestUtilityIndices[random.randint(0, len(bestUtilityIndices) - 1)], household)

    def setPriors(self, accuracy, bound, numAgents):
        if accuracy == 'accurate':
            self.accuratePriors(bound, numAgents)
        elif accuracy == 'inaccurate':
            self.inaccuratePriors(bound, numAgents)
        elif accuracy == 'random':
            self.randomPriors()

    def accuratePriors(self, bound, stop):
        inc = random.uniform(.01, bound)
        for i in range(stop):
            household = self.households[i]
            household.priors[0] += inc
            household.priors[1] -= random.uniform(0,inc)
            household.priors[2] = 1 - household.priors[0] - household.priors[1]

    def inaccuratePriors(self, bound, stop):
        inc = random.uniform(.01, bound)
        for i in range(stop):
            household = self.households[i]
            household.priors[0] -= inc
            household.priors[1] += random.uniform(0, inc)
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

    def visitTapUtility(self, chosenTap, household):
        self.sequentialKnowledge.append(chosenTap)
        self.taps[chosenTap].utilityVisit(household)

    def reset(self, likelihoods):
        self.likelihoods = likelihoods

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
