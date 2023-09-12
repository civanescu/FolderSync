#### Synchronizes two folders: source and replica. 

* The program should maintain a full, identical copy of source 
folder at replica folder. 
* Synchronization must be one-way: after the synchronization content of the 
 replica folder should be modified to exactly match content of the source 
 folder; 
* Synchronization should be performed periodically;
 
* File creation/copying/removal operations should be logged to a file and to the 
 console output;
* Folder paths, synchronization interval and log file path should be provided 
 using the command line arguments;


# Notes
- I tried to maintain an easy to modify code being ready for new changes.
- I created a class especially for compare & copying file to file, to add new features or to include in other ones.
- I added the option to use 0 for "sleep time." This way will run only one time.
- I don't process/reprocess errors on files immediately (like can't write to disk, file changed) because probably could be under usage somehow and is better to try at next run, so I keep in logs
- Only external library is pytest used for testing scripts.
- There is no way to test "file changed while copy" case, not implemented.
- Any autocompleting was done by PyCharm IDE. Didn't use CoPilot, GPT, only Google/Stackoverflow for some testing issues  
 