# JzSense Generator
This is the project that webscraps information from DAZ's Documentation website, processes the information, and outputs a file to allow the use of Visual Studio's Intellisense.

The result of this generator's output is: [JzSense](https://github.com/siblount/JzSense) - a javascript file that is used for Intellisense.

## Project Status
Currently, the repository is a mess and the main program *barely* works. It is not at any stage to produce any files as of yet.

### How you can help? 😲

Here are some problems you can help solve:
* The program is very *slowww*.
    * It can take up to 15 minutes to process all of the Objects listed in the documentation.
* Improve parsing data in cases where there are "Attention" or "Example" sections.
    * <font color='red'>Note:</font> It's easier said than done.  
* Help clean up repo.
* Find a way to capture all of the hidden functions not listed in DAZ version 3 and version 4 documentation.
    * The debugger pane for DAZ Studio has a list of all of available symbols - how do we get them all?
* Of course, anything other problems/solutions you find will be very useful and appreciated.

### Setup
If your current operating system is Windows 10, you may ignore this.

1) Make sure you have Python installed somewhere on your OS.
2) 