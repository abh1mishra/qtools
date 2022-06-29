import numpy as np
import cvxpy as cv
from itertools import chain, combinations, product
import re


class NpaHierarchy:

    def joinProjectors(self,arr):
        arr=np.delete(arr,np.where(np.diff(arr)==0))
        return arr

    def sepAandB(self,arr):
        return np.concatenate([np.extract((arr>=i[0])&(arr<=i[-1]),arr) for i in self.flatOprArray])

    def checkZero(self,arr):
        for i in range(len(arr)-1):
            consSet={arr[i],arr[i+1]}
            for j in self.groups:
                if(consSet==j):
                    return 0

    def processStrings(self,arr):
        arr=self.sepAandB(arr)
        arr=self.joinProjectors(arr)
        if(self.checkZero(arr)==0):
            return 0
        arr=arr.astype('int64')
        if(tuple(arr) in self.probTupleSet):
            return self.probTupleSet[tuple(arr)]
        return cv.Variable(complex=True)

    def addObjective(self,objective):
        self.addConstraints(objective=[objective])

    def solve(self):
        return cv.Problem(cv.Maximize(self.objective),self.additionalConstraints+self.trivialConstraints).solve()

    def addConstraints(self,constraints=None,objective=None):
        self.additionalConstraints=[]
        eqn=(objective is None) and constraints or objective
        eqn=[i.replace(" ","").lower() for i in eqn]
        pattern=(objective is None) and (re.compile(r"^([0-9]*\.?[0-9]*p[a-z]+\([0-9]+\|[0-9]+\))([+-][0-9]*\.?[0-9]*p[a-z]+\([0-9]+\|[0-9]+\))*(<?=.+)$")) or (re.compile(r"^([0-9]*p[a-z]+\([0-9]+\|[0-9]+\))([+-][0-9]*p[a-z]+\([0-9]+\|[0-9]+\))*"))
        subPatternPos=re.compile(r"[+][0-9]*\.?[0-9]*p[a-z]+\([0-9]+\|[0-9]+\)")
        subPatternNeg=re.compile(r"[-][0-9]*\.?[0-9]*p[a-z]+\([0-9]+\|[0-9]+\)")
        const_pattern=re.compile(r"(\+|\-)([0-9]*\.?[0-9]*)(.+)")
        split_pattern=re.compile('(<{0,1}=)(.+)')
        if(all((pattern.fullmatch(i)) for i in eqn)):
            for i in eqn:
                s="+"+i
                posOpr=subPatternPos.findall(s)
                negOpr=subPatternNeg.findall(s)
                const_j=0
                for j in posOpr:
                    const_groups=re.fullmatch(const_pattern,j).groups()
                    const_j+=(const_groups[1]=="") and (self.probStrSet[const_groups[2]]) or (float(const_groups[1])*self.probStrSet[const_groups[2]])
                for j in negOpr:
                    const_groups=re.fullmatch(const_pattern,j).groups()
                    const_j-=(const_groups[1]=="") and (self.probStrSet[const_groups[2]]) or (float(const_groups[1])*self.probStrSet[const_groups[2]])
                if(objective is None):
                    if(s.find("<")!=-1):
                        self.additionalConstraints.append(const_j<=float(split_pattern.findall(s)[0][1]))
                    else:
                        self.additionalConstraints.append(const_j==float(split_pattern.findall(s)[0][1]))
                else:
                    self.objective=const_j


        else:
            raise Exception("check your constriants")


    def AMaker(self):
        # for sod in self.probStrSet:
        #     print(sod,self.probStrSet[sod])
        # print(self.probStrSet)
        A=np.empty((len(self.row),len(self.row)),dtype=object)
        for j in range(len(self.row)):
            for k in range(len(self.row)):
                str=np.concatenate([self.row[j][::-1],self.row[k]])
                # print(str,end=" ")
                A[j][k]=self.processStrings(str)
                # print(A[j][k],end=" ")
                if(j!=k):
                    A[k][j]=(A[j][k])
            # print()
        A=cv.bmat(A)
        self.trivialConstraints.append(A>>0)


    def rowMaker(self):
        s=list(range(self.numParty))
        self.flatOprArray=[tuple(chain.from_iterable(i)) for i in self.bell_array]
        comb=list(chain.from_iterable(combinations(s, r) for r in range(1,len(s)+1)))
        self.row=[()]+[tuple([j]) for i in self.flatOprArray for j in i]
        for i in comb[self.numParty:]:
            self.row+=[k for k in product(*[self.flatOprArray[j] for j in i])]
        self.probStrSet={}
        self.probTupleSet={}
        self.probTupleSet[()]=1
        self.trivialConstraints=[]
        for i in comb:
            j_str="".join([chr(ord('a')+j) for j in i])#abc
            TinputArr=tuple(product(*[tuple(range(len(self.bell_array[j]))) for j in i]))
            for j in TinputArr:
                k_str="".join([str(t) for t in j])
                ToutputArray=tuple(product(*[tuple(range(len(self.bell_array[i[k]][j[k]]))) for k in range(len(j))]))
                Tconstraint=0
                for k in ToutputArray:
                    l_str="".join([str(t) for t in k])
                    finalTuple=tuple(self.bell_array[i[t]][j[t]][k[t]] for t in range(len(k)))
                    finalStr=f"p{j_str}({l_str}|{k_str})"
                    rowVariable=cv.Variable()
                    self.trivialConstraints.append(rowVariable<=1)
                    self.trivialConstraints.append(rowVariable>=0)
                    self.probStrSet[finalStr]=rowVariable
                    self.probTupleSet[finalTuple]=rowVariable
                    Tconstraint+=rowVariable
                self.trivialConstraints.append(Tconstraint==1)




    def __init__(self,oprArray=None,inputs=2,outputs=2):
        self.bell_array=oprArray
        if(type(self.bell_array) is int):
            if(self.bell_array>0):
                self.bell_array=[inputs for i in range(self.bell_array)]
            else:
                raise Exception("error parsing due to negative bell scenario inputs")
        if(type(self.bell_array) is list):
            if(all(isinstance(n, int) for n in self.bell_array)):
                if(all(n>0) for n in self.bell_array):
                    self.bell_array=[[outputs for j in range(i)] for i in self.bell_array]
                else:
                    raise Exception("error parsing due to negative bell scenario inputs")
            elif(all(isinstance(n, list) for n in self.bell_array)):
                if(not (all((j>0) for i in self.bell_array for j in i))):
                    raise Exception("error parsing due to negative bell scenario inputs")
                #for inputs like [[[1,2],4],[5,6]] put some error msg
            else:
                raise Exception("error parsing due to negative bell scenario inputs")
            self.numParty=len(self.bell_array)
        else:
            raise Exception("error in parsing due to incompatible datatype")
        k=0
        for i in range(len(self.bell_array)):
            for j in range(len(self.bell_array[i])):
                l=k+self.bell_array[i][j]
                self.bell_array[i][j]=list(range(k,l))
                k=l
        # print(self.bell_array)
        self.groups=[set(j) for i in self.bell_array for j in i]
        self.rowMaker()
        self.AMaker()
