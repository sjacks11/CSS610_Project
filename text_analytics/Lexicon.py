import random

class SemanticClass(object) :
	"""terms definining a point of view"""
	def __init__(self) :
		self.terms = []
		
	def add_term(self,term='') :
		self.terms.append(term)
		
class Lexicon(object) :
	"""object to encapsulate POVs"""
	def __init__(self) :
		self._lexi={}
		self._lexi['republican']=["constutionality", "cuttaxes", "secondamendment", "freeenterprise", "smallgovernment", "religiousfreedom", "drillherenow", "oil", "overturnroevswade", "prochoice" , 'rep1' ,'rep2' ,'rep3']
		self._lexi['democrat']=["taxthewealthy", "equalrights", "economicequality", "closeguantanamo", "epa", "nodrillinginwildlife", "alternativeenergy", "repealDNDT" ,'dem1','dem2','dem3','dem4']
		self._lexi['middle']=['energyindepdendence', 'jobs', 'economicgrowth', 'smallbusiness', 'education', 'middle1' ,'middle2' ,'middle3', 'middle4', 'middle5']
		
		self._lexi_lookup={}
		self._randomorder=[]
		for key in self._lexi :
			for value in self._lexi[key] :
				self._lexi_lookup[value]=key
				self._randomorder.append(value)
		self.shuffle_lexicon()	
		
	def politicalization_matrix(self,vector=[]) :
		rep=0
		dem=0
		mid=0
		for v in vector :
			if self._lexi_lookup[v] == "republican" : rep+=1
			if self._lexi_lookup[v] == "democrat" : dem+=1
			if self._lexi_lookup[v] == "middle" : mid+=1
			
		return rep,dem,mid
	
	def numericalize_opinion(self,vector=[]) :
		rep,dem,mid=self.politicalization_matrix(vector)
		#print str((rep,dem,mid))
		ttl=1.0*rep+dem
		m = 1.5 if mid == 0 else 1.0 / mid
		
		s_rep=0 if ttl==0 else rep/ttl
		
		s_dem= 0 if ttl == 0 else dem/ttl
		#print str((s_rep,s_dem,m))
		return (m-(s_rep-s_dem)) if s_rep > s_dem else (m + (s_dem-s_rep))
		
	
	def shuffle_lexicon(self) :
		random.shuffle(self._randomorder)
		
	def get_random_opinion(self, wordcount=0) :
		self.shuffle_lexicon()
		output=[]
		output.extend(self._randomorder[0:wordcount-1])
		return output
	
	
		
		