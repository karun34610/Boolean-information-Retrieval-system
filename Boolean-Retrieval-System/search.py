import argparse
import timeit
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from ir_system import IRSystem

# docs = ['hello i m a machine learning engineer', 
#         'hello bad world machine engineering people', 
#         'the world is a bad place',
#         'engineering a great machine that learns',"world is so great",'','']
docs=[]
for i in range(1,50):
    docs.append(' ')

#these are just a list of preliminary stop words listed by us but all the other stop words are take care using nltk library
stop_words = ['is', 'a', 'for', 'the', 'of','this','was','it','that','.',',',';',':','-','_']


documentID = 0
path = r"C:\Users\Rohan\OneDrive\Desktop\ir\Wildcard-Query-Search-Engine\proj\data1"

ps = PorterStemmer()
tokens={}
filename={}
for root, dirs, files in os.walk(path):
    for file in files:
        filename[documentID+1]=file
        with open(os.path.join(path, file), encoding="utf-8",errors="ignore") as f:
                documentID += 1
                line_tokens = []
                print(documentID)
               
                for line in f:
                    print(line)
                    line_tokens = line.split()
                    for each in line_tokens:
                        if each not in stop_words:
                            curr_word=""
                            for x in each:
                                if x.isalnum():
                                    curr_word+=x
                            docs[documentID]+=' '+curr_word   

                            if curr_word not in tokens:
                                tokens[curr_word] = [documentID]
                            else:
                                tokens[curr_word].append(documentID)


class TrieNode:
     
    # Trie node class
    def _init_(self):
        self.children = [None]*26
 
        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False
 
class Trie:
     
    # Trie data structure class
    def _init_(self):
        self.root = self.getNode()
 
    def getNode(self):
     
        # Returns new trie node (initialized to NULLs)
        return TrieNode()
 
    def _charToIndex(self,ch):
         
        # private helper function
        # Converts key current character into index
        # use only 'a' through 'z' and lower case
         
        return ord(ch)-ord('a')

    def insert(self,key):
         
        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
 
            # if current character is not present
            if not pCrawl.children[index]:
                pCrawl.children[index] = self.getNode()
            pCrawl = pCrawl.children[index]
 
        # mark last node as leaf
        pCrawl.isEndOfWord = True
 
    def search(self, key):
         
        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            index = self._charToIndex(key[level])
            if not pCrawl.children[index]:
                return False
            pCrawl = pCrawl.children[index]
 
        return pCrawl.isEndOfWord
def parse_args():
    parser = argparse.ArgumentParser(description='Information Retrieval System Configuration')
    return parser.parse_args()

def hashFunc(s):
    ans= hash(s)
    ans=ans%1003#1003 is some primenumber
    # print(ans)
    return ans
hm={}#hashmap for preprocessing
def preprocessHash():
    for x in tokens:
        if hashFunc(x) not in hm:
            hm[hashFunc(x)]=[x]
        else:
            hm[hashFunc(x)].append(x)

#for wildcard query from here
def rotate(str, n):
    return str[n:] + str[:n]

#generate permuterm index
keys = tokens.keys()
list_permTokens=[]
for key in sorted(keys):
    dkey = key + "$"
    for i in range(len(dkey),0,-1):
        out = rotate(dkey,i)
        list_permTokens.append(out)
inverted = {}
for i in tokens.keys():
    inverted[i]=tokens.get(i)[0]
permuterm = {}
for i in range(0,len(list_permTokens)-1):
    permuterm[list_permTokens[i]]=list_permTokens[i+1]



def bitwise_and(A,B):
    return set(A).intersection(B)
def process_query(query):    
    term_list = prefix_match(permuterm,query)
    #print(term_list)
    
    docID = []
    for term in term_list:
        docID.append(inverted[term])
    #print(docID)

    temp = []
    for x in docID:
        for y in x:
            temp.append(y)
    #print(temp)        

    temp = [int(x) for x in temp]
    documentID = 0
    outputfile = open("RetrievedDocuments.txt","w")
    path = r"C:\Users\Rohan\OneDrive\Desktop\ir\Wildcard-Query-Search-Engine\proj\data1"
    for root, dirs, files in os.walk(path):
        for file in files:
            documentID = documentID + 1
            with open(os.path.join(path, file)) as f:
                for text in f:
                    if documentID in temp:
                        outputfile.write(file + "\n" + text + "\n")
            f.close()
    outputfile.close()
    return

def fun1(query):
    
    parts = query.split("*")
    if len(parts) == 3:
        case = 4
    elif parts[1] == '':
        case = 1
    elif parts[0] == '':
        case = 2
    elif parts[0] != '' and parts[1] != '':
        case = 3
    
    if case == 4:
        if parts[0] == '':
            case = 1
    print("case = ", case)

    if case == 1:
        query = parts[0]
    elif case == 2:
        query = parts[1] + "$"
    elif case == 3:
        query = parts[1] + "$" + parts[0]
    elif case == 4:
        queryA = parts[2] + "$" + parts[0]
        queryB = parts[1]
    if case != 4:
        process_query(query)
    elif case == 4:
        # queryA Z$X
        term_list = prefix_match(permuterm,queryA)
        #print(term_list)
    
    docID = []
    for term in term_list:
        docID.append(inverted[term])
    #print(docID)

    temp1 = []
    for x in docID:
        for y in x:
            temp1.append(y)
    #print(temp)        

    temp1 = [int(x) for x in temp1]
# queryB Y
    term_list = prefix_match(permuterm,queryB)
    #print(term_list)
    
    docID = []
    for term2 in term_list:
        docID.append(inverted[term2])
    #print(docID)

    temp2 = []
    for x in docID:
        for y in x:
            temp2.append(y)
    #print(temp)        

    temp2 = [int(x) for x in temp2]

    temp = bitwise_and(temp1,temp2)

  #  print(temp1,temp2,temp)    
    documentID = 0
    outputfile = open("RetrievedDocuments.txt","w")
    path = r"C:\Users\Rohan\OneDrive\Desktop\ir\Wildcard-Query-Search-Engine\proj\data1"
    for root, dirs, files in os.walk(path):
        for file in files:
            documentID = documentID + 1
            with open(os.path.join(path, file)) as f:
                for text in f:
                    if documentID in temp:
                        outputfile.write(file + "\n" + text + "\n")
            f.close()
    outputfile.close()


def prefix_match(term, prefix):
    term_list = []
    for tk in term.keys():
        if tk.startswith(prefix):
            term_list.append(term[tk])
    return term_list

def main():
    args = parse_args()
    ir = IRSystem(docs, stop_words=stop_words)
    preprocessHash()
    while True:
        query = input('Enter boolean query: ')
        for x in query:
            if(x=='*'):
                fun1(query)
                continue
        start = timeit.default_timer()
        nquery=editDistQuery(query)
        print(query)
        print(nquery)
        query=input('ENTER THE CORRECTED INPUT: ')
        results = ir.process_query(query)
    
        stop = timeit.default_timer()

        if results is not None:
            print ('Processing time: {:.5} secs'.format(stop - start))
            print('\nDoc IDS: ')
            li=[]
            for x in results:
                # print(type(x))
                filename.get(x-1)
                li.append(x)
            print(li) 
            # print(filename)   
      
def editDistQuery(query):
    finalQuery=""
    words=query.split()
    
    
    # for word in words:
    #     if hm.get(hashFunc(x)) is not None:
    #         for k in hm.get(hashFunc(x)):
    #             value=editDistDP(k,word,len(k),len(word))
    #             if(value<ans_val):
    #                 ans_val=value
    #                 finalWord=k
    #     finalQuery+=' '+finalWord
    # return finalQuery   
    for word in words:
        ans_val=100000000000000
        finalWord=""
        if(word=="AND" or word=="OR" or word=="NOT" or tokens.get(word) is not None):
            finalQuery=finalQuery+word+" "
            continue
        for k in tokens.keys():
            if(k==word):
                print("hellow")
            value=editDistDP(k,word,len(k),len(word))
            if(value<ans_val):
                ans_val=value
                finalWord=k
        finalQuery=finalQuery+finalWord+" "
    # finalQuery.strip()
    
    return finalQuery   
 
def editDistDP(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
 
    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
 
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])    # Replace
 
    return dp[m][n]
 
 
if _name_ == '_main_':
    try:
        main()
    except KeyboardInterrupt as e:
        print('EXIT')