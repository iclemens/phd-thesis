
# Read all input text
 # Replace \input{X} by file contents

# Replace \section{X} \label{Y} with <h2 name="Y">X</h2> and store label in table
# Replace \begin{equation}X\label{Y}Z\end{equation} with \[XZ\] and generate number for label Y

# Scan page for:
  # Headings
  # Labels
  # Citations
  
# Number chapters, graphics, equations, and tables
# Sort and resolve citations

# Go through page and emit HTML

import re


baseDirectory = '../'
source = """
	\input{src/intro/intro.tex}"""
	
#	\input{src/paper1/paper1.tex}
	#\input{src/paper2/paper2.tex}
	#\input{src/paper3/paper3.tex}
	#\input{src/paper4/paper4.tex}"""


#
# Load all files and resolve \input
#

def inputFile(match):
	try:
		infile = open(baseDirectory + match.group(1))
	except:
		infile = open(baseDirectory + match.group(1) + ".tex")
	buffer = ""
	for line in infile:
		buffer += line
	
	return resolveInputs(buffer)
	
def resolveInputs(source):
	return re.sub("\\\\input{(.*)}", inputFile, source, flags = re.MULTILINE)


source = resolveInputs(source)


#
# Remove comments
#

source = re.sub("\\\\%", "__PERCENT__", source)
source = re.sub("%(.*?)\n", "", source)
source = re.sub("__PERCENT__", "%", source)


#
# Replace all headings
#

namerefs = dict();

def chapterHTML(match):
	return "<h1>" + match.group(1) + "</h1>"

def sectionHTMLGroup(match):
	namerefs[match.group(2)] = match.group(1)
	return "<h2 name=\"" + match.group(2) + "\">" + match.group(1) + "</h2>"

def sectionHTML(match):
	return "<h2>" + match.group(1) + "</h2>"

def subsectionHTMLGroup(match):
	namerefs[match.group(2)] = match.group(1)
	return "<h3 name=\"" + match.group(2) + "\">" + match.group(1) + "</h3>"

def subsectionHTML(match):
	return "<h3>" + match.group(1) + "</h3>"
	
def subsubsectionHTMLGroup(match):
	namerefs[match.group(2)] = match.group(1)
	return "<h4 name=\"" + match.group(2) + "\">" + match.group(1) + "</h4>"

def subsubsectionHTML(match):
	return "<h4>" + match.group(1) + "</h4>"
	
def resolveChapters(source):
	source = re.sub("\\\\chapter{([^}]*)}", chapterHTML, source, flags = re.MULTILINE)
	source = re.sub("\\\\section{([^}]*)}\s*\\\\label{([^}]*)}", sectionHTMLGroup, source, flags = re.MULTILINE)
	source = re.sub("\\\\section{([^}]*)}", sectionHTML, source, flags = re.MULTILINE)
	
	source = re.sub("\\\\subsection{([^}]*)}\s*\\\\label{([^}]*)}", subsectionHTMLGroup, source, flags = re.MULTILINE)
	source = re.sub("\\\\subsection{([^}]*)}", subsectionHTML, source, flags = re.MULTILINE)

	source = re.sub("\\\\subsubsection{([^}]*)}\s*\\\\label{([^}]*)}", subsubsectionHTMLGroup, source, flags = re.MULTILINE)
	source = re.sub("\\\\subsubsection{([^}]*)}", subsubsectionHTML, source, flags = re.MULTILINE)
	
	return source
	
source = resolveChapters(source)


#
# Replace equations
#

eqns = dict()
eqnc = [0]

def equationHTML(match):	
	tmp = re.search("\\\\label{(.*?)}", match.group(1))
	
	if tmp is None:
		label = "No label"
	else:
		label = tmp.group(1)
	
	eqnc[0] = eqnc[0] + 1 
	eqns[label] = str(eqnc[0])
	
	equation = re.sub("\\\\label{(.*?)}", "", match.group(1))
	#return "\[" + equation + "\]<p><b>Equation " + str(eqnc[0]) + "</b></p>"
	return "<p style='font-weight: bold'>Equation " + str(eqnc[0]) + " about here</p>"
	

def resolveEquations(source):
	source = re.sub("\\\\begin{equation}([\s\S]*?)\\\\end{equation}", equationHTML, source, flags = re.MULTILINE)
	return source

	
source = resolveEquations(source)


#
# Replace figures
#

figs = dict()
figc = [0]

def figureHTML(match):
	tmp = re.search("\\\\label{(.*?)}", match.group(1))
	
	if tmp is None:
		label = "No label"
	else:
		label = tmp.group(1)
	
	figc[0] = figc[0] + 1 
	figs[label] = str(figc[0])
	
	return "<p style='font-weight: bold'>Figure " + str(figc[0]) + " about here</p>"

def resolveFigures(source):
	source = re.sub("\\\\begin{figure}([\s\S]*?)\\\\end{figure}", figureHTML, source, flags = re.MULTILINE)
	return source

source = resolveFigures(source)


#
# Replace figures
#

tabs = dict()
tabc = [0]

def tableHTML(match):
	tmp = re.search("\\\\label{(.*?)}", match.group(1))
	
	if tmp is None:
		label = "No label"
	else:
		label = tmp.group(1)
	
	tabc[0] = tabc[0] + 1 
	tabs[label] = str(tabc[0])
	
	return "<p style='font-weight: bold'>Table " + str(tabc[0]) + " about here</p>"

def resolveTables(source):
	source = re.sub("\\\\begin{table}([\s\S]*?)\\\\end{table}", tableHTML, source, flags = re.MULTILINE)
	return source

source = resolveTables(source)


#
# Replace name references
#

def nameRefHTML(match):
	if not match.group(1) in namerefs:
		return "<a href=\"#\">Undefined section label</a>"
	return "<a href=\"#" + match.group(1) + "\">" + namerefs[match.group(1)] + "</a>"

def eqnRefHTML(match):
	if not match.group(1) in eqns:
		return "<a href=\"#\">Undefined equation label</a>"
	return "<a href=\"#" + match.group(1) + "\">Equation " + eqns[match.group(1)] + "</a>"	

def figRefHTML(match):
	if not match.group(1) in figs:
		return "<a href=\"#\">Undefined figure label</a>"
	return "<a href=\"#" + match.group(1) + "\">Figure " + figs[match.group(1)] + "</a>"	

def tabRefHTML(match):
	if not match.group(1) in tabs:
		return "<a href=\"#\">Undefined table label</a>"
	return "<a href=\"#" + match.group(1) + "\">Table " + tabs[match.group(1)] + "</a>"	

	
def resolveRefs(source):
	source = re.sub("\\\\nameref{([^}]*?)}", nameRefHTML, source, flags = re.MULTILINE)
	source = re.sub("\\\\eqnref{([^}]*?)}", eqnRefHTML, source, flags = re.MULTILINE)
	source = re.sub("\\\\figref{([^}]*?)}", figRefHTML, source, flags = re.MULTILINE)
	source = re.sub("\\\\tabref{([^}]*?)}", tabRefHTML, source, flags = re.MULTILINE)
	return source

source = resolveRefs(source)



title = ""

print """
			<!DOCTYPE html>
			<html>
				<head>
					<title>""" + title + """</title>
	
					<meta charset="utf8" />
						
					<script type="text/x-mathjax-config">
					</script>
					<style>
						body {
							font-family: calibri
						}
					</style>
				</head>
			<body>"""

for line in source.split("\n"):
	line = line.strip()
	
	if len(line) == 0:
		continue
	c = line[0]
	if c == "&" or c == "\\" or c == "<":
		print line
	else:
		print "<p>" + line + "</p>"

print "</body></html>"