# Last updated 22.11.2022 / Aleksi Postari

import os
import zipfile
import json

requiredFiles : list = []
requiredLines : list = []
generateHTMLReport : bool = True

try:
  with open('grader_settings.json') as json_file:
    # Remove comments from the json file
    lines = json_file.readlines()
    lines = [line for line in lines if not "//" in line]
    data = json.loads("".join(lines))
    #print(data["requiredFiles"])
    requiredFiles = data['requiredFiles']
    requiredLines = data['requiredLines']
    generateHTMLReport = data["generateHTMLReport"]
except Exception as e:
  print("Error opening grader_settings.json file:")
  print(e)
  os._exit(0)

htmlOutput = '''
  <html>
    <style>
      table.success { color: green; }
      body { background: #1B0E37; color: white; }
      .title-success { color: #72e965; }
      .title-fail { color: #ff417d; }
      h1 { margin-top: 50px; }
      body { max-width: 1200px; margin: 0 auto; }
      table { width: 100% !important; }
      table td { padding-bottom: 60px; }
      table tr { border-bottom: 1px solid rgb(77 45 113); padding: 15px; border-radius: 4px; vertical-align: top; }
      table th { text-align: left; font-size: 20px; padding-bottom: 10px; }
      input[type="checkbox"] { width: 20px; height: 20px; }
      textarea { padding: 10px; min-width: 300px; }
    </style>
    <script>window.onbeforeunload = function() { return "Data will be lost if you leave the page, are you sure?"; };</script>
'''
htmlZipErrors = ""

# This grader extracts all zip files inside the folders.
# Then, it checks that the given files are present and the given lines are found in the files
# If not, it prints to console the student and their missing files/lines

print(os.linesep, os.linesep)
print("STARTING :BEFORE:GRADING:CHECKER")
print(os.linesep)

# Get list of all folders in the target folder
folders = [f for f in os.listdir('./') if os.path.isdir(f)]

# Go through all files inside each folder recursively and extract the zip files
for folder in folders:
  for root, dirs, files in os.walk(folder):
    for file in files:
      if file.endswith(".zip"):
        # If the zip has already been extracted, skip it
        if os.path.exists(os.path.join(root, file[:-4])):
          continue
        # Otherwise, extract the zip file
        try:
          zip_ref = zipfile.ZipFile(os.path.join(root, file), 'r')
          zip_ref.extractall(root)
          zip_ref.close()
        except Exception as e:
          print("Error extracting zip file:", root + "/" + file)
          print(e)
          htmlZipErrors += "Zip file could not be extracted: " + root + "/" + file + "<br />"
print("ALL ZIP FILES EXTRACTED!")

if (htmlZipErrors != ""):
  htmlOutput += "<h1 class='title-fail'>Zip Extraction Errors</h1>"
  htmlOutput += htmlZipErrors

def didNotFindEverything(dictionary):
  if (len(dictionary) == 0): return False
  for val in dictionary.values():
    if val == 0: return True
  return False

htmlOutput += '<h1 class="title-fail">Problems</h1>'
htmlOutput += '<table class="table-fail"><tr><th>Folder</th><th>Problems</th><th>Handled?</th><th>Notes</th></tr>'

# Go through all files inside each folder recursively and verify that the required files and folders exist
for folder in folders:
  # Create maps of the required files and lines for matching afterwards
  requiredFilesMap : dict = {}
  requiredLinesMap : dict = {}
  for file in requiredFiles: requiredFilesMap[file] = 0
  for line in requiredLines: requiredLinesMap[line] = 0

  for root, dirs, files in os.walk(folder):
    for file in files:
      #print(str(file))
      if str(file).lower() in requiredFiles: requiredFilesMap[str(file).lower()] = 1
      # Check does the file contain any of the required lines
      with open(os.path.join(root, file), 'r', errors='ignore') as f:
        for line in f:
          requiredLineCopy : dict = requiredLinesMap.copy()
          for requiredLine in requiredLineCopy:
            if requiredLine in line:
              requiredLinesMap[requiredLine] = 1

  if didNotFindEverything(requiredFilesMap) or didNotFindEverything(requiredLinesMap):
    # Print the student's name
    print(os.linesep)
    print("#######")
    print(folder)
    htmlOutput += "<tr><td>" + folder + "</td><td>"
    # Check if there are still any files or lines that are not found
    for file in requiredFilesMap:
      if requiredFilesMap[file] == 0:
        print("  File: " + file + " is missing")
        htmlOutput += "File: " + file + " is missing<br>"
    for line in requiredLinesMap:
      if requiredLinesMap[line] == 0:
        print("  Line: " + line + " is missing")
        htmlOutput += "Line: " + line + " is missing<br>"
    htmlOutput += "</td>"
    htmlOutput += "<td><input type='checkbox' /></td><td><textarea></textarea></td>"
    htmlOutput += "</tr>"
htmlOutput += "</table>"

htmlOutput += "</html>"
if generateHTMLReport:
  if os.path.exists("grader_output.html"):
    os.remove("grader_output.html")
  with open("grader_output.html", "w") as f:
    f.write(htmlOutput)
  print(os.linesep)
  print("Created grader_output.html file")