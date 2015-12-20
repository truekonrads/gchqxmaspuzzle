#!/usr/bin/env python
from pysmt.shortcuts import *
from pysmt import typing,logics
from generate_runs import generate_vector
from pprint import pprint
from datetime import datetime
import puzzle_spec
import pudb
def rows_and_cols_from_matrix(matrix):
	cols=[]
	for y in xrange(len(matrix)):
		cols.append([row[y] for row in matrix])
	# print cols
	return (matrix,cols)

def get_solver(size,rows,cols,blacks):
	try:
		solver=Solver(logics.QF_LIA)
		# build row and col number vectors
		rowvectors=[[v for v in generate_vector(size,x)] for x in rows]
		# pprint(rowvectors)
		assert len(rowvectors)==len(rows)
		colvectors=[[v for v in generate_vector(size,x)] for x in cols]
		assert len(colvectors)==len(cols)

		var_table = [[FreshSymbol(typing.INT) for _ in xrange(size)] for _ in xrange(size)]
		# pprint (var_table)
		# variables can be either 0 or 1
		can_be_one_or_zero=[]
		for x in var_table:
			for y in x:
				can_be_one_or_zero.append(Or([Equals(y,Int(0)),Equals(y,Int(1))]))
		can_be_one_or_zero=And(*can_be_one_or_zero)

		# Sanity checks - var_table constraints have to be satisfiable
		assert is_sat(can_be_one_or_zero)

		# set up pre-set constraints
		constraints=[]
		if blacks:
			for (x,y) in blacks:
				constraints.append(Equals(var_table[y-1][x-1],Int(1)))
		constraints=And(*constraints)
		assert is_sat(constraints)

		# next, create row and columnt constraint lists

		row_constraints=[]
		for y in xrange(len(rowvectors)):
			one_row_constraint=[]
			# rowvectors[y] = generated vectors for the y-th row (0 indexed)
			for v in rowvectors[y]:	 
				one_vector_constraint=And([					
						Equals(var_table[y][x],Int(v[x]))
					 for x in xrange(len(v))
					 ])
				one_row_constraint.append(one_vector_constraint)
				# i+=1
			row_constraints.append(Or(*one_row_constraint))
		row_constraints=And(*row_constraints)
		assert is_sat(row_constraints)



		col_constraints=[]
		_,symrows=rows_and_cols_from_matrix(var_table)
		# pprint(symrows)
		for x in xrange(len(symrows)):
			one_col_constraint=[]
			for v in colvectors[x]:
				one_vector_constraint=And([Equals(symrows[x][y],Int(v[y])) for y in xrange(len(v))])
				one_col_constraint.append(one_vector_constraint)
			col_constraints.append(Or(*one_col_constraint))
		# pprint (col_constraints)
		col_constraints=And(*col_constraints)
		assert is_sat(col_constraints)
		

		model=get_model(And(
			can_be_one_or_zero,
			constraints,
			row_constraints
			,col_constraints
			))
		# return [model.get_py_values(r).values() for r in var_table]
		results=[]
		for row in var_table:
			results.append([model.get_py_value(sym) for sym in row])
		return results
	except Exception,e:
		pu.db



def print_matrix(matrix):
	print
	for row in matrix:
		print " ".join([str(x) for x in row])

def main():
	t=datetime.now()
	print "Starting at {}".format(t)
	model=get_solver(puzzle_spec.size,puzzle_spec.rows,puzzle_spec.cols,puzzle_spec.constraints)
	if model is not None:
		print_matrix(model)
	else:
		"UNSAT model :("
	print "Done at {}".format(datetime.now()-t)
if __name__ == '__main__':
    main()





				

