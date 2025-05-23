#include <Keypad.h>
#include <Adafruit_LiquidCrystal.h>
//Libraries for the hardware


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
  	delay(200);
    lcd_1.setCursor(0,0);
    newMess=newMess.substring(1)+ *sent;
    sent++;
    lcd_1.print(newMess);
  }
}

void setup(){
    //set up sequences here
}

void loop(){
    //function loop(state machine) here
    switch (currentState){
        case 1:
            //Delay time adjustment
            break;
        
        case 2:
            //Spray time adjustment
            break;
        
        case 3:
            //Manual mode
            break;
        
        case 4:
            Instruction mode
            break;
        
        default:
            //Sprinkler running
            break;

    }

}