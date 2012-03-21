import StopList as SL
import math

class AgentIndex :

    def __init__(self,stoplist_path=None,stoplist_file=None) :
        self.iindex={}
        self.idf={}
        self.docrefs={}
        self.sl=None
        if (stoplist_path and stoplist_file ) : self.sl=SL.StopList(stoplist_path,stoplist_file)

    def add_doc(self,docref={}) :
        
        for token in docref['vector'] :
           
            if token not in  self.iindex :
                self.iindex[token]={}
                self.idf[token]=0
            self.idf[token]+=1
            if docref['docid'] not in self.iindex[token] :
                self.iindex[token][docref['docid']]=0
            self.iindex[token][docref['docid']]+=1

    def add_doc_vector(self,docref={}) :
        for token in docref['vector'] :
            if token not in  self.iindex :
                self.iindex[token]={}
                self.idf[token]=0
            self.idf[token]+=1
            if docref['docid'] not in self.iindex[token] :
                self.iindex[token][docref['docid']]=0
            self.iindex[token][docref['docid']]+=1        

    def add_keyed_doc_vectors(self,docrefset={}) :

        for dr in docrefset :
            #print str(dr)
            k = dr.keys()[0]
            self.docrefs[k]=dr[k]
            docref=dr[k]
            for token in docref['vector'] :
                if token not in  self.iindex :
                    self.iindex[token]={}
                    self.idf[token]=0
                self.idf[token]+=1
                if docref['docid'] not in self.iindex[token] :
                    self.iindex[token][docref['docid']]=0
                self.iindex[token][docref['docid']]+=1
            
    def update_idf(self) :
        self.idf={}
        for token in self.iindex :
            for docid in self.iindex[token] :
                self.idf[token]+=1

    def doc_sim_keyed(self,dr_1=None,dr_2=None) :
        v1={}
        v2={}

        s1=set(dr_1['vector'])
        s2=set(dr_2['vector'])
        #print 's2 len : ' + str(len(s2))
        #print 's1 len : ' + str(len(s1))
        
        for t in s1 :
            
            v1[t]=(float(self.iindex[t][dd1['docid']])/float(self.idf[t]))
        for t in s2 :
            
            v2[t]=(float(self.iindex[t][dd2['docid']])/float(self.idf[t]))
        dot_prod=float(0.0)
        for t in s1.intersection(s2) :
            dot_prod+=v1[t]*v2[t]
        m1=magnitude(v1)
        m2=magnitude(v2)

        #print str(dot_prod) + " / ( " + str(m1) + " * " + str(m2)
        
        return (dot_prod) / (m1*m2)
    
    def doc_sim(self,dr_1=None,dr_2=None) :
        v1={}
        v2={}
        s1=set(dr_1['vector'])
        s2=set(dr_2['vector'])
        #print 's2 len : ' + str(len(s2))
        #print 's1 len : ' + str(len(s1))
        
        for t in s1 :
            print t
            v1[t]=(float(self.iindex[t][dr_1['docid']])/float(self.idf[t]))
        for t in s2 :
            print t
            v2[t]=(float(self.iindex[t][dr_2['docid']])/float(self.idf[t]))
        dot_prod=float(0.0)
        for t in s1.intersection(s2) :
            dot_prod+=v1[t]*v2[t]
        m1=magnitude(v1)
        m2=magnitude(v2)

        #print str(dot_prod) + " / ( " + str(m1) + " * " + str(m2)
        
        return (dot_prod) / (m1*m2)
        
    def get_index(self) : return self.iindex

    def get_idf(self) : return self.idf

    def get_docrefs(self) : return self.docrefs

    def get_vectorized_doc_ref(self,txt=None,docid=None,author=None,timestamp=None) :
	docref= { }
	if docid : docref['docid'] = docid
	docref['vector'] = vectorize(txt)
	docref['author']=author
	return docref

    def get_keyed_vectorized_doc_ref(self,txt=None,docid=None,author=None,timestamp=None) :
	docref= { }
	if docid : docref['docid'] = docid
	docref['vector'] = self.sl.vectorize(txt)
	docref['author']=author
	return { docid : docref }

    def get_sim_function(self) :
        return doc_sim
    
    def get_k_random_docrefs(self,k=2) :
        keyset=set(self.docrefs.keys())
        docrefs={}
        for i in range(0,k) :
            nk=keyset.pop()
            docrefs[nk] = self.docrefs[nk]
        return docrefs
    
    def get_clusters(centroids=[],corpus=[]) :
        clusters={}
        changed=False

        for dr in corpus :

            max_sim=float(-1.0)
            cluster_assn=-1
            centroid_index=0

            for centroid in centroids :
                sim=self.doc_sim(dr,centroid)
                if sim > max_sim :
                    max_sim=sim
                    cluster_assn=centroid_index
                centroid_index+=1
                
            if not changed and not (dr['cluster'] == cluster_assn) :
                changed=True
            dr['cluster']=cluster_assn

            if not cluster_assn in clusters : clusters[cluster_assn]=[]
            clusters[cluster_assn].append(dr)

        return clusters,changed

def magnitude(vector={}) :
    m=float(0.0)
    for v in vector :
        m+=math.pow(float(vector[v]),2.0)
    return math.sqrt(m)
    
def vectorize(txt=None) :
    return txt.split()

    
