#!/usr/bin/env python


import unittest
from solve import get_solver, rows_and_cols_from_matrix
from generate_runs import array_to_runs
from pprint import pprint
def parse_matrix(matrixstr):
	matrix=[]
	# y=0
	for row in matrixstr.strip().splitlines():
		matrix.append([int(x) for x in row.split(" ")])
	return matrix

def runs_from_matrix(matrix):
	(rows,cols)=rows_and_cols_from_matrix(matrix)
	row_runs = [array_to_runs(x) for x in rows]
	col_runs = [array_to_runs(x) for x in cols]
	return (row_runs,col_runs)



class TestSolver(unittest.TestCase):

	sample_matrix="""
		1 0 1 0
		1 1 1 0
		0 0 0 1
		1 0 1 1
		"""
	ref_matrix=[
		[1,0,1,0],
		[1,1,1,0],
		[0,0,0,1],
		[1,0,1,1]
		]
	ref_row_runs=[
		[1,1],
		[3],
		[1],
		[1,2]
		]
	ref_col_runs=[
		[2,1],
		[1],
		[2,1],
		[2]
	]


	def test_parse_matrix(self):

		parsed_matrix=parse_matrix(self.sample_matrix)
		self.assertEquals(parsed_matrix,self.ref_matrix)

	def test_runs_from_matrix(self):
		matrix=parse_matrix(self.sample_matrix)
		(row_runs,col_runs)=runs_from_matrix(matrix)
		self.assertEquals(row_runs,self.ref_row_runs)
		self.assertEquals(col_runs,self.ref_col_runs)
	
	def test_simple_solution(self):
	 	matrix=parse_matrix(self.sample_matrix)
		(row_runs,col_runs)=runs_from_matrix(matrix)
		blacks=[
			[1,1],
			[1,2]
		]
		model=get_solver(4,row_runs,col_runs,blacks)
		# print "MATRIX"
		# print matrix
		# print "Solution is: {}".format(model)
		# print "MODEL"
		# print model
		self.assertIsNot(model,None)
		self.assertEquals(matrix,model)
		from solve import print_matrix
		print_matrix(model)
	 	# row_runs=[array_to_runs(x) for x in ref_matrix]
		# col_runs=[array_to_runs(c) for c in []]
		# get_solver(3,)


if __name__ == '__main__':
    unittest.main()