# Signal generator

*WARNING: Please check the output volume from your device before passing any audio signals to a shaker.*

Use the 'run_test.py' script to execute a test. This will require an installation of Python 3.12.1 or greater. This script enables data collection and excitation. The data logger must return the following data as a comma separated row in the order below:

- Time (ms)
- Acceleration (any units)
- Force (any units)

The units of force and acceleration can be defined in the 'run_test.py' source code.

## Executing a test

Execute the following from the terminal

```cmd
pip install -r requirements.txt
python run_test.py
```

The script will then prompt the user for:
- Test duration (s)
- Sampling frequency (Hz)
- COM port
- Shaker required? (Yes/No)
    If yes:
    - Excitation method
    - Signal amplitude
    - Excitation frequency or frequency range (Hz)

Once these parameters are specified, data collection is initiated and the signal is played through the audio output of the device.