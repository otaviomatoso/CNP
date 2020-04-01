price(My_job,X) :- .random(R) & S = (20*R) & X = math.round(S) & my_service(My_job).

/*Initial Believes */
my_service(beer).

/*Initial goals */
!start.
// !make_marketing.

/*Plans */
+!start : .my_name(Me) & my_service(S)
	<- .print("My name is ", Me, " and I have ", S, " to offer");
		 focus(mqtt);
		 .wait(2000);
		 .print("Registering my credentials to CNP...");
		 register(Me,S);
		 .

+cfp(Id,Name,Service) : .my_name(Me) & price(Service,Offer)
	<- .print("CFP received by agent ", Name, ", looking for ", Service);
		 .print("Sending a proposal...");
		 +proposal(Id,Service,Offer); // remember my proposal
		 propose(Id, Me, Offer);
		 .

+accept(Id,Name) : .my_name(Me) & Name==Me
	<- .print("My proposal Won CNP with ID = ", Id);
		 .

+accept(Id,Name) : .my_name(Me) & Name\==Me
	<- .print("I lost CNP with ID = ", Id);
		 .
