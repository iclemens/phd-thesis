
LATEX_CMD=pdflatex
LATEX_ARGS=-jobname thesis -output-directory build -file-line-error
BIBTEX_CMD=bibtex

all: thesis.pdf	

thesis.pdf:
	cp src/refs.bib src/plain_custom.bst build
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex
	cd build; bibtex thesis
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex