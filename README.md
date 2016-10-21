# Concept Systems

**Concept system** is a web application that supports parsing [concept maps](https://en.wikipedia.org/wiki/Concept_map) in particular format and provides immediate feedback.

This project is developed for the subject [INFO3315 Human-Computer Interaction](https://cusp.sydney.edu.au/students/view-unit-page/alpha/INFO3315) at the [University of Sydney](http://sydney.edu.au/).

An [introduction video](https://www.youtube.com/watch?v=3Bv19KaX75Q) is also available on Youtube.

## Authors

 * Jen Liu
 * Chenrui Liu
 * Jason Liu
 * Di Lu
 * Thi Kim Ngan Nguyen
 * Agamjot Virk

## Software dependencies

This application is developed in python 3 with [Django](https://www.djangoproject.com/) web framework and [jinja2](http://jinja.pocoo.org/docs/dev/) html rendering library.

To run the application, you will need to install the dependencies.
details are also available in requirements text documentation.

## Setup

Install Python 3 and all software dependencies from "requirements.txt". Then, you may start a developer server through the manage.py script within the project.

For more information on how to setup and run a Django project, please refer to [django documentation](https://docs.djangoproject.com/en/1.10/).

Alternatively, on Mac OSX and linux, you may execute the quickstart shell script to setup a development server automatically, this script requires Python 3 installed.

## Usage

A [demo](https://www.youtube.com/watch?v=3Bv19KaX75Q) is available on Youtube to give you an idea about the application.

This app requires a .csv document recording a model concept map, which defines a list of available concepts, links, and propositions.
It then requires a .cxl concept map file exported from [Cmaptools](http://cmap.ihmc.us/).
The .csv model map is supposed to be provided by teachers and the .cxl map is supposed to be created by students.
Then you may start the application and upload both files, the application will generated a new page to provide a range of feedback.

A pair of sample .csv and .cxl files are also available under sample maps directory to start with.
