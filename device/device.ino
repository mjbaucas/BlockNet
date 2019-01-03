#include <AESLib.h>

void setup()
{
  Serial.begin(9600);
  uint8_t * key = (unsigned char *) "Dev00001Dev00001";
  char data[] = "0123456789012345"; //16 chars == 16 bytes
  uint8_t * iv = (unsigned char *) "Dev00001Dev00001";
  aes128_cbc_enc(key, iv, data, 16);
  Serial.print("encrypted:");
  Serial.println(data);
  aes128_cbc_dec(key, iv, data, 16);
  Serial.print("decrypted:");
  Serial.println(data);
}

void loop()
{
  
}

