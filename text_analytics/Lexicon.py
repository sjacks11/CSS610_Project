import random
import math
import Opinion
import csv

class SemanticClass(object) :
	"""terms definining a point of view"""
	def __init__(self) :
		self.terms = []
		
	def add_term(self,term='') :
		self.terms.append(term)
		
class Lexicon(object) :
	"""object to encapsulate POVs"""
	def __init__(self,cloudsize=20,vector_size=20) :
		self.cloudsize=cloudsize
		self._lexi={}

		#self._lexi['republican']=["constutionality", "cuttaxes", "secondamendment", "freeenterprise", "smallgovernment", "religiousfreedom", "drillherenow", "domesticoil", "overturnroevswade", "prochoice" , 'rep1' ,'rep2' ,'rep3']
		#self._lexi['democrat']=["taxthewealthy", "equalrights", "economicequality", "closeguantanamo", "epa", "nodrillinginwildlife", "alternativeenergy", "repealDNDT" ,'dem1','dem2','dem3','dem4']
		#self._lexi['middle']=['energyindepdendence', 'jobs', 'economicgrowth', 'smallbusiness', 'education', 'middle1' ,'middle2' ,'middle3', 'middle4', 'middle5']
		
		width=2.0/cloudsize/2
		
		self.inter_document_frequency={}
		
		#{category : {token : value}}
		self._lexi['republican']={}  	#pertains to [skew,1] continuum
		self._lexi['democrat']={}	#pertains to [0,skew] continuum
		for i in range(0,cloudsize+1) :
			r1=('r' + str(i))
			d1=('d' + str(i))
			self._lexi['republican'][r1]= (-width)
			self._lexi['democrat'][('d' + str(i))]= (+width)
			self.inter_document_frequency[r1]=0.0
			self.inter_document_frequency[d1]=0.0
		
		self._lexi_lookup={}
		self._randomorder=[]
		#reverse lookup
		# {term : category}
		for key in self._lexi :
			for value in self._lexi[key] :
				self._lexi_lookup[value]=key
				self._randomorder.append(value)
		self.shuffle_lexicon()
	
	def get_idf_vector(self) : return self.inter_document_frequency
	def clear_idf_vector(self) : self.inter_document_frequency = {}
	
	
	def remove_from_idf(self,term=None) :
		self.inter_document_frequency[term]-=1
	
	def add_to_idf(self,term=None) :
		self.inter_document_frequency[term]+=1
		
	def cosine_distance(self,vector1={},vector2={}) :
		"""
			Determine the cosine distance between two term-term_frequency vectors
				cosine_distance(dict,dict) --> float in [0,1]
				
				Keyword arguments:
				vector1 , vector2 - dict object containing kv pairs of the form {term : term_frequency}
		"""
		tf_idf_1={}
		tf_idf_2={}
		#calculate term frequencies for each document
		for t in vector1 :
			if t not in tf_idf_1 : tf_idf_1[t]=0
			tf_idf_1[t]+=1
		for t in vector2 :
			if t not in tf_idf_2 : tf_idf_2[t]=0
			tf_idf_2[t]+=1
		#calculate tf_idf vector values for each document
		for t in tf_idf_1 :
			if self.inter_document_frequency[t]==0.0 :
				tf_idf_1[t]= 0.0
			else :
				tf_idf_1[t]/self.inter_document_frequency[t]
				
		for t in tf_idf_2 :
			if self.inter_document_frequency[t]==0.0 :
				tf_idf_2[t]= 0.0
			else :
				tf_idf_2[t]/self.inter_document_frequency[t]
		ks1=set(tf_idf_1.keys())
		ks2=set(tf_idf_2.keys())
		#print str(sorted(ks1))
		#print str(sorted(ks2))
		keyset=ks1.intersection(ks2)
		#print str(keyset)
		#print 'intersection ' + str(len(keyset))
		#print 'union ' + str(len((set(tf_idf_1.keys()).union(set(tf_idf_2.keys())))))
		
		dp=0.0
		m1=0.0
		m2=0.0
		ci=0
		for k in keyset :
			#print str(k)
			dp+=(tf_idf_2[k]*tf_idf_1[k])
			ci+=1
		#print str(len(keyset)) + ' items in common, len of .product: ' + str(ci)
		ci=0
		for t in tf_idf_1 :
			m1+=math.pow(tf_idf_1[t],2.0)
			ci+=1
		#print 'len of m1: ' + str(ci) + str(sorted(list(tf_idf_1.values())))
		ci=0
		for t in tf_idf_2 :
			m2+=math.pow(tf_idf_2[t],2.0)
			ci+=1
		#print 'len of m2: ' + str(ci)
		
		#print 'dotprod=' + str(dp) + ' ' +  'm1=' + ' ' + str(m1) + ' ' +  'm2=' + str(m2)

		return (dp / (math.sqrt(m1) * math.sqrt(m2)))

	def jaccard_distance(self,vector1=[],vector2=[]) :
		"""calculates distance between vectors based on intersection and union sizes"""
		s1=set(vector1)
		s2=set(vector2)
		intersect=s1.intersection(s2) 
		union=s1.union(s2)
		return 1.0-(1.0*len(intersect)/len(union)*1.0)


	def politicalization_matrix(self,vector={}) :
		rep=0
		dem=0
		mid=0
		for v in vector :
			if self._lexi_lookup[vector[v]] == "republican" : rep+=1
			if self._lexi_lookup[vector[v]] == "democrat" : dem+=1
			if self._lexi_lookup[vector[v]] == "middle" : mid+=1
		return rep,dem,mid
	
	def shuffle_lexicon(self) :
		random.shuffle(self._randomorder)
		
	def get_skewed_opinion(self,skew=0.0,sz=20) :
		kr=list(self._lexi['republican'].keys())	#pertains to [skew,1] continuum
		ka=list(self._lexi['democrat'].keys())	        #pertains to [0,skew] continuum
		random.shuffle(kr)
		random.shuffle(ka)
		term_vector={}
		for i in range(0,sz) :
			t=''
			if random.random() >= skew :
				j=random.randint(0,len(kr)-1)
				t=kr[j]
			else :
				j=random.randint(0,len(ka)-1)
				t=ka[j]
			if t not in term_vector : term_vector[t]=0.0
			term_vector[t]+=1
			self.inter_document_frequency[t]+=1
		return term_vector 		
		
	def get_random_opinion(self, wordcount=20) :
		"""
		get_random_opinion(int) --> dict
		"""
		self.shuffle_lexicon()
		output={}
		for i in range(0,wordcount+1) :
			rint=random.randint(0,len(self._randomorder)-1)
			print str(rint) + ' ' + str(len(self._randomorder))
			t = self._randomorder[rint]    #don't care about duplicates
			if t not in output : output[t]=0.0
			output[t]+=1
			self.inter_document_frequency[t]+=1
		return output

	def get_numeric_position(self,wordcloud=[]) :
		position=0.0
		cat_neg='republican'
		nr_neg=0
		cat_pos='democrat'
		nr_pos=0
		for w in wordcloud :
			category=self._lexi_lookup[w]
			if category == 'republican' :
				nr_neg+=1
			else :
				nr_pos+=1
		position = 1.0*nr_neg / (nr_neg+nr_pos)
		return position

def write_vector(vector={},outputfilename=None,outputfile=None) :
	if outputfilename == None and outputfile == None : return
	fout=None
	if outputfilename != None :
		fout=open(outputfilename,'a')
		print 'opening new file in append mode'
	if outputfile != None :
		fout=outputfile
		print 'using given output file'
	writer=csv.writer(fout)
	for t in vector : 
		writer.writerow([t,vector[t]])

	if outputfilename != None : fout.close()

def test01() :
	L = Lexicon(40)
	opinions=[]
	for i in range(0,20)  : opinions.append(L.get_random_opinion(10))
	idf=L.get_idf_vector()
	fout=open('/Users/johngugliotti/Dev/pydev/text_analytics/test01','wb')
	write_vector(idf,outputfile=fout)
	write_vector({'--':'--'},outputfile=fout)
	write_vector(opinions[2],outputfile=fout)
	a=list(sorted(opinions[2].keys()))
	b=list(sorted(opinions[1].keys()))
	print str(a)
	print str(b)
	print str(L.cosine_distance(opinions[1],opinions[2]))
	
	
	write_vector({'--':'--'},outputfile=fout)
	write_vector(opinions[1],outputfile=fout)
	write_vector({'--':'--'},outputfile=fout)
	write_vector({'o1-->o2': L.cosine_distance(opinions[1],opinions[2])},outputfile=fout)
	fout.close()
	
	for i in range(0,len(opinions)-1) :
		for j in range(i+1,len(opinions)-1) :
			print str(i) + ' ' + str(j) + ':  ' + str(L.cosine_distance(opinions[i],opinions[j]))
	
	
	