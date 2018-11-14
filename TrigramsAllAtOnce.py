import pickle, random, sys, nltk, re

StorageName = "tsmalldictionary.pkl"
CorpusName = "bigcorpus.txt"

def CreatTriDictionary(Corpus, Storage):
    thislist1 = []
    thislist2 = []
    thislist3 = []
    thislist4 = []
    thisdic1 = {}
    thisdic2 = {}
    finaldic = {}
    prevdic = {}
    print("test")
    thislistfinalnum = []
    fptr = open(CorpusName)
    raw = fptr.read()



    words = nltk.word_tokenize(raw)
    finder = nltk.collocations.TrigramCollocationFinder.from_words(words)
    #finder.apply_freq_filter(1)
    finder.apply_word_filter(lambda w: w in ('I', 'me', '#', '?', ',', ':', '<', '>', '@'))
    trigrams =finder.ngram_fd.items()


    
    for i, j in trigrams:
        thislist1.append(i[0])
        thislist2.append(i[1])
        thislist3.append(i[2])
        thislist4.append(j)
        if (i[0],i[1]) in thisdic1:
            num = thisdic1[i[0],i[1]]
            num = num + j
            thisdic1[i[0],i[1]] = num
        if (i[0],i[1]) not in thisdic1:
            thisdic1[i[0],i[1]] = j
    for (f,b,l,k) in zip(thislist1, thislist2, thislist3, thislist4):
            num = thisdic1[f,b]
            if (f,b) in prevdic:
                prev = prevdic[f,b]
                finaldic1[f,b, (float(k)/num + prev)] = l
                prevdic[f,b] = prev + k/num
            else:
                prevdic[f] = k/num
                finaldic[f,b, (float(k)/num)] = l
    pickle.dump( finaldic, open( StorageName, "wb" ) )



def GetNextWord(dictionary, secondlastword, lastword):
    list = []
    rand = random.uniform(0,1)
    for key in dictionary:
        if (key[0] == secondlastword) and (key[1] == lastword):
            list.append(key[2])
    list.sort()
    if not list:
        return("and")
    nextword = dictionary[secondlastword ,lastword, list[0]]
    for i in list:
        if i > rand:
            nextword = dictionary[secondlastword, lastword, i]
            break
    try:
        nextword
        return(nextword)
    except NameError:
        return("error")


def main():
    try:
        sys.argv[1] and sys.argv[2] and sys.argv[3]
    except IndexError:
        print("needs an arguement")
        exit()

    if (sys.argv[1] == '0'):
        CreatTriDictionary(CorpusName, StorageName)
        exit()

    if(sys.argv[1] == '1'):
        pckledictionary = pickle.load( open( StorageName, "rb" ) )
        arguement2 = sys.argv[1]
        arguement3 = sys.argv[2]
        arguement4 = GetNextWord(pckledictionary, sys.argv[1], sys.argv[2])
        #
        i = 0
        while(i<30):
            arguement2 = arguement3
            arguement3 = arguement4
            arguement4 = GetNextWord(pckledictionary, arguement2, arguement3)
            if arguement4 == '.':
                print(arguement4)
                break;
            print(arguement4)
            i+=1

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Insufficient arguments')
        exit()
    main()
