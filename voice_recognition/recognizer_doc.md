##Recognizer documentation

To use the recognizer an instance is needed. The instance can be created  as followed:

```sh
recognizer = SphinxRecognizer()
```

The constructor can also be passed a parameter called "noise_adjust_duration". This parameter determines the number of 
seconds the recognizer has to wait in order to listen to the environment and recognize the surrounding noise.


```sh
text = recognizer.recognize()
```

The recognize method can be passed a parameter called digit_allowed which is set to "False" by default. If it's set to True, 
in case of recognizing a number in the speech, the number would be in digits format and otherwise it will be in words and 
letters format.