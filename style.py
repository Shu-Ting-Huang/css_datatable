no_hover="""table {
	table-layout: auto;
	white-space: pre;
}
td, th {
	border: 1px solid black;
}
td {
	text-align: center;
}
th {
	background-color: lime;
	text-align: center;
	z-index: 1;
}
td:first-child, th:first-child {
	position: sticky;
	left: 0;
	z-index: 1;
	background-color: cyan;
	text-align: right;
}
thead tr th {
	position: sticky;
	top: 0;
}
th:first-child {
	z-index: 2;
	background-color: gold;
}"""

hover="""table {
	table-layout: auto;
	white-space: pre;
}
td, th {
	border: 1px solid black;
}
td {
	text-align: center;
	position: relative;
}
th {
	text-align: center;
	background-color: lime;
	z-index: 1;
	position: relative;
}
td:first-child, th:first-child {
	position: sticky;
	left: 0;
	z-index: 1;
	background-color: cyan;
	text-align: right;
}
thead tr th {  
	position: sticky;
	top: 0;
}
th:first-child {
	z-index: 2;
	background-color: gold;
} 
td:hover {
	  background-color: #ff9999;
}
td:hover::before {
	background-color: #ff9999;
	content: '\\00a0';
	height: 100%;
	left: -5000px;
	position: absolute;
	top: 0;
	width: 5000px;
	z-index: -1;
}
td:hover::after {
	background-color: #ff9999;
	content: '\\00a0';  
	height: 5000px;
	left: 0;
	position: absolute;  
	top: -5000px;
	width: 100%;
	z-index: -1;        
}"""
