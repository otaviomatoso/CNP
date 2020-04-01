import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import org.json.JSONObject;

public class Body2Literal implements Processor {

	@Override
	public void process(Exchange exchange) throws Exception {
		String literal = "";
		String body = exchange.getIn().getBody(String.class);
		JSONObject json = new JSONObject(body);

		String type = json.getString("Type");
		String name = json.getString("Name");

		if(type.equals("participant")){
			String service = json.getString("Service");
			literal = type + "(" + name + "," + service + ")";
		}
		else{
			String id = json.getString("Id");
			if(type.equals("cfp")){
				String service = json.getString("Service");
				literal = type + "(" + id + "," + name + "," + service + ")";
			}
			else if(type.equals("proposal")){
				String price = json.getString("Price");
				literal = type + "(" + id + "," + name + "," + price + ")";
			}
			else if(type.equals("accept")){
				literal = type + "(" + id + "," + name +")";
			}

		}
		System.out.println("\nliteral = " + literal + "\n");
		exchange.getIn().setBody(literal);
  }
}
