#include <Arduino.h>
#include <ssd1306.h>
#include <string.h>

// We have an 128x128 LCD screen.
// We use font size 8x16.
// So we have 16x8 characters.
// Reserve the first and the last character for overflow markers.
// The remaining 126 grids are available for display.
// But we find that the serial communication is very slow.
// So it's better to be a small number, e.g., 30.
#define CAPACITY 30

// // Or if we just want overflow effects...
// #define CAPACITY 8

static void update(char *);
static void display(const char *buf);

void setup()
{
  Serial.begin(115200);
  ssd1306_setFixedFont(ssd1306xled_font8x16);
  st7735_128x160_spi_init(3, 4, 5);  // RES CS DC, SDA=11, SCL=13
  ssd1306_setColor(RGB_COLOR16(255, 255, 255));  // BGR
  ssd1306_clearScreen();
  display("Hello! Welcome!");
}

// This simple solution works.
// No need for interrupt handling.
void loop()
{
  char buf[CAPACITY + 3];
  buf[CAPACITY + 2] = 0;
  if(Serial.available())
  {
    size_t n = Serial.readBytes(buf, CAPACITY + 2);
    if(n == CAPACITY + 2)
      update(buf);
  }
}

void update(char *buf)
{
  if(strchr(".|", buf[0]) && strchr(".|", buf[CAPACITY + 1]))
  {
    buf[0] = buf[0] == '.' ? '.' : ' ';
    buf[CAPACITY + 1] = buf[CAPACITY + 1] == '.' ? '.' : '#';
    display(buf);
  }
}

void display(const char *buf)
{
  ssd1306_setCursor(0, 0);
  ssd1306_print(buf);
}
