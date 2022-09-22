# Purpose
To verify proper installation of Microsoft SQL Server software on a workstation / server.
# Technical Approach
Use core Microsoft Operating System functions to examine system directly, without reliance on additional software components.

It is the wmic function that is relied upon extensively.

See MS documentation for information on wmic.

To execute the test, a Windows Batch file is run that makes a series of calls to the wmic functions.

Results from those calls are output to files for examination.

The file IQ_SERVER.bat can be examined to see which functions are being called or to adapt the file.

# Acceptance Criteria

The test will demonstrate that:
-	Microsoft SQL Server has been installed
-	Microsoft SQL Server Database Service is configured correctly
-	Microsoft SQL Server 'master' database is running
-	Microsoft SQL Server Agent is running
-	Microsoft SQL Server Reporting Service is configured correctly
-	Microsoft SQL Server Integration Service is configured correctly
-	Operating System version is correct
-	Database Timezone is configured correctly

# Pre-test Set-up
-	Log into target machine / server
-	Create a folder to hold your testing results e.g. C:\IQ
-	Copy file IQ_SERVER.BAT into the folder e.g. C:\IQ\IQ_SERVER.BAT
-	Navigate to the folder you created e.g. C:\IQ
-	Open a command prompt (Start Menu, enter cmd.exe)
-	Navigate to the location you created e.g. cd C:\IQ

Step	Procedure	Expected Result
Generate a set of data showing the configuration details on the target machine and output those results to files for subsequent examination.
1	Run the command IQ_SERVER.BAT	Script runs, indicates ëSCRIPT COMPLETEDí and returns to command prompt.
Microsoft SQL Server has been installed
		
Microsoft SQL Server Database Service is configured correctly
		
Microsoft SQL Server ëmasterí database is running
		
Microsoft SQL Server Agent is running
		
Microsoft SQL Server Reporting Service is configured correctly
		
Microsoft SQL Server Integration Service is configured correctly
		
Microsoft SQL Server Analysis Service is configured correctly
		
Operating System version is correct
		
Database Timezone is configured correctly
		




The goal of installation qualification (IQ) is to demonstrate and document that a computer system is installed and configured correctly.

I am going to demonstrate some methods of performing on a SQL Server instance.

# Is SQL Server installed on this machine (simple)?

	Approach:  log into machine with full administrator priviledges, open a command prompt and issue the sqlcmd command to connect to the database server.
	
	If you get to the point that the sqlcmd command prompt appears, you have confirmed at a simple level that SQL Server has been installed on the machine.

Step  | Expected Result 
------------- | ------------- 
Log into machine using account with administrator level priveleges    | Successful login  
Open a command prompt	| Command window appears
Enter the command:  sqlcmd	| The command prompt changes to: 1>

# What optional pieces of SQL Server are installed on this machine e.g. SSIS, SSRS?

	Approach:  log into machine with full administrator priviledges, open a command prompt and issue the sqlcmd command to connect to the database server.

Step  | Expected Result 
------------- | ------------- 
Log into machine using account with administrator level priveleges    | Successful login  
Open a command prompt	| Command window appears
Enter the command:  sqlcmd	| The command prompt changes to: 1>






![My cool picture](http://markdownpro.com/assets/html5_logo.png)


