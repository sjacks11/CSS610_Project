import nltk
import networkx
import re
import string

class LangBuilder :
    def __init__(self,fname=None) :
        self.index_dict={}
        self.ungram_freq={}
        self.bigram_freq={}
        self.trigram_freq={}
        
        self.trigram_matrix=[]
        self.bigram_matrix=[]
        self.init_term_index() 

    def add_document(self,fname='') :
        fin=open(fname,'rbU')
        text = fin.read().lower()
        fin.close()
        
               
        self.sentences=self.get_sentences(text)
        for sentence in self.sentences : self.proc_ngrams(sentence)
        self.init_ngram_matrix()
        self.assign_ngram_probabilities()


    """initializes the term index"""
    def init_term_index(self):
        self.index_dict["<s>"]=0
        self.index_dict["</s>"]=1
        print str(self.index_dict)
    
    """creates an empty nXnXn matrix where is the number of unique terms in the corpus"""
    def init_ngram_matrix(self) :
        for i in range(0,len(self.index_dict)) :
            self.trigram_matrix.append([])
            self.bigram_matrix.append([])
            for j in range(0,len(self.index_dict)) :
                self.trigram_matrix[i].append([])
                self.bigram_matrix[i].append(0)
                for k in range(0,len(self.index_dict)) :
                    self.trigram_matrix[i][j].append(0)

    def proc_ngrams(self,sentence='') :
        """returns ungram frequency dict"""
        tokenized_sentence = tokenize_sentence(sentence)
        self.proc_ungrams(tokenized_sentence)
        self.proc_ngt1_grams(tokenized_sentence)

    """inserts a term into the index dictionary (index_dict) and to the ungram frequency dictionary"""
    def proc_ungrams(self,tokenized_sentence=[]) :
        for term in tokenized_sentence :
            #print term
            if term not in self.index_dict and term != '':
                indsz=len(self.index_dict)
                self.index_dict[term]=(indsz+1)
            if term not in self.ungram_freq: self.ungram_freq[term]=0
            self.ungram_freq[term]+=1

    """"""    
    def proc_ngt1_grams(self,tokenized_sentence=[]) :
        """returns bigram frequency dict"""
        for i in range(1, len(tokenized_sentence)) :
            bigram=''
            trigram=''
            bigram=tokenized_sentence[i-1] + ' ' + tokenized_sentence[i]
            if bigram not in self.bigram_freq : self.bigram_freq[bigram]=0
            self.bigram_freq[bigram]+=1
            if i > 1 :
                trigram=tokenized_sentence[i-2] + ' ' + bigram
                if trigram not in self.trigram_freq : self.trigram_freq[trigram]=0
                self.trigram_freq[trigram]+=1
        

    def assign_ngram_probabilities(self) :
        """"""
        for bigram in self.bigram_freq :
            freq=self.bigram_freq[bigram]
            i,j=self.bigram_indices (bigram)
            print str(i) + ' ' + str(j)
            self.bigram_matrix[i][j]=freq
            
        for trigram in self.trigram_freq :
            freq = self.trigram_freq[trigram]
            i,j,k=self.trigram_indices(trigram)
            self.trigram_matrix[j][j][k] = freq
        print     str(trigram_matrix)
            
    
    """"""    
    def bigram_indices(self,bigram='') :
        print bigram
        v1=''
        v2=''
        if bigram.find("<s>") >= 0 : 
            v1= "<s>"
            bigram=bigram.replace("<s>","")
            v2 = re.split("[\W\s]+",bigram.strip())[0]
        elif bigram.find("</s>") >= 0 :
            bigram=bigram.replace("</s>","")
            v1 = re.split("[\W\s]+",bigram.strip())[0]
            v2 = "</s>"
        else :
            lst=re.split("[\W\s]+",bigram)
            v1=lst[0]
            v2=lst[1]
        print v1 + ' ' + v2
        i1=self.index_dict[v1]
        i2=self.index_dict[v2]
        return i1,i2

    def trigram_indices(self,trigram='') :
        v1=''
        v2=''
        v3=''
        if trigram.find("<s>") >= 0 : 
            v1= "<s>"
            trigram=trigram.replace("<s>","")
            lst=re.split("[\W\s]+",trigram)
            v2=lst[0]
            v3=lst[1]
            
        elif trigram.find("</s>") >= 0 :
            
            trigram=trigram.replace("</s>","")
            lst=re.split("[\W\s]+",trigram)
            v1=lst[0]
            v2=lst[1]
            v3 = "</s>"
        else :
            lst=re.split("[\W\s]+",trigram)
            v1=lst[0]
            v2=lst[1]
            v3=lst[2]
            
        return self.index_dict[v1],self.index_dict[v2],self.index_dict[v3]

    """tokenizes a body of text into discrete sentences"""
    def get_sentences(self,text=None) :
        return nltk.sent_tokenize(text)
    
"""tokenizes a string representing a sentence and returns a list of the sequential tokens wrapped in sentence start/end tags"""
def tokenize_sentence(sentence='') :
    
    retval=["<s>"]
    tokens=[x for x in re.split("[^A-Za-z]+",sentence) if len(x) >0]
    print str(tokens)
    
    tokens=retval.extend(tokens)
    
    retval.append("</s>")
    return retval

"""    
def tokenize_sentences(sentences=[]) :
    tokenized_sentences = []
    for sentence in sentences :
        tokenized_sentences.append(tokenize_sentence(sentence))
        return tokenized_sentences
"""