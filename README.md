<h1>sentinelscan</h1>
sentinelscan is a Python script that scans C#.net files for security weaknesses in GitHub repositories.

<h2>Features</h2> 

+ Connects to GitHub and downloads the repository for local analysis
+ Reviews C#.net files for security weaknesses
+ Outputs findings to console as well as creating a report in txt file for later review 
+ Supports caching - if a repository has already been downloaded, the program will not download it again and just proceed with the analysis 
+ Users can add their own rules (see ```/rules/csharp.xml```)
+ Can be extended to support other programming languages

<h3>Requirements</h3>

+ GitHub personal access token to access public/private repositories inside ```access_token.txt```
+ Python 3.6 or higher 
+ requests

<h3>Usage</h3>

+ Clone the repository or download the sentinelscan.py file
+ Install the required Python libraries using the command ```pip install -r requirements.txt```
+ Run the script using the command ```python sentinelscan.py <repository-url>```