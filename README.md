# Free URL Redirection in Github
This repo provides short URL like feature with Github pages, Google sheets and Google app scripts

# Directory Structure and File descriptions
```````````````````````````````````````
├── GoogleSheetsToJson.gs 	(Google App script to generate JSON from google sheets and provide REST response. Usage direction is inside the file.)
├── index.html 				(Main HTML page for redirection)
├── script.js 				(Gets value from URL and redirects. Otherwise, Shows the complete table from JSON.)
├── GoogleSheetFormat.png	(Sample google sheet format screenshot)
├── sample 					(Template codes to create new course)
```````````````````````````````````````
# Create new course
	1. Copy `course/sample` folder and rename folder name with the course name (Say XXXX)
	3. Find the google sheet at the bottom of `index.html`
	4. `Make a Copy` of the google sheet with the course name
	5. Go to `App script` console of the google sheet, and follow the instructions in the comments to deploy and get the WebApp URL
	6. 
		a. Update the WebApp URL `course/XXXX->script_note.js`
	 	b. Update the URL of the google sheet in `course/XXXX->index.html`
	 	c. Open `webAppURL` from `course/XXXX/script_note.js` in browser and copy the URL in the `jsonURL` field of `course/XXXX/index.html` in Line no. 16
 	7. Add the course XXXX to main page. (i.e. `course->index.html`)