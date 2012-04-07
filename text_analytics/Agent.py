import random
import Lexicon

"""
An Agent is the encapsulation of an personal identity and an opinion - represented as a vector

Each individual i has got an opinion (an attitude)
xi, 

and a threshold determining the
latitude of rejection ti with ti > ui .Varying the values of ti and ui allows for modeling agents
having different attitude structures. For example, an agent having a high ego-involvement
can be formalized as an agent where ti is slightly larger or equal to ui . The agents are
scheduled to communicate on a random basis by scheduling random pairs for each timestep
of the simulation. During the interaction between individual i and individual j , the
following rules are applied:

opinion dynammics model                     --> manifestation in change in a word cloud
If |xi - xj | < ui dxi = _mu * (xj ? xi ) --> change word cloud to be more like xj
If |xi - xj | > ti dxi = _mu * (xi ? xj ) --> change word cloud to be more different than xj
#where |xi ? xj | ==> 1 - jaccardIndex(xi.wordcloud ,xj.wordcloud)

latitude_of_acceptance   #a threshold determining the latitude of acceptance ui 
latitude_of_rejection      #threshold determining the latitude of rejection ti
# ti > ui
# latitude_of_rejection > latitude_of_acceptance

an agent having a high ego-involvement can be formalized as an agent where latitude_of_acceptance is slightly larger or equal to latitude_of_rejection

The opinions are drawn from a uniform distribution between [?1;1].
Vary U and T between 0.1 and the maximum of 2.0


We suspect that adding a network aspect to the model will increase or expedite network polarization?


"""
class Agent(object) :
    def __init__(self,uid=None,lex=None,lattitude_of_acceptance=0.0, lattitude_of_rejection=0.0,opinion_skew=0.0) :
        self._uid=uid
        self.lattitude_of_acceptance=lattitude_of_acceptance
        self.lattitude_of_rejection=lattitude_of_rejection
        self.lexicon=lex
        if opinion_skew != 0.0 :
            self._thought_vector=lex.get_skewed_opinion(opinion_skew,lex.cloudsize)
        else :
            self._thought_vector=lex.get_random_opinion(lex.cloudsize)

        self.__socialNetwork = [] # This is a list of IDs of other agents
        
    def set_opinion_vector(self,thought_vector={}) :
        """takes dict arg - this agent's thought vector"""
    
    def get_thought_vector(self) :
        return self._thought_vector
    
    def listen_to_schpeal(self,other_agent=None) :
        """
        calculate distance between my opinion and the talker's opinion
        if acceptable - then by increment the frequency of a common term and decrement the frequency of a difference term
        if rejectable - then decrement frequency of a common term and increment the frequency of a term in the difference
        (MAYBE a strategy object?)
        
        note the 'private' methods below to add or remove a word from the word cloud
        
        """
        
        
    def change_opinion(self,other_agent=None,direction=0.0) :
        """TODO inspect another agent's thoughts and change in the direction indicated """
        
    def _remove_word(self,term=None) :
        self._thought_vector[term]-=1
        lex.remove_from_idf(term)
        
    def _add_word(self,term=None) :
        if term not in self._thought_vector : self._thought_vector[term]=0
        self._thought_vector[term]+=1
        lex.add_to_idf(term)

    def getUID(self):
        return self._uid

    def addNetworkMember(self,AgentID):
        # Adds an agent (by ID) to another agent's social network
        self.__socialNetwork.append(AgentID)

    def getSocialNetwork(self):
        # Return the agent's social network
        return self.__socialNetwork

    def clearSocialNetwork(self):
        # Empty the social network
        self.__socialNetwork = []

class UID :
    def __init__(self) :
        self._uid=0
    def nextId(self) :
        nextId=self._uid
        self._uid+=1
        return nextId
#TODO TEST
class PolarityInitializationStrategy(object) :
    """methods to determine mix of opinion polarity
       polarity is a value, that when interpreted by the Lexicon in get_skewed_opinion, results in a word cloud with a cooresponding leaning
       the probability of a polarity 1 word is the area below the skew value in [0,skew)
       the probability of a polarity 2 word is the area at and above the skew value in [skew,1]
       
       the polarity initialization strategy determines the distribution of polarities with which to initialize agents with
       a setting of 0.5 results in an equal chance for either a polarity 1 or polarity 2 value being fed to the Agent constructor as skew
    """
    def __init__(self,pct_high=.5) :
        self.pct_high = pct_high
        
    def get_skew(self) :
        if random.random() < self.pct_high :
            return random.random()*.5 + .5  #return a skew towards polarity 2
        else :
            return random.random()*.5  #a skew towards polarity 1
#TODO TEST    
class EgoInvolvementInitializationStrategy(object) :
    """the ego involvement strategy determines how we will assign values to lattitude_of_acceptance and lattitude of rejection for agents at construction time"""
    def __init__(self,randomize=False,lattitude_of_acceptance_max=0.0,ego_involvement_max=0.0) :
        self.randomize=randomize
        self.lattitude_of_acceptance_max=lattitude_of_acceptance_max   #max value for lattitude_of_acceptance
        self.ego_involvement_max=min(ego_involvement_max,1-self.lattitude_of_acceptance_max)   #[0,1] for max distance between- a small value here generates high ego-involvement / reluctance to open-mindedness
        
    def get_lattitudes(self) :
        if self.randomize :
            laccept = random.random()*self.lattitude_of_acceptance_max
            lreject = laccept + random.random() * self.ego_involvement_max
            return laccept,lreject
        else :
            return self.lattitude_of_acceptance_max, (self.ego_involvement_max + self.lattitude_of_acceptance_max)

#TODO TEST
class AgentBuilder(object) :
    
    """
    john g - test the  
    """
    
    def __init__(self,polarity_strategy=None,ego_involvement_strategy=None,lexicon_size=20,agent_vector_size=20) :
        self.uidgen=UID()
        self.strategy=polarity_strategy
        self.ego_involvement_strategy=ego_involvement_strategy
        self.lex=Lexicon.Lexicon(lexicon_size,agent_vector_size)
        self.__numAgents = 0
        self.__networkType = "" # Valid types are: ErdosRenyi, Lattice, and RealWorld - all other values are treated as no-network requested
        
    # Methods to set and get the number of agents being used by the AgentBuilder object
    def setNumAgents(self,n):
        self.__numAgents = n

    def getNumAgents(self):
        return self.__numAgents

    def setNetworkType(self,networkType):
        self.__networkType = networkType

    def getNetworkType(self):
        return self.__networkType

    # This method creates a new set of 'n' agents with a network of type netType
    # Valid values for netType are listed above next to __networkType attribute
    # All invalid netType values are treated as no-network
    def createAgents(self,n,netType = "") :
        agents=[]

        # Set the number of agents
        self.setNumAgents(n)

        # Set the networkType
        self.setNetworkType(netType)
        
        for i in range(0,self.getNumAgents()) :
            #def __init__(self,uid=None,lex=None,lattitude_of_acceptance=0.0, lattitude_of_rejection=0.0,opinion_skew=0.0) :
            EIIS = EgoInvolvementInitializationStrategy(True,0.7,0.3)
            lattitudes=EIIS.get_lattitudes()
            PS = PolarityInitializationStrategy()
            a=Agent(self.uidgen.nextId(),lex=self.lex,lattitude_of_acceptance=lattitudes[0], lattitude_of_rejection=lattitudes[1], opinion_skew=PS.get_skew())
            agents.append(a)

        # Create the social network
        if self.getNetworkType() == "ErdosRenyi":
            self.createErdosRenyiSocialNetwork(agents)
        elif self.getNetworkType() == "Lattice":
            self.createLatticeSocialNetwork(agents)
        elif self.getNetworkType() == "RealWorld":
            self.createRealWorldNetwork(agents)
        

        return agents
        
    def createErdosRenyiSocialNetwork(self,agents):
        # This method creates the social network between the agents
        # This method uses the Erdos-Renyi method of creating the social network

        # Clear out any existing social networks
        self.clearSocialNetworks(agents)

        # Define the probability that two agents will be in the network together
        socialNetworkProbability = 0.01

        # Pair every set of agents, select a random value, and if the random value is < the socialNetworkProbability, then add the agents to each others' social network
        for i in range(self.getNumAgents()):
            for j in range(i+1,self.getNumAgents()):
                # Using the socialNetworkProbability property of the model, connect the agents to each other
                if random.random() < socialNetworkProbability:
                    agents[i].addNetworkMember(j)
                    agents[j].addNetworkMember(i)

    def createLatticeSocialNetwork(self,agents):
        # This method creates a lattice social network between the agents
        
        # Clear out any existing social networks
        self.clearSocialNetworks(agents)

        # Define the number of agents to partner with the current one
        # Since this is a lattice, they will be paired 1/2 below and 1/2 above the current value
        numPartners = 10 #NOTE: MUST BE AN EVEN VALUE

        # Go through the complete list of agents and define their agent lists
        for i in range(self.getNumAgents()):
            # First look at the middle agents and assign their network to be the 5 agents to their left and right
            if (i > (numPartners/2)-1) and (i < (self.getNumAgents()-(numPartners/2))):
                for j in range((numPartners/2)+1,1,-1):
                    agents[i].addNetworkMember(i+1-j)
                for j in range(1,(numPartners/2)+1):
                    agents[i].addNetworkMember(i+j)
            # If the agent is one of the first 5, then their lowest agents will be from the highest on the list (the network is circular)
            elif (i <= (numPartners/2)-1):
                for j in range((numPartners/2),i,-1): # Compute values below 0
                    agents[i].addNetworkMember(self.getNumAgents()+i-j)
                for j in range(i,0,-1): # Compute values between 0 and the current value (i)
                    agents[i].addNetworkMember(i-j)
                for j in range(0,(numPartners/2)): # Add the values above the current value (i)
                    agents[i].addNetworkMember(i+1+j)
            # If the agent is one of the last (numPartners/2), then their highest agents will be from the lowest on the list (the network is circular)
            elif (i >= (self.getNumAgents()-(numPartners/2))):
                for j in range((numPartners/2),0,-1): # Add the values below the current value (i)
                    agents[i].addNetworkMember(i-j)
                for j in range(i,self.getNumAgents()-1): # Add the values above the current value (i), but below 1000
                    agents[i].addNetworkMember(j+1)
                for j in range(self.getNumAgents()-(numPartners/2)-1,i): # Add the values starting from 0
                    agents[i].addNetworkMember(j - (self.getNumAgents() - 1) + (numPartners/2))

    def createRealWorldNetwork(self,agents):
        # This method creates a Lattice Network and then converts that network to real world by replacing a specific percentage of the links to random
        self.createLatticeSocialNetwork(agents)

        # Define the probability for rewiring the network 
        rewireProbability = 0.1

        # Go through all of the agents, unwire their network, and then rewire it based on rewireProbability
        for i in range(self.getNumAgents()):
            # Make a copy of the agent's current network
            CrntNetwork = list(agents[i].getSocialNetwork())

            # Clear the agent's existing network
            agents[i].clearSocialNetwork()

            # Go through the old network and re-add each agent unless a random number is less than the rewire probability
            for j in CrntNetwork:
                if random.random() < rewireProbability:
                    # Pick a random agent to add to the network instead
                    agents[i].addNetworkMember(random.randint(0,self.getNumAgents()-1))
                else:
                    # Add back the original agent
                    agents[i].addNetworkMember(j)

    def clearSocialNetworks(self,agents):
        # This method clears the social network for each agent
        for i in range(self.getNumAgents()):
            agents[i].clearSocialNetwork()    
        
######################### EXECUTION CODE #########################

# Create an AgentBuilder object
AB = AgentBuilder()

# Request agents from AB. The createAgents methods expects to see a number of agents and a type of Network to create.
theAgents = AB.createAgents(50,"ErdosRenyi")

# Print out the agents to see what is going on with them
for i in theAgents:
    print "Agent " +str(i.getUID()) + " has a lattitude_of_acceptance of " + str(i.lattitude_of_acceptance) + ", a lattitude_of_rejection of " + str(i.lattitude_of_rejection) + ", a get_thought_vector of " + str(i.get_thought_vector()) + ", and a getSocialNetwork of " + str(i.getSocialNetwork())
