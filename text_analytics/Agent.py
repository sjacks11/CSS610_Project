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
of the simulation. During the interaction between individual iand individual j , the
following rules are applied:

opinion dynammics model                     --> manifestation in change in a word cloud
If |xi - x j | < ui dxi = _mu * (x j ? xi ) --> change word cloud to be more like xj
If |xi - x j | > ti dxi = _mu * (xi ? x j ) --> change word cloud to be more different than xj
#where |xi ? x j | ==> 1 - jaccardIndex(xi.wordcloud ,x j.wordcloud)

latitude_of_acceptance   #a threshold determining the latitude of acceptance ui 
latitude_of_rejection      #threshold determining the latitude of rejection ti
# ti > ui
# latitude_of_rejection > latitude_of_acceptance

an agent having a high ego-involvement can be formalized as an agent where latitude_of_acceptance is slightly larger or equal to latitude_of_rejection

The opinions are drawn from a uniform distribution between [?1;1].
Vary U and T between 0.1 and the maximum of 2.0

"""
class Agent(object) :
    def __init__(self,uid=None,lex=None,lattitude_of_acceptance=0.0, lattitude_of_rejection=0.0,opinion_skew=0.0) :
        self._uid=uid
        
        self.lattitude_of_acceptance=lattitude_of_acceptance
        self.lattitude_of_rejection=lattitude_of_rejection
        self.lexicon=lex
        if opinion_skew != 0.0 :
            self._thought_vector=lex.get_skewed_opinion(skew=skew,sz=lex.vector_size)
        else :
            self._thought_vector=lex.get_random_opinion(sz=lex.vector_size)
        
    def set_opinion_vector(self,thought_vector={}) :
        """takes dict arg - this agent's thought vector"""
    
    def get_thought_vector(self) :
        return self._thought_vector
        
    def change_opinion(self,other_agent=None,direction=0.0) :
        """TODO inspect another agent's thoughts and change in the direction indicated """
        
    def _remove_word(self,term=None) :
        self._thought_vector[term]-=1
        lex.remove_from_idf(term)
        
    def _add_word(self,term=None) :
        if term not in self._thought_vector : self._thought_vector[term]=0
        self._thought_vector[term]+=1
        lex.add_to_idf(term)

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
            return random.random*.5 + .5  #return a skew towards polarity 2
        else :
            return random.random*.5  #a skew towards polarity 1
#TODO TEST    
class EgoInvolvementInitializationStrategy(object) :
    """the ego involvement strategy determines how we will assign values to lattitude_of_acceptance and lattitude of rejection for agents at construction time"""
    def __init__(self,randomize=False,lattitude_of_acceptance_max=0.0,ego_involvement_max=0.0) :
        self.randomize=randomize
        self.lattitude_of_acceptance_max=lattitude_of_acceptance_max   #max value for lattitude_of_acceptance
        self.ego_involvement_max=math.min(ego_involvement_max,1-self.lattitude_of_acceptance_max)   #[0,1] for max distance between- a small value here generates high ego-involvement / reluctance to open-mindedness
        
    def get_lattitudes(self) :
        if self.randomize :
            laccept = random.random()*self.lattitude_of_acceptance_max
            lreject = laccept + random.random() * self.ego_involvement_max
            return laccept,lreject
        else :
            return self.lattitude_of_acceptance_max, (self.ego_involvement_max + self.lattitude_of_acceptance_max)

#TODO TEST
class AgentBuilder(object) :
    
    def __init__(self,polarity_strategy=None,ego_involvement_strategy=None,lexicon_size=20,agent_vector_size=20) :
        self.uidgen=UID()
        self.strategy=polarity_strategy
        self.ego_involvement_strategy=ego_involvement_strategy
        self.lex=Lexicon(lexicon_size,agent_vector_size)
        
    #TODO finish construction of the population - enter hooks to place the agents on a graph
    def get_N_Agents(self,n) :
        agents=[]
        for i in range(0,n+1) :
            #def __init__(self,uid=None,lex=None,lattitude_of_acceptance=0.0, lattitude_of_rejection=0.0,opinion_skew=0.0) :
            lattitudes=ego_involvement_strategy.get_lattitudes()
            a=Agent(self.uidgen.nextId(),lex=self.lex,lattitude_of_acceptance=lattitudes[0], lattitude_of_rejection=lattitudes[1], opinion_skew=polarity_strategy.get_skew())
            agents.append(a)
        return agents
        
    
        
        
    
        
        
        

            
        
        
    