//ARDUINO 1.0+ ONLY
#include <Ethernet.h>
#include <SPI.h>


////////////////////////////////////////////////////////////////////////
//CONFIGURE
////////////////////////////////////////////////////////////////////////
byte server[] = { 74, 125, 47, 141 }; //ip Address of the server you will connect to

//The location to go to on the server
//make sure to keep HTTP/1.0 at the end, this is telling it what type of file it is
String location_open = "/rest/status/open";
String location_close = "/rest/status/close";
String host = "Host: garoahc.appspot.com";
String token = "/YOURKEY";

#define SENSOR_PIN 3

IPAddress ip(192, 168, 1, 245);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

// if need to change the MAC address (Very Rare)
byte mac[] = { 0xFA, 0xFE, 0xF1, 0xFA, 0xFE, 0xF1 };
////////////////////////////////////////////////////////////////////////

EthernetClient client;

char inString[32]; // string for incoming serial data
int stringPos = 0; // string index counter
boolean startRead = false; // is reading?

int pinStatus = LOW;
long updateDelay= 600000; //10 Minutes
long lastUpdate=0;


void setup(){
  pinMode(SENSOR_PIN, INPUT);
  digitalWrite(SENSOR_PIN, HIGH);
  pinStatus = digitalRead(SENSOR_PIN);
  
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    Ethernet.begin(mac, ip, gateway, subnet);
  }
  Serial.begin(9600);
  updateStatus();
}

void loop(){
  //Status changed or last change was to long ago.
  if ( (pinStatus != digitalRead(SENSOR_PIN)) || ( (millis()-lastUpdate) >= updateDelay ) ) {
    Serial.println("Updating Status");
    updateStatus();
  }
  delay(100);
}

void updateStatus() {
    pinStatus = digitalRead(SENSOR_PIN);
    lastUpdate = millis();
    String pageValue = connectAndRead(); //connect to the server and read the output
    Serial.println(pageValue); //print out the findings.
}

String connectAndRead(){
  //connect to the server
  Serial.println("connecting...");

  //port 80 is typical of a www page
  if (client.connect(server, 80)) {
    Serial.println("connected");
    client.print("GET ");
    if (pinStatus == HIGH) {
      client.print(location_open);
    } else {
      client.print(location_close);
    }
    client.print(token);
    
    client.println(" HTTP/1.0");
    client.println(host);
    client.println();

    //Connected - Read the page
    return readPage(); //go and read the output

  }else{
    return "connection failed";
  }

}

String readPage(){
  //read the page, and capture & return everything between '<' and '>'

  stringPos = 0;
  memset( &inString, 0, 32 ); //clear inString memory

  while(true){
    if (client.available()) {
      char c = client.read();
      if (c == '<' ) { //'<' is our begining character
        startRead = true; //Ready to start reading the part 
      } else if(startRead) {

        if(c != '>'){ //'>' is our ending character
          inString[stringPos] = c;
          stringPos ++;
        }else{
          //got what we need here! We can disconnect now
          startRead = false;
          client.stop();
          client.flush();
          Serial.println("disconnecting.");
          return inString;
        }

      }
    }

  }

}
