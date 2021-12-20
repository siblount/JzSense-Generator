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

1) Make sure you have Python and pip installed somewhere.
    * Linux:
        ```bash
        sudo apt install python3 python3-pip python3.8-venv
        ```
    * All OS:
        * Install python (includes pip) from [here](https://www.python.org/downloads/)
        
2) Install `venv`.
    ```bash
    pip install venv
    ```
    If not admin:
    ```bash
    pip install venv --user
    ```
    Linux (if you haven't done already):
    ```bash
    sudo apt install python3.8-venv
    ```

3) Git this!
    ```bash
    git clone https://github.com/siblount/JzSense-Generator.git
    ```
4) Create a venv in the repo.
    ```bash
    cd JzSense-Generator
    python3 -m venv venv
    ```
5) Activate the venv script. 
    The location varies depending on OS.
    Windows: `JzSense-Generator/venv/Scripts/`
    Linux: `JzSense-Generator/venv/bin/`
    Mac: *Unknown*<br>
    Example for Linux:
    ```bash
    ~/JzSense-Generator$ source venv/bin/activate
    (venv) ~/JzSense-Generator$
    ```
    Example for Windows (Powershell):
    ```powershell
    PS D:\JzSense-Generator> ./venv/Scripts/Activate.ps1
    (venv) D:\JzSense-Generator>
    ```
    *For PowerShell, (I believe) you have to change your script-execution settings.*
    Example for Windows (Command Prompt):
    ```cmd
    D:\JzSense-Generator> venv/Scripts/activate.bat
    (venv) D:\JzSense-Generator>
    ```

6) Install the dependencies.
    ```bash
    (venv) D:\JzSense-Generator>pip install -r requirements.txt
    ```
    *Note: An error may show up if "bs4" couldn't be installed, this is fine.*

### Points of Interest
`jzsense\scrappers` - `ds4` and `ds3` are where the code for scrapping data off of the website / local drive is located.
`jzsense\js` - where classes such as `JSType` are defined.
`jzsense\converters` - code to convert the dataclasses into a `javascript` format or `typescript` format.
`jzsense\common` - common functions, most of which are for webscrappers.<br>
`pages` - DAZ v3 Documentation located in `daz_v3` and current DAZ documentation webpages downloaded.

### Additonal Information
You may get import errors when attempting to run scripts that aren't in the root directory such as `..\ds4\__init__.py`. Try to run code through the root directory not from a subfolder.

`backup` contains the original code I used to create JzSense.

`find_deleted_objects.py` is used to call DAZ Studio and determine if symbols from v3 documentation still exists.

### Final Regards

I apologize if this is all messed up. I am a student and all of this is new to me, so I'll try my best. So please be nice :).

Oh, license, whatever license that says "don't use this for commercial means, if u do, it has to be free with all the contributors names on it."