# Alessio M 2023
#
# SentinelScan is a security scanning tool for C# code, designed to help developers identify
# potential security vulnerabilities in their software. The tool works by scanning C# code for specific
# keywords and patterns, which may indicate security weaknesses or code that needs to be further analysed.
#
# https://github.com/CptAlessio/sentinelscan

import os
import re
import datetime
import github
import urllib.parse
import shutil
from xml.etree.ElementTree import parse


def code_scanning(directory):
    # loop files in <directory>
    sourcecode_files_in_project = get_files_in_folder(directory)

    # Output to file
    x = datetime.datetime.now()
    output_file_name = 'codescan' + x.strftime("%f") + '.txt'
    with open(output_file_name, 'a') as output_file:
        output_file.write('Target folder ' + directory + '\n')
        print('Searching in:', len(sourcecode_files_in_project), 'files')
        patternsDetected = []
        listOfFindings = []

        # Parse the XML file
        current_dir = os.getcwd()
        ruleset_path = os.path.join(current_dir, "rules/csharp.xml")
        tree = parse(ruleset_path)
        root = tree.getroot()

        for each_file in sourcecode_files_in_project:
            scan_single_file(each_file, patternsDetected, root)

        patternsDetected = list(dict.fromkeys(patternsDetected))

        print('Security Hotspots:', len(patternsDetected))
        output_file.write('Security Hotspots: ' + str(len(patternsDetected)) + '\n')
        print('----------------------')
        output_file.write('----------------------' + '\n')

        counter = 0
        # Create a dictionary to keep track of which ruleIds have been printed
        printed_ruleids = {}

        for finding in patternsDetected:
            counter = counter + 1

            hotspot_text = finding.strip()
            index = hotspot_text.find("/#/") + len("/#/")
            rule_id = hotspot_text.split("/#/")[0]
            finding_details = extract_finding_details(root, rule_id)
            rule_name, finding_description = finding_details.split("/#/")
            vulnerable_lineofcode = hotspot_text[index:]
            finding = {
                "ruleId": rule_id,
                "name": rule_name,
                "description": finding_description,
                "line_of_code": vulnerable_lineofcode.lstrip()
            }
            # Add finding to collection of Findings
            listOfFindings.append(finding)
            # Loop through the findings and print each one only if the corresponding ruleId has not been printed before
            for finding in listOfFindings:
                rule_id = finding["ruleId"]
                if rule_id not in printed_ruleids:
                    print("\033[33m" + finding["name"] + "\033[0m")
                    print("Found in: \033[32m" + finding["line_of_code"] + "\033[0m")
                    print("Description:", finding["description"])
                    # print("Rule ID:", rule_id)
                    # Print any other fields you want to include
                    print()
                    printed_ruleids[rule_id] = True

            save_findings_to_file(counter, finding_description, output_file, rule_name, vulnerable_lineofcode)


# output finding to a file
def save_findings_to_file(counter, finding_description, output_file, rule_name, vulnerable_lineofcode):
    output_file.write(str(counter) + "] " + rule_name + '\n')
    output_file.write(finding_description + '\n')
    output_file.write(vulnerable_lineofcode.lstrip() + '\n\n\n')


# get name and description of the rule firing
def extract_finding_details(xmlroot, rule_id):
    for rule in xmlroot.findall("./rule[@id='" + rule_id + "']"):
        rule_name = rule.get("name")
        description = rule.find("description").text
        return rule_name + '/#/' + description


# scan file for vulnerabilities
def scan_single_file(filename, allfindings, xmlruleset):
    with open(filename, encoding='utf-8-sig') as file:
        for line in file:
            for rule in xmlruleset.iter("rule"):
                pattern_found = re.search(rule.find("pattern").text, line)
                if pattern_found:
                    allfindings.append(rule.get("id") + "/#/" + line)


# Get list of c# files in directory
def get_files_in_folder(directory):
    r = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".cs"):
                r.append(os.path.join(root, name))
    return r


if __name__ == '__main__':

    # clear console
    os.system('cls' if os.name == 'nt' else 'clear')
    # header
    print("\033[36mSentinelScan v1.0\033[0m")
    # get github repository url
    url = input("Enter GitHub repository URL: ")

    parsed_url = urllib.parse.urlparse(url)
    path_components = parsed_url.path.split('/')

    org_name = path_components[1]
    repo_name = path_components[2]

    output_folder = github.main(org_name, repo_name)
    code_scanning(output_folder)

    # Ask the user if they want to delete the output folder
    delete_folder = input("Do you want to delete the source code or keep it for future use (y/n)")

    if delete_folder.lower() == 'y':
        shutil.rmtree(output_folder)
        print("The folder has been successfully deleted")
