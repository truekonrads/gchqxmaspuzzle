#!/usr/bin/env python
from test_solutions import parse_matrix
import puzzle_spec

print """
<html>
<head> 
	<title>
GCHQ x-mas puzzle solution 
</title>
<style type="text/css">
td {
	border: none;
	padding: none;
	min-height: 25px;
	min-width: 25px;
}
table {
	border:none;
	border-spacing: 0px;
}
</style>
</head>
<body>
<table style="border: 1px solid black;">
"""
matrix=parse_matrix(file("answer2.txt","rb").read())

for (y,row) in enumerate(matrix):
	print "<tr>"
	for (x,cell) in enumerate(row):
		if (x+1,y+1) in puzzle_spec.constraints:
			if cell==0:
				color="red;"
			# else:
			# 	color="blue;"
		elif cell==1:
			color="black"
		else:
			color="white";
		print "<td style=\"background-color:{}\">&nbsp;</td>".format(color)
	print "</td>"
print """
</table>
</body>
</html>
"""