# Komputonomikon

Knjiga o izračunljivosti, specijalno namijenjena računarcima.

## Kako ga proizvesti?

Instalirajte distribuciju TeX live (https://www.tug.org/texlive/acquire-netinstall.html).

    git clone https://github.com/vedgar/izr.git
    cd izr
    mkdir -p tikzcache
    rm tikzcache/*
    pdflatex -shell-escape Komputonomikon
    biber Komputonomikon
    pdflatex Komputonomikon
    pdflatex Komputonomikon

Ako dobijete nekakav `Font Warning`, vjerojatno trebate instalirati paket `texlive-cbfonts`.

Ako samo trebate ažurirati izdanje koje ste već napravili, u većini slučajeva je dovoljno

    cd izr
    git pull
    pdflatex Komputonomikon

Ako su neki dijagrami promijenjeni (sustav bi vas trebao upozoriti na to, ali to nažalost nije sasvim pouzdano) treba još izvršiti

    rm tikzcache/*
    pdflatex -shell-escape Komputonomikon

Ako je literatura promijenjena (također, trebali biste dobiti upozorenje) treba još izvršiti

    biber Komputonomikon
    pdflatex Komputonomikon

Alternativno: pošaljite mi email (veky@math.hr) ako samo želite gotovi PDF zadnje verzije. :-)
