# Komputonomikon

Knjiga o izračunljivosti, specijalno namijenjena računarcima.

## Kako ga proizvesti?

Instalirajte distribuciju TeX live (https://www.tug.org/texlive/acquire-netinstall.html).

    git clone https://github.com/vedgar/izr.git
    cd izr
    mkdir tikzcache
    make
    biber Komputonomikon
    make
    make

Na Linuxu ćete vjerojatno `make` trebati izvršiti kao `./make.bat` (i `chmod u+x make.bat` prvo).

Alternativno: pošaljite mi email (veky@math.hr) ako želite gotovi PDF. :-)
