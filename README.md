<h1>sentinelscan</h1>
sentinelscan is a Python script that analyses C#.net files for security weaknesses based on the content of the file chsharp.xml. The script can be used to scan a local repository or a remote GitHub repository.

<h2>Features</h2>
- Connects to GitHub and downloads the repository for local analysis
- Reviews C#.net files for security weaknesses
- Outputs findings to console as well as creating a report in txt file for later review
- Supports caching - if a repository has already been downloaded, the program will not download it again and just proceed with the analysis
- Users can add their own rules
- Can be extended to support other programming languages
- 
<h3>Requirements</h3>
- Python 3.6 or higher
- The git command-line tool must be installed

<h3>Usage</h3>
- Clone the repository or download the sentinelscan.py file
- Install the required Python libraries using the command pip install -r requirements.txt
- Run the script using the command python sentinelscan.py <repository-url>

Contributing
Contributions are welcome! To contribute, please fork the repository, create a new branch, make your changes, and submit a pull request. Please make sure your code follows PEP 8 guidelines.

License
This project is licensed under the MIT License. See the LICENSE file for more information.