# Komputonomikon

Knjiga o izračunljivosti, specijalno namijenjena računarcima.

## Kako ga proizvesti?

Instalirajte distribuciju TeX live (https://www.tug.org/texlive/acquire-netinstall.html).

    git clone https://github.com/vedgar/izr.git
    cd izr
    mkdir tikzcache
    pdflatex -shell-escape Komputonomikon
    biber Komputonomikon
    pdflatex Komputonomikon
    pdflatex Komputonomikon

Ako dobijete nekakav `Font Warning`, vjerojatno trebate instalirati paket `texlive-cbfonts`.

Alternativno: pošaljite mi email (veky@math.hr) ako samo želite gotovi PDF. :-)
