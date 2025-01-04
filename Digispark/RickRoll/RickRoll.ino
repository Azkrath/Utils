#include "DigiKeyboard.h"

void setup() {

}

void loop() {
  DigiKeyboard.sendKeyStroke(0); 
  DigiKeyboard.delay(2000);

  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT); 
  DigiKeyboard.delay(500);
  
  DigiKeyboard.print(F("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=43s")); 
  DigiKeyboard.delay(500);

  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  for(;;){ /*empty*/ }
}