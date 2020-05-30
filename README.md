# SearchEngine

### Why are there two versions?
- For grading Milestone 3 of this assignment, only look at version2.
Version 1 was created during Milestone 1 & 2 of this assignment. The inverted index used in Version 1 is slow to obtain postings from. For Milestone 3, I created a new version of this project which obtains Postings from the inverted index at constant time which allows for faster query times.

### Structure of Given Data
Main Directory ('ANALYST' or 'DEV')
- Domain Name
    - json file
        - url
        - content
        - encoding

### Questions I had during project:
How do I iterate through folders/files in a directory?
https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory

How do I open multiple files at the same time without knowing how many files I may have?
https://stackoverflow.com/questions/29550290/how-to-open-a-list-of-files-in-python