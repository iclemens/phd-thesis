
LATEX_CMD=pdflatex
LATEX_ARGS=-output-directory build -file-line-error
BIBTEX_CMD=bibtex

all: thesis.pdf

%.pdf: src/%.tex
	mkdir -p build
	cp src/refs.bib src/*_custom.bst build
	$(LATEX_CMD) $(LATEX_ARGS) -jobname $(*F) $<
	cd build; bibtex $(*F)
	$(LATEX_CMD) $(LATEX_ARGS) -jobname $(*F) $<
	$(LATEX_CMD) $(LATEX_ARGS) -jobname $(*F) $<

thesis.html:
	python latex2html/main.py intro/intro paper1/paper1 paper3/paper3 paper4/paper4 paper2/paper2 misc/s2_discussion > build/thesis.html

samenvatting.html:
	python latex2html/main.py misc/s3_summary > build/samenvatting.html
