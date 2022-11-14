store(best_smoothies, [alan, john, mary],
      [ smoothie(berry, [orange, blueberry, strawberry], 2),
        smoothie(tropical, [orange, banana, mango, guava], 3),
        smoothie(blue, [banana, blueberry], 3) ]).

store(all_smoothies, [keith,mary],
      [ smoothie(pinacolada, [orange, pineapple, coconut], 2),
        smoothie(green, [orange, banana, kiwi], 5),
        smoothie(purple, [orange, blueberry, strawberry], 2),
        smoothie(smooth, [orange, banana, mango], 1) ]).

store(smoothies_galore, [heath,john,michelle],
      [ smoothie(combo1, [strawberry, orange, banana], 2),
        smoothie(combo2, [banana, orange], 5),
        smoothie(combo3, [orange, peach, banana], 2),
        smoothie(combo4, [guava, mango, papaya, orange],1),
        smoothie(combo5, [grapefruit, banana, pear],1) ]).

/* Used in Question 2 and 5 */
inSmoothieList(Element, [smoothie(Element, _, _)|_]).
inSmoothieList(Element, [_|Tail]):- 
    inSmoothieList(Element, Tail).

/* Used in Question 1, 3 and 4 */
count([], 0).
count([_|Tail], NumberOfElements):-
    count(Tail, X),
    NumberOfElements is X+1.


/*Question 1 : more_than_four(X) is true if store X has four or more smoothies on its menu. */
more_than_four(StoreName):-
    store(StoreName, _, SmoothieList),
    count(SmoothieList, NumberOfSmoothies),
    NumberOfSmoothies >= 4.

/*Question2 : exists(X) is true if there is a store that sells a smoothie named X. */
exists(SmoothieName):- 
    store(_, _, ListOfSmoothies),
    inSmoothieList(SmoothieName, ListOfSmoothies).

/*Question3 : ratio(X, R) is true if there is a store named X that has a ratio R, of the store's number of employees to the store's number of smoothies on the menu*/
ratio(StoreName, Ratio):- 
    store(StoreName, EmployeeList, SmoothieList),
    count(EmployeeList, NumberOfEmployees),
    count(SmoothieList, NumberOfSmoothies),
    Ratio is NumberOfEmployees/NumberOfSmoothies.

/*Question4 : average(X, A) is true if there is a store named X with A as the average price of the smoothies on the store's menu*/
totalPrice([], 0).
totalPrice([smoothie(_, _, Price)|T], TotalPrice):- 
    totalPrice(T, X),
    TotalPrice is X+Price.

average(StoreName, AveragePriceOfSmoothies):- 
    store(StoreName, _, SmoothieList), 
    totalPrice(SmoothieList, TotalPrice),
    count(SmoothieList, NumberOfSmoothies),
    AveragePriceOfSmoothies is TotalPrice/NumberOfSmoothies.

/*question5 : smoothies_in_store(X, L) is true if L is the list of smoothie names that are present on the menu of a store named X.*/
/*app([], _).
app([smoothie(Y,_,_)| S], [Y | S2]) :- app(S, S2).*/
accCp([],[]).
accCp([smoothie(SmoothieName, _,_)|T1],[SmoothieName|T2]) :- accCp(T1,T2).

copy(Source,Destination) :- accCp(Source,Destination).

inListOfSmothies([], _).
inListOfSmothies([SmoothieName|Tail], ListOfSmoothies):-
    inSmoothieList(SmoothieName, ListOfSmoothies),
    membersOfSmoothieList(Tail, ListOfSmoothies).

membersOfSmoothieList(ListOfSmoothieNames, ListOfSmoothies) :-
    var(ListOfSmoothieNames)->
        copy(ListOfSmoothies,ListOfSmoothieNames);% if ListOfSmoothieNames is a free variable (uninstantiated) then copy the smoothie names to it
    inListOfSmothies(ListOfSmoothieNames, ListOfSmoothies).% elss check the names in the list to see if they are in the menu of the store 
        

smoothies_in_store(StoreName, ListOfSmoothieNames):-
    store(StoreName, _, ListOfSmoothies),
    membersOfSmoothieList(ListOfSmoothieNames, ListOfSmoothies).


/*question6 : fruit_in_all_smoothies(X, F) is true if there is a fruit F that is an ingredient of all smoothies on the menu of store X. */

inFruitList(Fruit, [Fruit|_]).
inFruitList(Fruit, [_|Tail]):- inFruitList(Fruit,Tail).

fruitInAllSmoothies(_, []).
fruitInAllSmoothies(Fruit, [smoothie(_,ListOfFruits,_)|Tail]):-
    inFruitList(Fruit, ListOfFruits),
    fruitInAllSmoothies(Fruit, Tail).

fruit_in_all_smoothies(StoreName, Fruit):-
    store(StoreName, _, ListOfSmoothies),
    fruitInAllSmoothies(Fruit, ListOfSmoothies).