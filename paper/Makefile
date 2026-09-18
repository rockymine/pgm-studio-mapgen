# The paper and the poster. Both are pdflatex; latexmk runs it to a fixed point
# so the table of contents, the cross-references and the bookmarks settle.

LATEXMK := latexmk -pdf -interaction=nonstopmode -halt-on-error

.PHONY: all paper poster clean figures

all: paper poster

paper:
	$(LATEXMK) whitepaper.tex

poster:
	cd poster && $(LATEXMK) poster.tex

clean:
	latexmk -C whitepaper.tex
	cd poster && latexmk -C poster.tex
