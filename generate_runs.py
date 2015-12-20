import unittest
from  copy import copy
import pudb
from pprint import pprint
import itertools


def generate_vector(size,runs,index=-1):
    res=[x for x in _generate_vector(size,runs)]
    res.sort()
    res=list([res for res,_ in itertools.groupby(res)])
    return res
    # pprint (res)
    # return iter(set(res))

def _generate_vector(size,runs,index=-1):
    # results=[]
    # pu.db
    #print "[DD] Index: {}/Size: {} ".format(index,size)
    if index==-1:    # first run, we don't need to add one member from runs
                # pu.db
        if len(runs)==1:
            # return
            # start_results=[1 for _ in xrange(0,runs[index])]
            start_results=[0 for _ in xrange(size-runs[0])]
            start_results.extend([1 for _ in xrange(0,runs[0])])
            yield start_results

            start_results=[1 for _ in xrange(0,runs[0])]
            start_results.extend([0 for _ in xrange(size-runs[0])])
            yield start_results
            # raise StopIteration
        spaces_to_play_with=calculate_available_spaces(size,runs)
        # pu.db
        if spaces_to_play_with>0:
            # print "[DD] Spaces to play with : {}".format(spaces_to_play_with)
            for i in xrange(0,spaces_to_play_with+1):
                tmpresults=[]
                tmpresults.extend([0 for _ in xrange(0,i)])    # add spacers as zeroes
                remaining_size=size-len(tmpresults)
                for j in _generate_vector(remaining_size,runs,index+1):
                    yield_results=copy(tmpresults)
                    yield_results.extend(j)
                    #print "[DD] RESULTS: {}".format(yield_results)
                    yield yield_results
        else:
            for j in _generate_vector(size,runs,index+1):
                yield j

    elif (index>=0) and (index<len(runs)-1): # middle elements
        # add 1s for the length of the current run               
        start_results=[1 for _ in xrange(0,runs[index])]

        
        #add a zero as a mandatory spacer for the element
        start_results.append(0)
        size_of_unconsumed_array=size-len(start_results)
        spaces_to_play_with=calculate_available_spaces(size,runs[index:])+1
        for i in xrange(0,spaces_to_play_with):
            tmpresults=copy(start_results)
            tmpresults.extend([0 for _ in xrange(0,i)])    # add spacers as zeroes
            remaining_size=size-len(tmpresults)
            # print "TMPRESULTS {}".format(tmpresults)
            for j in _generate_vector(remaining_size,runs,index+1):
                yield_results=copy(tmpresults)
                yield_results.extend(j)
                yield yield_results
        
        #if index==len(runs)-2: # case before last, we chop off the zero at the end
            #start_results=[1 for _ in xrange(0,runs[index])]
            
        if spaces_to_play_with==0 and index==len(runs)-1:
            tmpresults=copy(start_results)
            remaining_size=size-len(tmpresults)
            yield _generate_vector(remaining_size,runs,index+1)

    else: # last element, index=len(runs)-1
        #print "LAST SIZE: {}".format(size)
        end_results=[1 for _ in xrange(0,runs[index])]
        # spaces_to_play_with=calculate_available_spaces(size-len(end_results),runs[index:],end_results)
        # pu.db
        spaces_to_play_with=size-len(end_results)
        end_results.extend([0 for _ in xrange(0,spaces_to_play_with)])
        # print "END RESULTS: {}; spaces: {}".format(end_results,spaces_to_play_with)
        yield end_results
        # for i in xrange(0,spaces_to_play_with):
        #     yield_results=copy(end_results)
        #     yield yield_results.extend([0 for _ in xrange(0,i)])

def calculate_available_spaces(size,runs,existing_array=[]):
    spaces=size-len(existing_array)-sum(runs)-len(runs)+1
    return spaces

def array_to_runs(array):
    runs=[]
    i=0
    array=array[array.index(1):] # chop first zeroes
    # len(array) - array[::-1].index(array)
    array=array[:len(array) - array[::-1].index(1)] # chop last zeroes
    for k in xrange(0,len(array)):

        j=array[k]
        # print "J: {} I: {}".format(j,i)
        if j==1:
            i+=1
            continue
        if j==0 and i!=0:                
            runs.append(i)
            i=0
    runs.append(i)
    return runs


class TestVectorGeneration(unittest.TestCase):

    def test_arrays_to_runs(self):
        ref_run=[1,2,2]
        ref_size=10
        ref_vectors=(
            [1, 0, 1, 1, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [1, 0, 0, 1, 1, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 1, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 1, 0, 1, 1, 0],
            [1, 0, 0, 0, 1, 1, 0, 0, 1, 1],
            [1, 0, 0, 0, 0, 1, 1, 0, 1, 1],
            [0, 1, 0, 1, 1, 0, 1, 1, 0, 0],
            [0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 0, 1, 1, 0, 1, 1, 0],
            [0, 1, 0, 0, 1, 1, 0, 0, 1, 1],
            [0, 1, 0, 0, 0, 1, 1, 0, 1, 1],
            [0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 1, 1, 0, 1, 1]
            )
        # vectors=[x for x in generate_vector(ref_size,ref_array)]
        for v in ref_vectors:
            self.assertEquals(array_to_runs(v),ref_run)


    # def test_arrays_to_runs2(self):
    #     ref_run=[1,2]
    #     ref_size=4
    #     ref_vectors=[
    #         [1,0,1,1]
    #         ]
    #     # vectors=[x for x in generate_vector(ref_size,ref_array)]
    #     for v in ref_vectors:
    #         # print v
    #         self.assertEquals(array_to_runs(v),ref_run)

    def test_calculate_spaces(self):
        ref_array=[1,2,3,3,1]
        ref_size=25
        #25 size, with 10 covered squares in 5 runs should give us 15 spaces
        self.assertEquals(calculate_available_spaces(ref_size,ref_array),11)
        # 25 size, with one element filled in + a spacer
        existing_array=[1,0]
        self.assertEquals(calculate_available_spaces(ref_size,ref_array[1:],existing_array),11)
        existing_array=[1,0,0,0,0,1,1]
        self.assertEquals(calculate_available_spaces(ref_size,ref_array[2:],existing_array),9)

        ref_array=[1,2,2]
        ref_size=10

        self.assertEquals(calculate_available_spaces(ref_size,ref_array),3)
        self.assertEquals(calculate_available_spaces(ref_size-6,ref_array[2:]),2)




    def test_vector_generated_correctly(self):
        ref_array=[1,2,2]
        ref_size=10
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        # print vectors[0]
        # print len(vectors)
        for v in vectors:
            self.assertEquals(len(v),ref_size) # must be the size as defined  
            self.assertEquals(array_to_runs(v),ref_array)
            # vstr="".join([str(x) for x in v])
            # vstr.strip("0")
            # reconstructed_array=[int(x) for x in filter(lambda x: x!='',vstr.split("0"))]
            # self.assertEquals(reconstructed_array,ref_array)
        # print "\n".join([str(x) for x in vectors])

    def test_vector_generated_correctly2(self):
        ref_size=25
        ref_array=[1,3,1,5,2,1,3,1]
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        for v in vectors:
                self.assertEquals(len(v),ref_size) # must be the size as defined  
                self.assertEquals(array_to_runs(v),ref_array)
        # print "\n".join([str(x) for x in vectors])
        # print len(vectors)

    def test_vector_generated_correctly3(self): 
        ref_size=4
        ref_array=[1,2]
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        self.assertTrue(len(vectors)>0,"Vector list can't be empty!")
        for v in vectors:
                self.assertEquals(len(v),ref_size) # must be the size as defined  
                self.assertEquals(array_to_runs(v),ref_array)

    def test_vector_generated_correctly4(self): 
        ref_size=4
        ref_array=[1]
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        self.assertTrue(len(vectors)>0,"Vector list can't be empty!")
        # pprint(vectors)
        self.assertTrue([0, 0, 0, 1] in vectors,"No zero-padding to the end vector found :(")


        ref_array=[2]
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        self.assertTrue(len(vectors)>0,"Vector list can't be empty!")
        # pprint(vectors)
        self.assertTrue([0, 0, 1, 1] in vectors,"No zero-padding to the end vector found :(")


        ref_array=[3]
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        self.assertTrue(len(vectors)>0,"Vector list can't be empty!")
        # pprint(vectors)
        self.assertTrue([0, 1, 1, 1] in vectors,"No zero-padding to the end vector found :(")
    
    def test_vector_generated_correctly5(self): 
        ref_array=[1,1]
        ref_size=4
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        self.assertTrue(len(vectors)>0,"Vector list can't be empty!")
        # pprint(vectors)
        self.assertTrue([0, 1, 0, 1] in vectors,"No zero-padding to the end vector found :(")

    def test_vector_generated_correctly6(self): 
        ref_array=[3]
        ref_size=4
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        self.assertTrue(len(vectors)>0,"Vector list can't be empty!")
        # pprint(vectors)
        self.assertTrue([1, 1, 1,0] in vectors,"No zero-padding to the end vector found :(")
        
    def test_vector_generated_correctly7(self): 
        ref_array=[1,1]
        ref_size=4
        vectors=[x for x in generate_vector(ref_size,ref_array)]
        self.assertTrue(len(vectors)>0,"Vector list can't be empty!")
        # pprint(vectors)
        self.assertTrue([1, 0, 0,1] in vectors,"No zero-padding to the end vector found :(")




if __name__ == '__main__':
    unittest.main()