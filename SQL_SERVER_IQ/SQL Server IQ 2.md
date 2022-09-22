# Purpose
To verify proper installation and configuration of Microsoft SQL Server software on a workstation or server.
# Technical Approach
Use core Microsoft Operating System functions to examine system directly, without reliance on additional software components.

It is the WMI Command Line Utility (WMIC) that is relied upon extensively.

See MS documentation for information:

http://msdn.microsoft.com/en-us/library/aa394531(v=vs.85).aspx

To execute the test, a Windows Batch file is run that makes a series of calls to the WMIC functions.

Results from those calls are output to files for examination.

The file IQ_SERVER.bat can be examined to see which functions are being called or to adapt the file.

# Acceptance Criteria

The test will demonstrate that:
-	Microsoft SQL Server has been installed
-	Microsoft SQL Server Database Service is configured correctly
-	Microsoft SQL Server Agent is configured correctly
-	Microsoft SQL Server Reporting Service is configured correctly
-	Microsoft SQL Server Integration Service is configured correctly
-	Microsoft SQL Server Analysis Service is configured correctly
-	Operating System version is correct
-	Database Timezone is configured correctly

# Pre-test Set-up
	Approach:  log into target machine and create location to hold test scripts and output data.  Open a command prompt and navigate to that location.

-	Log into target machine / server
-	Create a folder to hold your testing results e.g. C:\IQ [IQ_FOLDER]
-	Copy file [IQ_SERVER.BAT] into [IQ_FOLDER]
-	Navigate to  [IQ_FOLDER]
-	Open a command prompt (Start Menu, enter cmd.exe)
-	Navigate to  [IQ_FOLDER]
-   Run the script by entering the command IQ_FOLDER.BAT

# Generate Output Files Documenting Installed Software and Status of Service Applications
	Approach:  run script that calls operating system functions that generate sets of data describing system configuration.  Those results are placed in output files for subsequent examination.
	The file _PRODUCT.csv contains details which software applications are installed on the machine.
	The file _SERVICE.csv contains details which services are running and their health status.
	Taken in conjunction, these sets of data can be used to document which versions of software are installed and wheter critical service applications are running as expected.

-	Open a command prompt (Start Menu, enter cmd.exe)
-	Navigate to  [IQ_FOLDER]
-   Run the script by entering the command IQ_FOLDER.BAT

The script takes approximately one minute to run.

# Examine Values To Check Status (IQ)

	Approach:  Having generated a rich set of data describing the system and its status, check the data for specific values relating to the goal of the IQ.  For example, confirm that SQL Server is installed.
	
	These steps become the core of your IQ documentation and can be cut-and-paste and specific values edited to suit the particular versions of software you are targeting.



Step  | Value to Check  |  Expected
------------- | ------------- | ----------
Microsoft SQL Server has been installed    | Examine the _PRODUCT.csv file.  Locate the value where name = SQL Server 2014 Database Engine Services.  | Vendor = Microsoft Corporation; Version =  12.0.2000.8 
Microsoft SQL Server Database Service is configured correctly    | Examine the _SERVICE.csv file.  Locate the value where name =  MSSQLSERVER |  StartMode = Auto; State = Running; Status = OK; 
Microsoft SQL Server Agent is configured correctly   | Examine the _SERVICE.csv file.  Locate the value where name =  SQLSERVERAGENT |  StartMode = Auto; State = Running; Status = OK;
Microsoft SQL Server Reporting Service is configured correctly   |  Examine the _SERVICE.csv file.  Locate the value where name = XXXXXXXXXXXX  |  StartMode = Auto; State = Running; Status = OK;
Microsoft SQL Server Analysis Service is configured correctly    | 	 Examine the _SERVICE.csv file. Locate the value where name =  MSSQLServerOLAPService   | StartMode = Auto; State = Running; Status = OK;
Microsoft SQL Server Integration Service is configured correctly   |  Examine the _SERVICE.csv file. Locate the value where name =  xxxxxxxxx  |  StartMode = Auto; State = Running; Status = OK;
Operating System version is correct   |  Examine the _OS.csv file.  Locate the Version value.  |  Version = 6.1.7601 
Database Timezone is configured correctly   |  Examine the _TIMEZONE.csv file.  |  Caption = (UTC-08:00) Pacific Time (US &amp; Canada)
