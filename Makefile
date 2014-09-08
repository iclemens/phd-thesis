
LATEX_CMD=pdflatex
LATEX_ARGS=-jobname thesis -output-directory build -file-line-error
LATEX_ARGS2=-jobname paper3_main -output-directory build -file-line-error
BIBTEX_CMD=bibtex

all: thesis.pdf	

thesis.pdf:
	cp src/refs.bib src/*_custom.bst build
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex
	cd build; bibtex thesis
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex

paper3_main.pdf:
	$(LATEX_CMD) $(LATEX_ARGS2) src/paper3_main.tex
	cd build; bibtex paper3_main
	$(LATEX_CMD) $(LATEX_ARGS2) src/paper3_main.tex
	$(LATEX_CMD) $(LATEX_ARGS2) src/paper3_main.tex

