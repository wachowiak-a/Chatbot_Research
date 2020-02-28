import nltk
import re

statement_one = 'My name is Aaron Wachowiak and I work at Walmart.'

#LOOK AT RELATION EXTRACTION- May be useful for finding patterns and creating questions that associate an entity with an action or something else.

def qa_generator(inputStr):
    orgininal_statement = inputStr
    tokens = nltk.word_tokenize(inputStr)
    tagged = nltk.pos_tag(tokens)
    copy = tagged

    #tree2conlltags gives a list of tuples, each tuple has the word, POS, and entity in that order
    entities = (nltk.tree2conlltags(nltk.ne_chunk(tagged)))
    print('ENTITIES BELOW')
    print(entities)

    #seperates the tuple into lists for the word and its entity
    words, tags, ent = zip(*entities)
    words = list(words)
    ent = list(ent)
    questions = list()
    i=0
    while i<= len(entities)-1:
        #get words with have pos B-PERSON or I-PERSON
        #Create a question that has both the first and last name? May not be super critical

        '''TAGS
        B-egin - first token of a multi-token entity
        I-n - inner token of a multi-token entity
        L-ast - Final token of a multi token entity
        U-nit - a single-token entity
        O-ut - a non-entity token
        '''

        if ent[i] == 'B-PERSON':
            questions.append("Who is " + words[i] + "?")
        elif ent[i] == 'I-PERSON':
            questions.append("Who is " + words[i] + "?")
        elif ent[i] == 'B-ORGANIZATION':
            questions.append("What is " + words[i] + "?")
            questions.append("Where is " + words[i] + "?")
            questions.append("What does " + words[i] + " do?")

        i=i+1

    for i in questions:
        print(i)

    #PATTERN RECOGNITION EXAMPLE

'''
 EXAMPLE FROM NLTK CHAPTER 7
>>> IN = re.compile(r'.*\bin\b(?!\b.+ing)')
>>> for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
...     for rel in nltk.sem.extract_rels('ORG', 'LOC', doc,
...                                      corpus='ieer', pattern = IN):
...         print(nltk.sem.rtuple(rel))
[ORG: 'WHYY'] 'in' [LOC: 'Philadelphia']
[ORG: 'McGlashan &AMP; Sarrail'] 'firm in' [LOC: 'San Mateo']'''



#    return ' '.join([t[0] for t in tagged])

print(statement_one)
qa_generator(statement_one)

#removes everything and inserts a question


#text = nltk.word_tokenize(question_one)
#print(nltk.pos_tag(text))
#print(nltk.pos_tag(nltk.word_tokenize("What is your name? His")))


#if it contains a pronoun do this, if it contains something else do this, make a who, what when where why

"""
CC coordinating conjunction
CD cardinal digit
DT determiner
EX existential there (like: “there is” … think of it like “there exists”)
FW foreign word
IN preposition/subordinating conjunction
JJ adjective ‘big’
JJR adjective, comparative ‘bigger’
JJS adjective, superlative ‘biggest’
LS list marker 1)
MD modal could, will
NN noun, singular ‘desk’
NNS noun plural ‘desks’
NNP proper noun, singular ‘Harrison’
NNPS proper noun, plural ‘Americans’
PDT predeterminer ‘all the kids’
POS possessive ending parent’s
PRP personal pronoun I, he, she
PRP$ possessive pronoun my, his, hers
RB adverb very, silently,
RBR adverb, comparative better
RBS adverb, superlative best
RP particle give up
TO, to go ‘to’ the store.
UH interjection, errrrrrrrm
VB verb, base form take
VBD verb, past tense took
VBG verb, gerund/present participle taking
VBN verb, past participle taken
VBP verb, sing. present, non-3d take
VBZ verb, 3rd person sing. present takes
WDT wh-determiner which
WP wh-pronoun who, what
WP$ possessive wh-pronoun whose
WRB wh-abverb where, when


"""
