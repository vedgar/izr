# Komputonomikon

Knjiga o izračunljivosti, specijalno namijenjena računarcima.

## Kako ga proizvesti?

Instalirajte distribuciju TeX live 2020 (https://www.tug.org/texlive/acquire-netinstall.html).

    git clone https://github.com/vedgar/izr.git
    cd izr
    mkdir -p tikzcache
    rm tikzcache/*
    pdflatex -shell-escape Komputonomikon
    biber Komputonomikon
    pdflatex Komputonomikon
    pdflatex Komputonomikon

Ako dobijete nekakav `Font Warning`, vjerojatno trebate instalirati paket `texlive-cbfonts` i/ili `texlive-bold-extra`.

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

## Što moram učiniti ako želim koristiti odnosno redistribuirati Komputonomikon?

Ništa. Verzija Komputonomikona u ovom repozitoriju je eksplicitno u javnoj domeni, odnosno ne podliježe zaštiti autorskih prava.
Ipak, dobro je da mi se javite kako biste bili u toku što se tiče kasnijih verzija,
jer će one možda biti izdane na tradicionalniji način. Knjiga se redovito ažurira i prilagođava studentima novih generacija,
a svakako je moja intencija da rani korisnici Komputonomikona zauvijek imaju pristup najnovijoj verziji.
(Također, lijepo je znati da je plod mog dugogodišnjeg rada još nekome koristan.:)
