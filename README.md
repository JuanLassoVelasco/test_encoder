# test_encoder

A python package for using the AMS AS5048B-EK-AB magnetic encoder. The EncoderAMS class uses the SMBus package to read from i2C addresses
of the encoder and the ast library to parse the bit information into a usable angle output.

## Dependencies

- SMBus package
- ast package (for it's literal_eval method)
- npath package (for it's join method)

## Use

In order to pull data from the encoder, you will need to figure out the i2C addresses that your device alots to each encoder you have connected
to it. You will need this address for the i2cAddress argument when you initialize a new EncoderAMS class for the new encoder you've connected.
This is easy on a raspberry pi as you can simply use the i2cdetect command line tool in the terminal prompt to see what addresses it distributes
to each device, but for other platforms it may be a bit trickier. The addresses will be two digit numbers such as 40 or 43, which you would then set
as a variable in your program in the form `newEncoderAddress = 0x40`.

The extra arguments are board specific addresses that do not change, so you can use the ones found in the example code. The addresses come from the
datasheet for the encoder board.

### Methods

As of now, the EncoderAMS class only has one method, which is the `getAngle()` method.

The method takes no arguments and returns a float which represents the angle (in degrees) read by the encoder associated with the instance of 
the class.


