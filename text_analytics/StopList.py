import PorterStemmer as stemmer
import string

separators=(string.whitespace + string.punctuation).replace("'","").replace("`","")

class StopList :
        
        def __init__(self,path=None,fn=None) :
                fin=open(path+fn,'rbU')
                self.stopwords=set()
                for f in fin :
                        token=filter(lambda x : x in string.ascii_letters, f)
                        stemmed_token=stemmer.stem(token,0,len(token)-1)
                        self.stopwords.add(token)
                        self.stopwords.add(stemmed_token)

        def stopword_count(self) : return len(self.stopwords)
        
        def stopwords_list(self) : return self.stopwords
        
        def is_stopword(self,txt=None) :
                token=filter(lambda x : x in string.ascii_letters, txt).lower()
                ##token=stemmer.stem(token)
                return token in self.stopwords

        def tokenize(self,txt) :
                tokens=[printable (t) for t in txt.split()]
                return [filt(t).lower() for t in tokens]
                
        def stem_tokens(self,txt) :
                return [stemmer.stem(x,0,len(x)-1) for x in self.tokenize(txt)]

        def remove_stopwords(self,tokens=[]) :
                for t in tokens :
                        if self.is_stopword(t) : tokens.remove(t)
                return tokens

        def vectorize(self,txt,stoplist=True) :
                if stoplist :
                        return self.remove_stopwords(self.stem_tokens(txt))
                else :
                        return self.stem_tokens(txt)

                       
                
def filt(t) : return filter(lambda x : x not in separators, t)
def printable(t) : return filter(lambda x : x in string.printable,t)





        



