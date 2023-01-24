from multiprocessing.sharedctypes import copy
import os
from quopri import decodestring
from random import *
import random
import datetime
import bisect

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

class Genoma:
    def __init__(self, numberOfGenes = 30, nInputs = 4, rateMutation = 0.1):
        self.genotipo = []
        self.copyGenotipo = []
        self.numberOfGenes = numberOfGenes
        self.faultChance = 1
        self.nInputs = nInputs
        self.nOutputs = 2**nInputs
        self.fitness = 0.0
        self.noiseFitness = 0.0
        self.rateMutation = rateMutation
        self.deadGenesRate = 0.6
        self.activeGenesRate = 0.4
        self.flagDeadActive = 0
        self.indexDeadGenes = []
        self.indexActiveGenes = []
        self.Stochasticity = 0
        self.ToEvaluate = []

    def setGenotipo(self, a):
      self.genotipo = a.copy()
      

    def fill_Initial_Genome(self):
        for i in range (0,self.numberOfGenes):
            self.genotipo.append("")

    def generate_parent(self):  

        self.fill_Initial_Genome()          # fill the genome with the rigth length
        
        for i in range(0,self.numberOfGenes):

            in1 = randint(0,i+self.nInputs-1)    # returns a number between 0 and n (PS: in randint() both inputs are included)
            in2 = randint(0,i+self.nInputs-1)    # returns a number between 0 and n (PS: in randint() both inputs are included)
        
            sin1 = str(in1)
            sin2 = str(in2)

            gene = sin1 +"-"+ sin2
            self.genotipo.pop(i)
            self.genotipo.insert(i, gene)



    # 0102 0102 0102 0102 0102 0102

    def identify_deadGenes(self):
    
      for i in range (0,self.numberOfGenes-1):
        self.ToEvaluate.append(False)
      self.ToEvaluate.append(True)

      p = self.numberOfGenes-1
      while p>=0:
        
        if self.ToEvaluate[p]:
          inputs = self.genotipo[p].split("-")
          input1 = int(inputs[0])
          input2 = int(inputs[1])
          x = input1 - self.nInputs 
          y = input2 - self.nInputs                   
          if(x >= 0):
            self.ToEvaluate[x] = True
          if(y >= 0):
            self.ToEvaluate[y] = True
        
        p-=1
      
    def withdraw_deadGenes(self):  #Withdraw the genes that won't be used in any other position of the genome
              
            self.copyGenotipo = self.genotipo.copy()
            count = 1
            s = Stack()
            while(True):
                self.indexDeadGenes = []
                for j in range(0,self.numberOfGenes-1):       
                    for i in range (0,self.numberOfGenes):       #The iº gene of the genome. To each element of the list (each gene of genome) exception by the last (the last one is necessarily the output of the system).
                        nin = self.copyGenotipo[i].split("-")
                        nin1 = nin[0]  #The fisrt half (the input1)
                        nin2 = nin[1]  #The second half (the input2)
                        elementSearch = str(j+self.nInputs)

                        if(elementSearch == nin1 or elementSearch == nin2):
                            break

                        elif(i == self.numberOfGenes-1):
                            self.copyGenotipo[j] = "xx-xx"
                            self.indexDeadGenes.append(j)

                s.push(len(self.indexDeadGenes))

                if s.size() == 2:
                    felement = s.pop()
                    selement = s.pop()
                    if(selement == felement):
                        break
                    s.push(felement)

            for i in range(0,self.numberOfGenes):
                if(self.copyGenotipo[i] != "xx-xx"):
                    self.indexActiveGenes.append(i)

    def gpinand(self, l):
        count = 0
        n = len(l)
        for i in range(0,n):
          if(l[i] == 1):
            count+=1

        if(count%2 == 0):
            return 0
        else: 
            return 1
    
    def gpinandOld(self, in1,in2,in3):
        count = 0
        if(in1 == 1):
          count+=1
        if(in2 == 1):
          count+=1
        if(in3 == 1):
          count+=1
        
        if(count%2 == 0):
            return 0
        else: 
            return 1

    def NAND(self,a,b):
        if(not(a and b)):
            return 1
        else:
            return 0
        
    def badNAND(self,a,b):
        if(not(a and b)):
            return 0
        else:
            return 1
        
    def getCartesianProduct(self,l):
        CartesianProduct = [[]]
        for iterable in l:
          CartesianProduct = [a+[b] for a in CartesianProduct for b in iterable]
        return CartesianProduct

    def calculateFitnessWithFaultsOld(self):
        if(self.flagDeadActive == 1):
          self.withdraw_deadGenes()
        
        fitnessCounter = 0
        for i0 in range(0,2):
            for i1 in range(0,2):
                for i2 in range(0,2):
                    for i3 in range(0,2):
                        valuesTable = {'0':i0, '1':i1, '2':i2, '3':i3}
                        i = 4
                        for element in self.genotipo:
                            elements = element.split("-")
                            in1 = elements[0]
                            in2 = elements[1]
                            x = randint(0, 100)
                            if(x<=self.faultChance):
                              out = self.badNAND(valuesTable[in1], valuesTable[in2])
                            else:
                              out = self.NAND(valuesTable[in1], valuesTable[in2])
                            si = str(i)
                            valuesTable[si] = out
                            i+=1
                        if(valuesTable[si] == self.gpinandOld(valuesTable['0'],valuesTable['1'],valuesTable['2'],valuesTable['3'])):
                            fitnessCounter += 1
                            
        self.fitness = float(fitnessCounter/self.nOutputs)
    
    def calculateFitnessOld(self):
        if(self.flagDeadActive == 1):
          self.withdraw_deadGenes()
        
        fitnessCounter = 0
        for i0 in range(0,2):
            for i1 in range(0,2):
                for i2 in range(0,2):
                        valuesTable = {'0':i0, '1':i1, '2':i2}
                        i = 3
                        for element in self.genotipo:
                            elements = element.split("-")
                            in1 = elements[0]
                            in2 = elements[1]
                            x = randint(0, 100)
                            out = self.NAND(valuesTable[in1], valuesTable[in2])
                            si = str(i)
                            valuesTable[si] = out
                            i+=1
                        if(valuesTable[si] == self.gpinandOld(valuesTable['0'],valuesTable['1'],valuesTable['2'])):
                            fitnessCounter += 1
                            
        self.fitness = float(fitnessCounter/self.nOutputs)
    def calculateFitness(self):
        if(self.flagDeadActive == 1):
          self.withdraw_deadGenes()
        fitnessCounter = 0
        l = []
        dic =  dict() 

        for i in range(0,self.nInputs):
            subL = [0,1]
            l.append(subL)

        TrueTable = self.getCartesianProduct(l)

        for i in range(0,self.nOutputs):
            ithTrueTable = TrueTable[i]
            for input in range(0,self.nInputs):
                sinput = str(input)
                dic[sinput] = ithTrueTable[input]

            indexOut = self.nInputs
            for element in self.genotipo:
                  elements = element.split("-")
                  in1 = elements[0]
                  in2 = elements[1]
                  out = self.NAND(dic[in1], dic[in2])
                  sindexOut = str(indexOut)
                  dic[sindexOut] = out
                  indexOut+=1

            lGPINAND = []
            for m in range(0,self.nInputs):
              sm = str(m)
              value = dic[sm]
              lGPINAND.append(value)

            if(dic[sindexOut] == self.gpinand(lGPINAND)):
                fitnessCounter += 1
                            
        self.fitness = float(fitnessCounter/self.nOutputs)    
    def calculateFitnessNew(self):
        fitnessCounter = 0
        l = []
        dic =  dict() 

        for i in range(0,self.nInputs):
            subL = [0,1]
            l.append(subL)

        TrueTable = self.getCartesianProduct(l)

        for i in range(0,self.nOutputs):
            ithTrueTable = TrueTable[i]
            for input in range(0,self.nInputs):
                sinput = str(input)
                dic[sinput] = ithTrueTable[input]

            indexOut = self.nInputs
            position = 0
            for element in self.genotipo:
              
                if(self.ToEvaluate[position]):
                  elements = element.split("-")
                  in1 = elements[0]
                  in2 = elements[1]
                  out = self.NAND(dic[in1], dic[in2])
                  sindexOut = str(indexOut)
                  dic[sindexOut] = out

                indexOut+=1
                position+=1

            lGPINAND = []
            for m in range(0,self.nInputs):
              sm = str(m)
              value = dic[sm]
              lGPINAND.append(value)

            if(dic[sindexOut] == self.gpinand(lGPINAND)):
                fitnessCounter += 1
                            
        self.fitness = float(fitnessCounter/self.nOutputs)
        
    def calculateFitnessWithFaults(self):
        if(self.flagDeadActive == 1):
          self.withdraw_deadGenes()
        fitnessCounter = 0
        l = []
        dic =  dict() 

        for i in range(0,self.nInputs):
            subL = [0,1]
            l.append(subL)

        TrueTable = self.getCartesianProduct(l)

        for i in range(0,self.nOutputs):
            ithTrueTable = TrueTable[i]
            for input in range(0,self.nInputs):
                sinput = str(input)
                dic[sinput] = ithTrueTable[input]

            indexOut = self.nInputs
            for element in self.genotipo:
                elements = element.split("-")
                in1 = elements[0]
                in2 = elements[1]
                x = randint(0, 100)
                if(x<=self.faultChance):
                    out = self.badNAND(dic[in1], dic[in2])
                else:
                    out = self.NAND(dic[in1], dic[in2])
                sindexOut = str(indexOut)
                dic[sindexOut] = out
                indexOut+=1

            lGPINAND = []
            for m in range(0,self.nInputs):
              sm = str(m)
              value = dic[sm]
              lGPINAND.append(value)

            if(dic[sindexOut] == self.gpinand(lGPINAND)):
                fitnessCounter += 1
                            
        self.fitness = float(fitnessCounter/self.nOutputs)

    def calculateFitnessWithFaultsNew(self):
        fitnessCounter = 0
        l = []
        dic =  dict() 

        for i in range(0,self.nInputs):
            subL = [0,1]
            l.append(subL)

        TrueTable = self.getCartesianProduct(l)

        for i in range(0,self.nOutputs):
            ithTrueTable = TrueTable[i]
            for input in range(0,self.nInputs):
                sinput = str(input)
                dic[sinput] = ithTrueTable[input]

            indexOut = self.nInputs
            position = 0
            for element in self.genotipo:
              
                if(self.ToEvaluate[position]):
                  elements = element.split("-")
                  in1 = elements[0]
                  in2 = elements[1]
                  x = randint(0, 100)
                  if(x<=self.faultChance):
                      out = self.badNAND(dic[in1], dic[in2])
                  else:
                      out = self.NAND(dic[in1], dic[in2])
                  sindexOut = str(indexOut)
                  dic[sindexOut] = out

                indexOut+=1
                position+=1

            lGPINAND = []
            for m in range(0,self.nInputs):
              sm = str(m)
              value = dic[sm]
              lGPINAND.append(value)

            if(dic[sindexOut] == self.gpinand(lGPINAND)):
                fitnessCounter += 1
                            
        self.fitness = float(fitnessCounter/self.nOutputs)

    def calculateNoiseFitness(self):
        noise = random.uniform(-self.Stochasticity,self.Stochasticity)
        noise = round(noise,4)
        self.noiseFitness = self.fitness + noise
        

    def copyGene(self, destiny):
        destiny.genotipo = self.genotipo.copy()
        destiny.copyGenotipo = self.copyGenotipo.copy()
        destiny.fitness = self.fitness 
        destiny.noiseFitness = self.noiseFitness
        destiny.flagDeadActive = self.flagDeadActive
        destiny.indexDeadGenes = self.indexDeadGenes.copy()
        destiny.indexActiveGenes = self.indexActiveGenes.copy()
        destiny.nOutputs = self.nOutputs 

    def mutateWithParam(self):
        
        childGenes = Genoma()                                                    # a copy of the parente that will be mutate
        self.copyGene(childGenes)


        deadMutationIndex = int(len(self.indexDeadGenes) * self.deadGenesRate)    # 50% of the active genes will be mutate
        i=0
        while(i < deadMutationIndex):
            
            indexMut = random.sample(self.indexDeadGenes, 1)
            index = int(indexMut[0])
            newGene,alternate = random.sample(list(range(0,index+self.nInputs)),2)

            if newGene < 10:
                newGene = "0"+str(newGene)
            newGene = str(newGene)    
            if alternate < 10:
                alternate = "0"+str(alternate)
            alternate = str(alternate)  

            inputPosition = randint(0,1)                            # in the random input of the gene (the first or second)

            if inputPosition == 0:                                  # if the input that need to be mutate is the first:
                if index == self.index1 or index == self.index2 or index == self.index3 or  index == self.index4:    
                    return self                                     # if the index of any mutate is the same of the inputs index, return parent

                if newGene == childGenes.genotipo[index][0:2]:
                    childGenes.genotipo[index] = alternate + str(childGenes.genotipo[index][2:4])     
                else:
                    childGenes.genotipo[index] = newGene + str(childGenes.genotipo[index][2:4])

            else:
                if newGene == childGenes.genotipo[index][2:4]:               # if the input that need to be mutate is the second:
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + alternate
                else: 
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + newGene

            i+=1

        activeMutationIndex = max(2,int(len(self.indexActiveGenes) * self.activeGenesRate) ) # 20% of the active genes will be mutate
        j = 0
        while(j < activeMutationIndex):
            indexMut = random.sample(self.indexActiveGenes, 1)
            index = int(indexMut[0])
            newGene,alternate = random.sample(list(range(0,index+self.nInputs)),2)

            newGene = str(newGene)    
      
            alternate = str(alternate)   
            
            inputPosition = randint(0,1)                            # in the random input of the gene (the first or second)

            if inputPosition == 0:                                  # if the input that need to be mutate is the first:
                if index == self.index1 or index == self.index2 or index == self.index3 or  index == self.index4:    
                    return self                                   # if the index of any mutate is the same of the inputs index, return parent

                if newGene == childGenes.genotipo[index][0:2]:
                    childGenes.genotipo[index] = alternate + str(childGenes.genotipo[index][2:4])     
                else:
                    childGenes.genotipo[index] = newGene + str(childGenes.genotipo[index][2:4])

            else:
                if newGene == childGenes.genotipo[index][2:4]:               # if the input that need to be mutate is the second:
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + alternate
                else: 
                    childGenes.genotipo[index] = str(childGenes.genotipo[index][0:2]) + newGene
            j +=1
        
        return childGenes
    
    def mutate(self):
        
        childGenes = Genoma()                                                    # a copy of the parente that will be mutate
        self.copyGene(childGenes)
        
        numberOfMutations = max(self.numberOfGenes*self.rateMutation,1)

        for i in range(0,int(numberOfMutations)):

            indexMut = randint(1,self.numberOfGenes-1)
            newGene,alternate = random.sample(list(range(0,indexMut+self.nInputs)),2)

            newGene = str(newGene)     
            alternate = str(alternate)   

            whichInput = randint(0,1) 
            inputs = childGenes.genotipo[indexMut].split("-")
            input1 = inputs[0]
            input2 = inputs[1]
            if(whichInput == 0):
                if newGene == input1:
                    childGenes.genotipo[indexMut] = alternate + "-" + input2
                else: 
                    childGenes.genotipo[indexMut] = newGene + "-" + input2
            else:
                if newGene == input2:
                    childGenes.genotipo[indexMut] = input1 + "-" + alternate
                else: 
                    childGenes.genotipo[indexMut] = input1 + "-" + newGene

        
        return childGenes

class GeneticAlgorithm():
    def __init__(self, step = 1/16, alpha = 0, y = 10, maxGeneration = 400000):
        self.step = step
        self.y = y
        self.startTime = datetime.datetime.now()
        self.data_atual = datetime.datetime.today()
        self.totalGeneration = 0
        self.countGeneration = 0
        self.maxGeneration = maxGeneration
        self.histogram= []

    def display(self, guess, fitness, noiseFitness, totalGeneration):
        sguess = ' '.join(guess)
        timeDiff = datetime.datetime.now() - self.startTime

        print("{0}\t {1}\t {2}\t Geração: {3} Tempo: {4}\n ".format(sguess, fitness, round(noiseFitness, 4), self.totalGeneration, str(timeDiff), self.totalGeneration))

    def saveNetlists(self, generation, fitness,noiseFitness ,countGeneration):
        fImprovedNetlist = open("Netlists improved.txt", 'a', encoding='utf-8')      # The file that save the improveds genomes
        
        data_atual = datetime.datetime.today()
        sbestParent = ' '.join(generation)                                           # Convert the child in str to append the genome in Netlists improved.txt
        appendFile = sbestParent+" at "+str(data_atual)+ " " + str(fitness) + " " + str(noiseFitness) + " Geração: "+str(countGeneration) + "\n"  # Make the string format to append
        fImprovedNetlist.write(appendFile)                                           # Append the string in Netlists improved.txt 
        fImprovedNetlist.close()

    def makeHistgram(self, childFitness):                                                  # make the histogram list                                                         
        bisect.insort(self.histogram,str(childFitness))                                # Using the bisect library, insert the fitness garanting the sorting

    def saveHistogram(self):
        fHistogram = open("histgramArray.txt", 'a', encoding='utf-8')
        sHistogramList = ','.join(self.histogram)                                           # Convert the histogram in str to append in histgramArray.txt
        appendFile = sHistogramList
        fHistogram.write(appendFile)                                                     
        fHistogram.close()

    def getBestGenomeWithSize(self, listChild):
        bestChild = listChild[0]
        for child in listChild:
            if (child.noiseFitness > bestChild.noiseFitness):
                    bestChild = child
            elif((child.noiseFitness == bestChild.noiseFitness) and (len(child.indexActiveGenes) <= len(bestChild.indexActiveGenes))):
                    bestChild = child
              
        return bestChild
    def getBestGenome(self, listChild):
        bestChild = listChild[0]
        for child in listChild:
            if(child.fitness > bestChild.fitness):
                bestChild = child
                
        return bestChild


    def evolution(self):
        
        bestParent = Genoma() 
        bestParent.generate_parent() # Generate the first generation (The first Parent)
        # bestParent.calculateFitness()  # Get the first generation fitness
        bestParent.calculateFitnessWithFaults()
        bestParent.calculateNoiseFitness()
        self.display(bestParent.genotipo, bestParent.fitness,bestParent.noiseFitness, self.totalGeneration)
       
        listGenomes = []
        ffc = 0
        
        reference = Genoma()
        bestParent.copyGene(reference)
        nd = 20
        
        while True:
            self.totalGeneration = self.totalGeneration + 1
            listGenomes.clear()
            
            cf = 0
            for i in range(0,nd):
                bestParent.calculateFitnessWithFaults()
                cf = cf + bestParent.fitness
            bestParent.fitness = cf/nd
            bestParent.calculateNoiseFitness()
            
            listGenomes.append(bestParent)
            
            for i in range(0, self.y):
                child = Genoma()
                bestParent.mutate().copyGene(child) 
                
                #child.calculateFitness()
                #child.calculateFitnessWithFaults()
                cf = 0
                for i in range(0,nd):
                    child.calculateFitnessWithFaults()
                    cf = cf + child.fitness
                child.fitness = cf/nd
                child.calculateNoiseFitness()
                
                listGenomes.append(child)

            self.getBestGenomeWithSize(listGenomes).copyGene(bestParent)
            
            if(self.totalGeneration % 1000 == 0):
                self.display(bestParent.genotipo, bestParent.fitness,bestParent.noiseFitness,self.totalGeneration)
                # For debugging: Show the mutations
                # ind = 0
                # for i,j in zip(bestParent.genotipo,reference.genotipo):
                #     if i != j:
                #         print(ind+4,':',j,'->',i)
                #     ind += 1
                # bestParent.copyGene(reference)
                # print('\n')
            
            if(self.totalGeneration>=self.maxGeneration):
                break
            
            if (bestParent.fitness >= 1):    # if the child fitness is 1 or the we have more than 10000 tries of mutation to that child, end the algorithm
                ffc += 1
                if (ffc == 10000):
                    self.display(bestParent.genotipo,bestParent.fitness,bestParent.noiseFitness,self.totalGeneration)
                    break
            
        bestParent.withdraw_deadGenes()
        print('Active part of the genotype of the last genome', bestParent.indexActiveGenes)
        timeDiff = datetime.datetime.now() - self.startTime
        print("The end in: ",str(timeDiff))

    def evolutionPerformanceDiff(self):
        
        bestParent = Genoma() 
        bestParent.generate_parent() # Generate the first generation (The first Parent)
        # set the same parent to the evolution with the new Mutate()
        bestParent_improved = Genoma()
        bestParent_improved.setGenotipo(bestParent.genotipo)

        bestParent.calculateFitness()  
        bestParent.calculateNoiseFitness()
        self.display(bestParent.genotipo, bestParent.fitness,bestParent.noiseFitness, self.totalGeneration)
       
        listGenomes = []
        ffc = 0
        
        reference = Genoma()
        bestParent.copyGene(reference)
        nd = 1
        
        while True:
            self.totalGeneration = self.totalGeneration + 1
            listGenomes.clear()
            
            cf = 0
            for i in range(0,nd):
                bestParent.calculateFitness()
                cf = cf + bestParent.fitness
            bestParent.fitness = cf/nd
            bestParent.calculateNoiseFitness()
            
            listGenomes.append(bestParent)
            
            for i in range(0, self.y):
                child = Genoma()
                bestParent.mutate().copyGene(child) 

                cf = 0
                for i in range(0,nd):
                    child.calculateFitness()
                    cf = cf + child.fitness
                child.fitness = cf/nd
                child.calculateNoiseFitness()
                
                listGenomes.append(child)

            self.getBestGenomeWithSize(listGenomes).copyGene(bestParent)
            
            if(self.totalGeneration % 1000 == 0):
                self.display(bestParent.genotipo, bestParent.fitness,bestParent.noiseFitness,self.totalGeneration)

            
            if(self.totalGeneration>=self.maxGeneration):
                break
            
            if (bestParent.fitness >= 1):
                ffc += 1
                if (ffc == 10000):
                    self.display(bestParent.genotipo,bestParent.fitness,bestParent.noiseFitness,self.totalGeneration)
                    break
            
        bestParent.withdraw_deadGenes()
        print('Active part of the genotype of the last genome', bestParent.indexActiveGenes)
        timeDiff1 = datetime.datetime.now() - self.startTime
        print("The end in: ",str(timeDiff1))

        # THE NEW WAY ############################################################
        self.totalGeneration = 0
        self.startTime = datetime.datetime.now()
        self.data_atual = datetime.datetime.today()
        bestParent_improved.identify_deadGenes()
        bestParent_improved.calculateFitnessNew()  
        bestParent_improved.calculateNoiseFitness()
        self.display(bestParent_improved.genotipo, bestParent_improved.fitness,bestParent_improved.noiseFitness, self.totalGeneration)
       
        listGenomes = []
        ffc = 0
        
        reference = Genoma()
        bestParent_improved.copyGene(reference)
        nd = 1
        
        while True:
            self.totalGeneration = self.totalGeneration + 1
            listGenomes.clear()
            
            cf = 0
            for i in range(0,nd):
                bestParent_improved.identify_deadGenes()
                bestParent_improved.calculateFitnessNew()
                cf = cf + bestParent_improved.fitness
            bestParent_improved.fitness = cf/nd
            bestParent_improved.calculateNoiseFitness()
            
            listGenomes.append(bestParent_improved)
            
            for i in range(0, self.y):
                child = Genoma()
                bestParent_improved.mutate().copyGene(child) 

                cf = 0
                for i in range(0,nd):
                    child.identify_deadGenes()
                    child.calculateFitnessNew()
                    cf = cf + child.fitness
                child.fitness = cf/nd
                child.calculateNoiseFitness()
                
                listGenomes.append(child)

            self.getBestGenomeWithSize(listGenomes).copyGene(bestParent_improved)
            
            if(self.totalGeneration % 1000 == 0):
                self.display(bestParent_improved.genotipo, bestParent_improved.fitness,bestParent_improved.noiseFitness,self.totalGeneration)

            
            if(self.totalGeneration>=self.maxGeneration):
                break
            
            if (bestParent_improved.fitness >= 1):
                ffc += 1
                if (ffc == 10000):
                    self.display(bestParent_improved.genotipo,bestParent_improved.fitness,bestParent_improved.noiseFitness,self.totalGeneration)
                    break

        timeDiff2 = datetime.datetime.now() - self.startTime
        print("The end in: ",str(timeDiff2))

        print(timeDiff1 - timeDiff2)
        print(timeDiff2/timeDiff1)

 
    def back_foward_propagation_Proof(self,attempts):
      backPropagationCounter=0
      flagBackPropagation = True
      flagFowardPropagation = True
      fowardPropagationCounter=0
      
      x=0
      while(x<attempts):
        x+=1
        bestParent = Genoma() 
        bestParent.generate_parent()

        bestParent.identify_deadGenes()
        bestParent.withdraw_deadGenes()

        #print("ToEvaluate: ", bestParent.ToEvaluate)
        #print("indexActiveGenes: ", bestParent.indexActiveGenes)

        for i in range(0,bestParent.numberOfGenes):
          #print("i: ",i,"bestParent.ToEvaluate[i]: ",bestParent.ToEvaluate[i]," ")
          if(bestParent.ToEvaluate[i]):
            if(not(i in bestParent.indexActiveGenes)):
              flagBackPropagation = False
              break
          else:
            if(i in bestParent.indexActiveGenes):
              flagBackPropagation = False
              break
        if(flagBackPropagation):
          backPropagationCounter+=1
        else:
          flagBackPropagation = True

        bestParent.calculateFitness()
        fitnessOld = bestParent.fitness

        bestParent.calculateFitnessNew()
        fitnessNew = bestParent.fitness

        if(fitnessOld == fitnessNew):
          fowardPropagationCounter+=1

        
      print("Backpropagation Robustness:  ")
      print("Counter: ", backPropagationCounter)
      print("Attempts: ", attempts)
      print("Accuracy: ", backPropagationCounter/attempts)
      print("                              ")      

      print("Fowardpropagation Robustness:  ")
      print("Counter: ", fowardPropagationCounter)
      print("Attempts: ", attempts)
      print("Accuracy: ", fowardPropagationCounter/attempts)
      print("                              ")      


    def deep_foward_propagation_Proof(self):
        fowardPropagationCounter = 0
        attempts = 0
        flagFowardPropagation = True
        
        listGenomes = []
        
        bestParent = Genoma() 
        bestParent.generate_parent() # Generate the first generation (The first Parent)
        
        bestParent.calculateFitness()  # Get the first generation fitness
        
        fitnessOld = bestParent.fitness
        
        bestParent.identify_deadGenes()
        bestParent.calculateFitnessNew()
        fitnessNew = bestParent.fitness

        if(fitnessOld != fitnessNew):
          attempts+=1
          flagFowardPropagation = False
        
        attempts+=1
        if(flagFowardPropagation):
          fowardPropagationCounter+=1
          while True:
            self.totalGeneration = self.totalGeneration + 1
            listGenomes.clear()
            listGenomes.append(bestParent)
            
            for i in range(0, self.y):
                child = Genoma()
                bestParent.mutate().copyGene(child)  
                child.calculateFitness()
                fitnessOld = child.fitness
                child.identify_deadGenes()
                child.calculateFitnessNew()
                fitnessNew = child.fitness
                listGenomes.append(child)
                attempts+=1
                if(fitnessOld == fitnessNew):
                  fowardPropagationCounter+=1

            self.getBestGenome(listGenomes).copyGene(bestParent)
  
            if(self.totalGeneration>=self.maxGeneration):
                break
            
            if (bestParent.fitness >= 1):    # if the child fitness is 1 or the we have more than 10000 tries of mutation to that child, end the algorithm
                print("We did it! The fitness arrived in: ", bestParent.fitness)
        print("Fitness: ")
        print("Fowardpropagation Robustness:  ")
        print("Counter: ", fowardPropagationCounter)
        print("Attempts: ", attempts)
        print("Accuracy: ", fowardPropagationCounter/attempts)

