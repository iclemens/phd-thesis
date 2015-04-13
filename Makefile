
LATEX_CMD=pdflatex
LATEX_ARGS=-output-directory build -file-line-error
BIBTEX_CMD=bibtex

all: thesis.pdf	paper1.pdf paper2.pdf paper3.pdf paper4.pdf intro.pdf

%.pdf: src/%.tex
	cp src/refs.bib src/*_custom.bst build
	$(LATEX_CMD) $(LATEX_ARGS) -jobname $(*F) $<
	cd build; bibtex $(*F)
	$(LATEX_CMD) $(LATEX_ARGS) -jobname $(*F) $<
	$(LATEX_CMD) $(LATEX_ARGS) -jobname $(*F) $<

thesis.html:
	python latex2html/main.py intro/intro paper1/paper1 paper3/paper3 paper4/paper4 paper2/paper2 misc/s2_discussion > build/thesis.html