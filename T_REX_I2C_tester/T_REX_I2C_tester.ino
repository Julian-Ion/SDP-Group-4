#include <Wire.h>

#define startbyte 0x0F
#define I2Caddress 0x07

int sv[6]={0,0,0,0,0,0};                 // servo positions: 0 = Not Used
int sd[6]={5,10,-5,-15,20,-20};                      // servo sweep speed/direction
int lmspeed,rmspeed;                                 // left and right motor speed from -255 to +255 (negative value = reverse)
int ldir=5;                                          // how much to change left  motor speed each loop (use for motor testing)
int rdir=5;                                          // how much to change right motor speed each loop (use for motor testing)
byte lmbrake = 0;                                    // left and right motor brake (non zero value = brake)
byte rmbrake = 0;
byte devibrate=50;                                   // time delay after impact to prevent false re-triggering due to chassis vibration
int sensitivity=50;                                  // threshold of acceleration / deceleration required to register as an impact
int lowbat=550;                                      // adjust to suit your battery: 550 = 5.50V
byte i2caddr=7;                                      // default I2C address of T'REX is 7. If this is changed, the T'REX will automatically store new address in EEPROM
byte i2cfreq=0;                                      // I2C clock frequency. Default is 0=100kHz. Set to 1 for 400kHz
const byte numChars = 32;
String receivedChars="255255000200200200200200200";
bool newData = false;
int numbers[2]={0,0};

void setup()
{
  Serial.begin(9600);
  Serial.setTimeout(10);
  while (!Serial) {}
  
  Wire.begin();                                      // no address - join the bus as master
}


void loop()
{
                                                     // send data packet to T'REX controller 
  //delay(50);
  //MasterReceive();                                   // receive data packet from T'REX controller, currently, it will mess with usb
  //delay(50);
  
  
  
  //=================================================== Code to test motors and sweep servos =============================================  
  //lmspeed+=ldir;
  //if(lmspeed>240 or lmspeed<-240) ldir=-ldir;        // increase / decrease left motor speed and direction (negative values = reverse direction)

  if (Serial.available() > 0) {
      receivedChars = Serial.readStringUntil('\n');
      Serial.println(receivedChars);
  }
  /*
  for (int i = 0; i < 2; i+=1) {
    numbers[i] = receivedChars.substring(i*3, (i*3)+3).toInt()-255;
  }
  */
  
  lmspeed = receivedChars.substring(0, 3).toInt()-255;
  rmspeed = receivedChars.substring(3, 6).toInt()-255;

  //lmbrake = byte(receivedChars.substring(6, 9).toInt());
  //rmbrake = byte(receivedChars.substring(6, 9).toInt());

  sv[0] = 1000+10*receivedChars.substring(9, 12).toInt();
  sv[1] = 1000+10*receivedChars.substring(12, 15).toInt();
  sv[2] = 1000+10*receivedChars.substring(15, 18).toInt();
  sv[3] = 1000+10*receivedChars.substring(18, 21).toInt();
  sv[4] = 1000+10*receivedChars.substring(21, 24).toInt();
  sv[5] = 1000+10*receivedChars.substring(24, 27).toInt();

  for(int i = 0; i < 6; i++){
    if(sv[i] == 3000){
      sv[i] = 0;
    }
  }
  
  delay(25);

  //sv[0] = 2000; // 1000 is inward
  //sv[1] = 2000; // 1000 is inward
  //sv[2] = 1000; // 2000 is inward
  //sv[3] = 1000; //1000 is inward
  
  MasterSend(startbyte,2,lmspeed,lmbrake,rmspeed,rmbrake,sv[0],sv[1],sv[2],sv[3],sv[4],sv[5],devibrate,sensitivity,lowbat,i2caddr,i2cfreq);

  //MasterReceive();
  
  //rmspeed+=rdir;
  //if(rmspeed>240 or rmspeed<-240) rdir=-rdir;        // increase / decrease left motor speed and direction (negative values = reverse direction)
 
  
  //lmbrake=0;                        // test left  motor brake 
  //rmbrake=0;                        // test right motor brake 

  // Code for Servos; Currently Defunct
  //for(byte i=0;i<6;i++)                              // sweep servos
  //{
  //  if(sv[i]!=0)                                     // a value of 0 indicates no servo attached
  //  {
  //    sv[i]+=sd[i];                                  // update servo position to create sweeping motion
  //    if(sv[i]>2000 || sv[i]<1000) sd[i]=-sd[i];     // reverse direction of servo if limit reached
  //  }
  //}
}
