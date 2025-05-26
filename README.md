# Console Utilities (ConUtils)

Hai :3 

Terminal needs ANSI support! - *duh*

ConUtils is a simple toolkit designed to beautify your console and provide essential utilities for script development.
Currently implemented:

- Spinner
- Text
- Containers
- Console

## to-do:

- Log 
- DynamicTextelements

- implement multi line spinners/animations
- add Frame class for containers
- add Screen and Line Classes as containers

- add update functionality to dynamically adjust screen state after run command

### internal changes:

- compile output string before printing to reduce tearing
- move error classes to seperate folder

## desgtribution

- will be handled by pip ```pip install ConUtils```
- currently on testpypi ```pip install --index-url https://test.pypi.org/simple/ --no-deps conutils```
