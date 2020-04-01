/* Rules */

/*Initial Believes */
i_do(beer).
// proposal(p3,beer,3).
// proposal(python,beer,4).
// proposal(p1,beer,12).
// proposal(p2,beer,2).

/*Initial goals */
!start.

/*Plans */

// +!start
// 	<- .print("Start").

+!start : .my_name(Me) & i_do(S)
	<-
		 focus(mqtt);
		 .print("Registering my credentials to CNP...");
		 .wait(2000);
		 register("participant",Me,S);
		 .

+!start
	<- .findall(offer(Value,Service,Name),proposal(Name,Service,Value),L);
	 	 .print("List = ", L);
		 // .min(L,offer(WAg,Service,WOf)); // sort offers, the first is the best
		 // .print("Winner is ",WAg," with ",WOf);
		 .sort(L,X);
		 .print("Ordered list = ",X);
		 X = [H|T];
		 // .concat(X, [H|T], Result);
		 .print("Head of list = ", H);
		 .print("Tail of list = ", T);

		 .
