// C++ code
//
#include <Keypad.h>
#include <Adafruit_LiquidCrystal.h>
#define SCROLLSPEED 150

const byte ROWS = 4; 
const byte COLS = 4; 

int printedVar = 1;


Adafruit_LiquidCrystal lcd_1(0);

char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'.', '0', '#', 'D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; 
byte colPins[COLS] = {5, 4, 3, 2}; 

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

    enum State{
        gapInput,
        pulseInput,
        blinkMode,
        mainMenu,
        manualMode,
        help
    };

    State state = mainMenu;

// starter is a variable used to track if the scrolling instructions for the state have played yet.
static bool starter = 1;

void cleanUp(){
    lcd_1.clear();
    starter = 1;
}

void scrollText(const char* sent,int length){
  //gives scrolling text to display longer messages
  lcd_1.setCursor(0,0);
  String message = "";
    for(int i=0; i<16; i++){
    message = message + *sent;
    sent ++;
  }
  lcd_1.print(message);
  String newMess=message;
  for(int i=16; i<length; i++){
  	delay(SCROLLSPEED);
    lcd_1.setCursor(0,0);
    newMess=newMess.substring(1)+ *sent;
    sent++;
    lcd_1.print(newMess);
  }
}

void setup(){
  lcd_1.begin(16,2);
  Serial.begin(9600);
  pinMode(10,OUTPUT);
}
  
void loop(){
    //basic set up of variables
    lcd_1.setBacklight(1);
    char customKey = customKeypad.getKey();
    static int mrk = 0;
    //script tracks the user input to the device. Eventually I would like it to track between states.
    static String script = "";
    //These are the starting values for the variable indicating gap between sprays, number of cycles and length of spray respectively.
    static int gap = 3000;
    static int count = 4;
    static int pulse = 500;

    switch (state){

        case gapInput:
            if(starter){
                String text = "Input the number of seconds the sprayer will be off for. Then press #";
                scrollText(text.c_str(),text.length());
                script = "";
                starter = 0;
            }
            if (customKey){
                //A button has been pressed
                if(customKey!='#'){
                    script = script + customKey;
                    lcd_1.setCursor(0,1);
                    lcd_1.print(script);
                }
                else{
                    lcd_1.setCursor(0,1);
                    float newScript = script.toFloat();
                    gap = (int)(newScript*1000);
                    script = "";
                    Serial.println(script);
                    cleanUp();
                    state = mainMenu;
                }
            }
            break;

        case pulseInput:
            if(starter){
                String text = "Input the number of seconds the sprayer will be on for. Then press #";
                scrollText(text.c_str(),text.length());
                script = "";
                starter = 0;
            }
            if (customKey){
                //A button has been pressed
                if(customKey!='#'){
                    script = script + customKey;
                    lcd_1.setCursor(0,1);
                    lcd_1.print(script);
                }
                else{
                    lcd_1.setCursor(0,1);
                    float newScript = script.toFloat();
                    pulse = (int)(newScript*1000);
                    script = "";
                    Serial.println(script);
                    cleanUp();
                    state = mainMenu;
                }
            }
            break;

        case blinkMode:
            for(int x=0;x<count;x++){
                        lcd_1.print("Sprayer on");
                        digitalWrite(10,HIGH);
                        delay(gap);
                        digitalWrite(10,LOW);
                        lcd_1.clear();
                        delay(pulse);
                    }
                mrk = 0;
                starter = 1;
                state = mainMenu;
            break;
        
        case mainMenu:
            if(starter){
                lcd_1.setCursor(0,0);
                lcd_1.print("1gap");
                lcd_1.setCursor(8,0);
                lcd_1.print("2pulse");
                lcd_1.setCursor(0,1);
                lcd_1.print("3run time");
                lcd_1.setCursor(10,1);
                lcd_1.print("4help");
                delay(50);
                starter = 0;
            }

            if(customKey == '1'){
                state = gapInput;
                cleanUp();
            }
            else if(customKey == '2'){
                state = pulseInput;
                cleanUp();
            }
            else if(customKey == '3'){
                state = blinkMode;
                cleanUp();
            }
            else if(customKey == '4'){
                state = help;
                cleanUp();
            }
            else if(customKey == 'A'){
                state = blinkMode;
                cleanUp();
            }
            else if(customKey == 'B'){
                state = mainMenu;
                cleanUp();
            }
            else if(customKey == 'C')
                state = manualMode;
                cleanUp;
            break;

        case manualMode:
            if(starter){
                lcd_1.setCursor(0,0);
                lcd_1.print("Press C to turn on");
                lcd_1.setCursor(0,1);
                lcd_1.print("Press # to return");
                starter = 0;
            }
            if(customKey == 'C'){
                digitalWrite(10,HIGH);
            }
            else if(customKey == '#'){
                digitalWrite(10,LOW);
                state = mainMenu;
                cleanUp();
            }
            else{
                digitalWrite(10,LOW);
            }
            break;

        case help:
            if(starter){
                String Message = "Press any key to return to main menu";
                scrollText(Message.c_str(),Message.length());
                starter = 0;
            }
            if(customKey){
                //Navigate from help menu logic
                cleanUp();
                state = mainMenu;
            }
            break;
        default:
            break;

    }
}