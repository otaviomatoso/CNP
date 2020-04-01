!start.
!register.

+!register <- .df_register("participant");
              .df_subscribe("initiator").
+!start
  <- .print("Started.").

+hi[source(S)]
  <- .print("Hi received from ", S);
     .print("Sending hi back");
     .send(S,tell,hi);
     .
