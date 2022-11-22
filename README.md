# :Before:Grading:Checker

![image](https://user-images.githubusercontent.com/3810422/203306151-158d1fcd-f045-420a-8717-f9ac1d1c0902.png)

This script can be used to check the folders inside the directory recursively for matching files and lines inside files. Used by me at university for checking student submissions for matching files and folders for faster grading. All students who have not returned certain file(s) or do not have certain  line(s) in their submissions will have more throughout inspection done.

Produces the output in a HTML file and also in console. Example of the produced output is visible below:

![image](https://user-images.githubusercontent.com/3810422/203306438-e9e677f6-c334-4db6-9fc5-efa35c2f3e55.png)

## Usage

1. Download this repository
2. Move the files ``grader.py`` and ``grader_settings.json`` to a folder where you have the folders which you need to check.
3. Add in ``grader_settings.json`` the files and lines to check.
4. Run the ``grader.py`` using python. For example: ``python3 grader.py``
5. Output will be printed in the console and HTML report will also be created in file ``grader_report.html``, if that configuration is enabled in the ``grader_settings.json`` file.
