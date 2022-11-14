/* The predicate pop is defined such that the goal pop(X, Y) is true if population of country named X is about Y million people */

pop(usa, 203).
pop(india, 548).
pop(china, 800).
pop(brazil, 108).

/* The predicate area is defined such that the goal area(X, Y) is true if the area covered by the country X is about Y million square miles */

area(usa, 3).
area(india, 1).
area(china, 4).
area(brazil, 3).
/* The predicate density is defined such that the goal density(X, Y) is true if the population density of the country X is about Y people/square mile */
density(Country, Density):-
    pop(Country, Population),
    area(Country, Area),
    Density is Population // Area.

/* The predicate male is defined such that the goal male(X) is true if the person named X is male */
male(albert).
male(edward).

/* The predicate female is defined such that the goal female(X) is true if the person named X is female */
female(alice).
female(victoria).

/* The predicate parents is defined such that the goal parents(X, M, F) is true if M and F are the mother and father of person X */
parents(edward, victoria, albert).
parents(alice, victoria, albert).

/* The predicate sister_of is defined such that the goal sister_of(X, Y) is true if person X is sister of person Y */
sister_of(X, Y) :- 
    female(X), 
    parents(X, M, F), 
    parents(Y, M, F),
    \=(X, Y).

/* The predicate owns is defined such that the goal owns(X, book(Y, author(L, F), ISBN)) is true if the person X owns a book named Y written by an author with last name L and first name F and have the isbn number as ISBN */

owns(koushik, book(patherPanchali, author(bandyopadhyay, bibhutibhushan),6758394531)).
owns(nil, book(saratRachanabali, author(chattopadhyay, sarat), 8949589409)).
owns(john, book(wutheringHeights, author(emily, bronte), 6209857376)).

/* The predicate reigns is defined such that the goal reigns(X, Y, Z) is true if the prince named X reigned from year Y to year Z */

reigns(rhodri, 844, 878).
reigns(anarawd, 878, 916).
reigns(hywel_dda, 916, 950).
reigns(lago_ap_idwal, 950, 979).
reigns(hywel_ap_ieuaf, 979, 985).
reigns(cadwallon, 985, 986).
reigns(maredudd, 986, 999).

/* The predicate prince is defined such that the goal prince(X, Y) is true if the prince named X was on throne during year Y */

prince(Prince, Year):-
    reigns(Prince,X,Y),
    Year >= X,
    Year =< Y.