import org.apache.camel.Exchange;
import org.apache.camel.Processor;

public class Register implements Processor {

	@Override
	public void process(Exchange exchange) throws Exception {
		String jsonMsg = "";
		String type = exchange.getProperty("Type").toString().replaceAll("\"","");
		String name = exchange.getProperty("Name").toString().replaceAll("\"","");

		if(type.equals("participant")) {
			String service = exchange.getProperty("Service").toString().replaceAll("\"","");
			jsonMsg = "{\"Type\": \"" + type + "\", \"Name\": \"" + name + "\", \"Service\": \"" + service + "\"}";
		}
		else {
			String id = exchange.getProperty("Id").toString().replaceAll("\"","");
			if(type.equals("cfp")) {
				String service = exchange.getProperty("Service").toString().replaceAll("\"","");
				jsonMsg = "{\"Type\": \"" + type + "\", \"Id\": \"" + id + "\", \"Name\": \"" + name + "\", \"Service\": \"" + service + "\"}";
			}
			else if(type.equals("proposal")) {
				// String id = exchange.getProperty("Id").toString().replaceAll("\"","");
				String price = exchange.getProperty("Price").toString().replaceAll("\"","");
				jsonMsg = "{\"Type\": \"" + type + "\", \"Id\": \"" + id + "\", \"Name\": \"" + name + "\", \"Price\": \"" + price + "\"}";
			}
			else if(type.equals("accept")) {
				// String id = exchange.getProperty("Id").toString().replaceAll("\"","");
				jsonMsg = "{\"Type\": \"" + type + "\", \"Id\": \"" + id + "\", \"Name\": \"" + name + "\"}";
			}
		}
		// System.out.println("\nJSON MSG = " + jsonMsg + "\n");
		exchange.getIn().setBody(jsonMsg);
  }
}
