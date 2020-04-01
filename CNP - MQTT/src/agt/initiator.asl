/* Rules */

/*Initial Believes */

/*Initial goals */
!start(1,beer).

/*Plans */
+!start(Id,Service) : .my_name(Me)
	<- .print("Start.");
		 focus(mqtt);
		 .wait(7000);
		 cfp(Id,Me,Service);
		 .wait(4000);
		 !contract;
		 .

+!contract
	<- .findall(offer(Price,Id,Name),proposal(Id,Name,Price),L);
	 	 .print("Offers are = ", L);
		 .min(L,offer(WOf,Id,WAg));
		 .print("Winner is ",WAg," with ",WOf);
		 !announce_result(Id,WAg);
		 .

+!announce_result(Id,WAg)
	<- .print("RESULT");
		 +accept(Id,WAg); // remember result
		 accept(Id,WAg);
		 .
