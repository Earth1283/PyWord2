# PyWord2
Reconinuation the old PyWord project but this time with PyQt5 and other external libraries
Still, I am aiming to keep the dependencies to a minimum
## Auto Install & download
Execute the `install.py` file that checks for the dependency and downloads the `main.py` file for you automatically.
It achieves this with the `try` and `except` functions. It accounts for various situations by trying `pip3` and `pip`.

If you do not wish to use the installer, you may download it mannually by following the section below.

## Install dependencies
Run the following command in your terminal to install `PyQt5`
```bash
pip3 install PyQt5
```
try this if `pip3` does not work
```bash
pip install PyQt5
```
## Run the Program
Execute the program with
```bash
python3 /path/to/the/file/main.py
```
or
```bash
python /path/to/the/file/main.py
```
## Highlights
This program currently includes the following features:
1. Basic word processing
2. The creation and editing of `.txt` files. Support for `.rtf` or similar files will be added shortly
3. Light and dark mode support
4. Word counting
5. Coloring text

## Images/screenshots
Below is an example of the Light Mode UI 💡
![Image](https://i.ibb.co/pBcqgZ7B/image.png)

Below is the Dark Mode UI 🌙
![Image](https://i.ibb.co/FLVwJjXS/image.png)
