#include <Arduino.h>
#include <LiquidCrystal.h>

// put function declarations here:

// Initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  // put your setup code here, to run once:

  // Set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  
  // Print a message to the LCD
  lcd.setCursor(0, 0);
  lcd.print("Options Pricer");
  
  lcd.setCursor(0, 1);
  lcd.print("This gon be good");
}

void loop() {
  // put your main code here, to run repeatedly:
  
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}