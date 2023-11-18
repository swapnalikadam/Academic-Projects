# Natures Palette
Nature’s Palette: An open-access digital repository of spectral data

## Introduction
Nature’s Palette is a digital repository of spectral data.
This is a prototype of the online repository requested by Dr. Pierre-Paul Bitton.
Githlab URL, https://

#### Required Software
- Node.js, version- 12.x
- MongoDB, version 4.x
- Install R language, version >3.5.
- Open R language command line, and run the following command to install dependencies.
> $ install.packages("pavo") 
<br> $ install.packages("lightr")
> 
#### Installation steps
To run the project locally:
- Clone it.
- Open models.js file and replace the mongoDB mongoose connection string.
- Open command line terminal and change the path to project src folder.
> $ cd src
- Use npm to install dependencies.
> $ npm install
- The main file for the project is app.js.
- To run this file, type the following in the command line terminal.
> $ node server.js
- The project runs at http://localhost:8080/

- Install turf.js using the command 
> npm install @turf/turf
> npm install @turf/boolean-point-in-polygon



License
----

MIT
