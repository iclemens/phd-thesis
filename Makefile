
LATEX_CMD=pdflatex
LATEX_ARGS=-jobname thesis -output-directory build -file-line-error
BIBTEX_CM=bibtex

all: thesis.pdf	

thesis.pdf:
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex
	$(LATEX_CMD) $(LATEX_ARGS) src/thesis.tex