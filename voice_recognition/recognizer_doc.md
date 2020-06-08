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

The recognize method returns the recognized text as an output.