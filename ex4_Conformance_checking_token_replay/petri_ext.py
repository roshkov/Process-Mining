class PetriNet():

    def __init__(self):
        self.PaT = {}
        #self.Transitions = []

    def add_place(self, name):
        self.PaT.update({name: {'type':'place', 'obj': Place(name)}  })

    def add_transition(self, name, id):
        self.PaT.update({id: {'type':'trans', 'obj': Transition(name, id)}  })
    
    def add_edge(self, source, target):
        
        s = self.PaT[source]
        t = self.PaT[target]
        
        
        if (s['type']=='place' and t['type']=='trans'):
            t['obj'].addInput(source)
            #print('this one')
            
        elif (s['type']=='trans' and t['type']=='place'):
            s['obj'].addOutput(target)
            #print('another one')
        return self
            
    
    def getPat(self):
        print( self.PaT)
   
    def get_tokens(self, place):
        p = self.PaT[place]
        
        if p and p['type'] == 'place':
            return p['obj'].get_tokens()


    def countAllRemainingTokens (self):
        remaining_token_counter = 0
        
        for item in self.PaT:
            if self.PaT[item]['type'] == 'place':
                remaining_token_counter += self.PaT[item]['obj'].get_tokens()
        
        # print(remaining_token_counter)
        return remaining_token_counter 


    def is_enabled(self, transition):
        inp = self.PaT[transition]['obj'].getAllInputs()
        res = True
        
        for placeId in inp:
            if self.get_tokens(placeId) == 0:
                res = False
                break
        return res
            

    def add_marking(self, place):
        self.PaT[place]['obj'].addToken()

    # id of transition is passed as parameter
    # also returns amount of inputs and outputs
    def fire_transition(self, transition):
        inp = self.PaT[transition]['obj'].getAllInputs()
        oup = self.PaT[transition]['obj'].getAllOutputs()
        
        
        for placeId in inp:
            self.PaT[placeId]['obj'].removeAllTokens()

            
        for placeId in oup:
            self.PaT[placeId]['obj'].addToken()
        
        return len(inp), len(oup)
            
            
    def transition_name_to_id(self, tr_name):
        resId = None
        for item in self.PaT:
            t = self.PaT[item]
            if ( t['type']=='trans' and t['obj'].getName() == tr_name):
                resId = t['obj'].getId()
                break
        return resId
    
    
    # Checks the amount of tokens in each input of a given transition
    # Basically, to fire a transition, all inputs (aka places) must have 1 token each
    # This function checks that and if any input (aka place) does not have a token
    # then it adds the token. As well, this function returns the amount of tokens
    # that were added 'artificially'
    def checkTokenBalanceOfTransitionInputs(self, transition):
        
        inp = self.PaT[transition]['obj'].getAllInputs()
        added_tokens_counter = 0
        
        for i in inp:
            
            #if input (place) has no tokens, then adding one
            if (self.PaT[i]['obj'].get_tokens() == 0):
                self.PaT[i]['obj'].addToken()
                added_tokens_counter+=1
            
            
        
        return added_tokens_counter
        
    
    def removeTokenFromOutput(self, transition):
        oup = self.PaT[transition]['obj'].getAllOutputs()
        for o in oup:
            self.PaT[o]['obj'].removeAllTokens()
        
    
                
        
        
            



class Place:
    def __init__ (self, id):
        self.tokens = 0
        self.id = id
        
    def get_tokens (self): 
        return self.tokens
    
    def addToken (self):
        self.tokens += 1 
        
    def removeAllTokens (self):
        self.tokens= 0
        
    def getId (self):
        return self.id
    
    
class Transition:
     def __init__ (self, name, id):
        self.name = name
        self.id = id
        self.Inputs = []
        self.Outputs = []
          
     def addInput (self, idOfInputPlace):
        self.Inputs.append(idOfInputPlace)
    
     def addOutput (self, idOfOutputPlace):
        self.Outputs.append(idOfOutputPlace)
        
     def removeInput (self, idOfInputPlace):
        self.Inputs.remove(idOfInputPlace)
    
     def removeOutput (self, idOfOutputPlace):
        self.Outputs.remove(idOfOutputPlace)
    
     def getAllInputs (self):
        return self.Inputs
    
     # checks the input places and counts how many places with no tokens
     # are going into this transitions. Returns number value
     # def checkInputsWithNoTokens(self):
         
     #     for i in self.Inputs:
     #         #Inputs[] store only ids of input place
     #         i
    
     def getAllOutputs (self):
         return self.Outputs
     
     def getName (self):
         return self.name
     
     def getId (self):
         return self.id












# p = PetriNet()

# p.add_place(1)  # add place with id 1
# p.add_place(2)
# p.add_place(3)
# p.add_place(4)
# p.add_transition("A", -1)  # add transition "A" with id -1
# p.add_transition("B", -2)
# p.add_transition("C", -3)
# p.add_transition("D", -4)

# p.add_edge(1, -1)
# p.add_edge(-1, 2)
# p.add_edge(2, -2).add_edge(-2, 3)
# p.add_edge(2, -3).add_edge(-3, 3)
# p.add_edge(3, -4)
# p.add_edge(-4, 4)
        
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.add_marking(1)  # add one token to place id 1
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-1)  # fire transition A
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-3)  # fire transition C
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-4)  # fire transition D
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.add_marking(2)  # add one token to place id 2
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-2)  # fire transition B
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# p.fire_transition(-4)  # fire transition D
# print(p.is_enabled(-1), p.is_enabled(-2), p.is_enabled(-3), p.is_enabled(-4))

# # by the end of the execution there should be 2 tokens on the final place
# print(p.get_tokens(4))

# print (p.transition_name_to_id('C'))