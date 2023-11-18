# Natures Palette
I integrated the Georeferencing feature into the existing Nature's Palette website, originally developed by a PHD student who conducted research in the same domain. This new functionality enables users, particularly researchers, to access Google Maps directly on the website. It serves as a valuable tool for streamlining studies on various bird species worldwide. The website displays latitude and longitude coordinates of bird species locations as markers on Google Maps.

Users can enhance their search experience by entering specific terms in designated boxes and clicking the "Search with Georeferencing" button. This action displays all relevant markers on the map. For more focused research, researchers can draw polygons on the map, concentrating on specific areas of interest. Markers outside the drawn polygons are then disabled. The tool offers advanced features such as drawing complex polygons, zooming in or out on the Google Map, and creating multiple color-filled polygons to distinguish different areas on the map. These additions significantly enhance the user experience, providing researchers with powerful tools for detailed exploration and analysis within Nature's Palette.

## Introduction
This is a prototype of the online repository requested by Dr. Pierre-Paul Bitton.
URL- https://research.library.mun.ca/14708/1/thesis.pdf

#### Required Software Setup to Run the Project
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
