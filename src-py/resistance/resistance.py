from agent import Agent
import random
class Resistance(Agent):
    '''An abstract super class for an agent in the game The Resistance.
    new_game and *_outcome methods simply inform agents of events that have occured,
    while propose_mission, vote, and betray require the agent to commit some action.'''

    #game parameters for agents to access
    #python is such that these variables could be mutated, so tournament play
    #will be conducted via web sockets.
    #e.g. self.mission_size[8][3] is the number to be sent on the 3rd mission in a game of 8
    mission_sizes = {
            5:[2,3,2,3,3], \
            6:[3,3,3,3,3], \
            7:[2,3,3,4,5], \
            8:[3,4,4,5,5], \
            9:[3,4,4,5,5], \
            10:[3,4,4,5,5]
            }
    #number of spies for different game sizes
    spy_count = {5:2, 6:2, 7:3, 8:3, 9:3, 10:4} 
    #e.g. self.betrayals_required[8][3] is the number of betrayals required for the 3rd mission in a game of 8 to fail
    fails_required = {
            5:[1,1,1,1,1], \
            6:[1,1,1,1,1], \
            7:[1,1,1,2,1], \
            8:[1,1,1,2,1], \
            9:[1,1,1,2,1], \
            10:[1,1,1,2,1]
            }

    def __init__(self, name):
        '''
        Initialises the agent, and gives it a name
        You can add configuration parameters etc here,
        but the default code will always assume a 1-parameter constructor, which is the agent's name.
        The agent will persist between games to allow for long-term learning etc.
        '''
        self.name = name

    def __str__(self):
        '''
        Returns a string represnetation of the agent
        '''
        return 'Agent '+self.name

    def __repr__(self):
        '''
        returns a representation fthe state of the agent.
        default implementation is just the name, but this may be overridden for debugging
        '''
        return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        '''
        initialises the game, informing the agent of the number_of_players, 
        the player_number (an id number for the agent in the game),
        and a list of agent indexes, which is the set of spies if this agent is a spy,
        or an empty list if this agent is not a spy.
        '''
        self.mSize = self.mission_sizes[number_of_players]
        self.nSpy = self.spy_count[number_of_players]
        self.nFails = self.fails_required[number_of_players]
        
        self.id = player_number
        self.spies = spies
        self.N = number_of_players

        self.player_sus = [self.nSpy / (self.N - 1) for _ in range(number_of_players)]
        self.player_sus[self.id] = 0

        self.M = 1
        self.R = 1

        self.success = 0
        self.failure = 0


    def propose_mission(self, team_size, fails_required = 1):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        fails_required are the number of fails required for the mission to fail.
        '''
        team = []
        team.append(self.id)
        while len(team) < team_size:
            i = random.randrange(0, self.N)
            if not i in self.spies and i not in team:
                team.append(i)
        return team

    def vote(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        return True
        if self.R == 5:
            return True
        elif self.id in mission:
            return True
        else:
            return False

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        self.R += 1
        pass

    def betray(self, mission, proposer):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        Only spies are permitted to betray the mission. 
        '''
        return False

    def update_information(self, mission, num_fails):
        '''
        Apply Bayes' Rule to update the probability of each member of being a spy
        P(A|B) = P(B|A) * P(A) / P(B)
        P(A is a spy | n fails) = P(n fails | A is a spy) * P(A is a spy) / P(n fails)
        '''
        # if not self.id == 0:
        #     return
        total_permutations = 2**len(mission) # each player has 2 choices, succeed or fail
        prev = self.player_sus.copy()
        FAIL_RATE = (3 - self.failure) / (5 - self.M + 1) # e.g. for first mission: (3 - 0) / (5 - 1 + 1) = 3/5 = 0.6
        if FAIL_RATE < 0.001:
            FAIL_RATE = 1
        

        valid_permutations = []
        for p in range(total_permutations):
            pb = "{0:b}".format(p).zfill(len(mission))
            if pb.count('1') == num_fails:
                valid_permutations.append(pb)

        pB = 0
        for p in valid_permutations:
            probability = 1
            for i in range(len(p)):

                if p[i] == '1': # fail
                    # probability of being a spy and failing
                    probability *= (prev[mission[i]] * FAIL_RATE)      
                else:       # p[i] = 0 -> succeed
                    # probability succeeding as a spy and probability of being a res
                    probability *= (prev[mission[i]] * (1 - FAIL_RATE) + (1 - prev[mission[i]])) 
            
            pB += probability
        # print('=====================')
        # print(mission, num_fails, FAIL_RATE, self.player_sus)
        # print(pB)
        # print(valid_permutations)
        # input('=====================')

        for m in range(len(mission)):
            pBA = 0
            for p in valid_permutations:
                probability = 1
                for i in range(len(p)):
                    if i == m:
                        if p[i] == '1':
                            probability *= FAIL_RATE
                        else:
                            probability *= (1 - FAIL_RATE)
                    else:
                        if p[i] == '1':
                            probability *= (prev[mission[i]] * FAIL_RATE)
                        else:
                            probability *= (prev[mission[i]] * (1 - FAIL_RATE) +  (1 - prev[mission[i]]))
                pBA += probability
            
            pA = prev[mission[m]]

            pAB = (pBA * pA) / pB
            self.player_sus[mission[m]] = pAB

        # print(self.player_sus)
        # x = input("----------------------")
        
    def mission_outcome(self, mission, proposer, num_fails, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        num_fails is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It iss not expected or required for this function to return anything.
        '''
        self.update_information(mission, num_fails)

        self.M += 1
        self.R = 1
        self.success += mission_success
        self.failure += 1 - mission_success

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        if self.id == 0:
            print(self.player_sus)
            input("------GAME FINISHED------")


