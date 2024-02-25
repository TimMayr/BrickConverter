# LDrawSTLConvert

## Introduction
LDrawSTLConvert is a versatile program designed to facilitate the conversion of LEGO bricks to
STL files using [LDView](https://tcobbs.github.io/ldview/) and the [LDraw Parts Library](https://www.ldraw.org). Without
those amazing Resources, this would not have been possible. It
offers convenient features for generating all the parts of a LEGO sets in STL format, extracting individual parts, and
handling part lists exported from Stud.io.

## Features

* LEGO Set Conversion: Easily convert all parts of a LEGO set to STL files for 3D printing or visualization.
* Individual Part Extraction: Convert specific parts one at a time, allowing for focused printing or modification.
* Support for Stud.io Part Lists: Seamlessly import part lists exported from Stud.io into the conversion process.

## Usage

Install Dependencies:

* [Python 3.12](https://www.python.org/downloads/release/python-3122/)
* [LDraw AIO-Installer](https://www.ldraw.org/article/104.html#:~:text=Automated%20installation%20(Recommended))
* colorama (pip install colorama)
* requests (pip install requests)

## Also Needed

This program gathers its data using [Rebrickable](https://rebrickable.com/home/). To use it you will need to create a
Rebrickable Account, and generate an [API Key](https://rebrickable.com/api/).

## Run the Program:

Execute the main.py in the command line using python.

## Some Notes

* After creating the STL files, be sure to check their size, if it is relevant for your use case. Sometimes they are
  scaled incorrectly, and I haven't figured out why yet (Mostly you just need to multiply/divide the dimensions by 10).
* Some parts do not have LDraw models, and therefore can not be converted. In that case, search for an interchangeable
  part on Bricklink or anywhere else, and convert it separately
* If you are intending to 3D print the generated files, take care to look at their gcode, as Cura sometimes removes
  parts of the studs when printing the bricks standing on their sides. To avoid this rotate them to lie flat on the bed.

## Contribution Guidelines

Contributions to LDrawSTLConvert are welcome! Please follow the established contribution guidelines and coding
standards.
Fork the repository, make your changes, and submit a pull request for review and integration.
I am also taking suggestions for a new name, since I don't like the current one

## Further Notes

It's crucial for users of LDrawSTLConvert to adhere to LEGO's trademark and copyright policies when utilizing the
software for creating LEGO-related content. LEGO's trademarks and copyrights protect their brand and designs, ensuring
the integrity and authenticity of their products.

Here are some key points to consider:

* Respect LEGO's Intellectual Property: LEGO sets and designs are protected by intellectual property laws, including
  trademarks and copyrights. Users should respect these rights and avoid infringing on LEGO's intellectual property when
  using LDrawSTLConvert.

* Personal Use Only: LDrawSTLConvert should be used for personal, non-commercial purposes only, unless explicitly
  authorized by LEGO. Users should not use the software to create and distribute LEGO-related content for commercial
  gain without proper licensing or permission from LEGO.

* Attribution and Recognition: When sharing or showcasing LEGO-related content created using LDrawSTLConvert, users
  should provide appropriate attribution to LEGO for the original designs and acknowledge LEGO's ownership of the
  intellectual property.

* Follow LEGO's Guidelines: LEGO provides guidelines and policies for using their trademarks and copyrights. Users
  should familiarize themselves with these guidelines and ensure compliance when creating LEGO-related content with
  LDrawSTLConvert.

* Be Creative and Respectful: While LDrawSTLConvert enables users to create custom LEGO designs and models, it's
  essential to be creative while respecting LEGO's brand identity and design principles. Users should avoid creating
  content that may misrepresent or tarnish the LEGO brand.

By adhering to LEGO's trademark and copyright policies, users can contribute to a respectful and supportive community
while enjoying the creative possibilities offered by LDrawSTLConvert.