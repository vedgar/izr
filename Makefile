all:
	mkdir -p tikzcache
	pdflatex -shell-escape Komputonomikon
	biber Komputonomikon
	pdflatex Komputonomikon
	pdflatex Komputonomikon

