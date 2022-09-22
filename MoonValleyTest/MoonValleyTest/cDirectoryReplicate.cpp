#include "StdAfx.h"
#include "cDirectoryReplicate.h"
#include "cLogFile.h"

// Struct holds statistics and other info relating to this run
// => if you change this, alter ReplicateDirectory where log is being written
struct Statistics
{

	int FilesProcessed;

	int FilesArchived;

	int FilesCopied;

	CString StartTime;

	CString FinishTime;

	LONGLONG SecondsElapsed;

	int ErrorCount;

};


Statistics stats;

cDirectoryReplicate::cDirectoryReplicate(void)
{

}

cDirectoryReplicate::~cDirectoryReplicate(void)
{

}

BOOL cDirectoryReplicate::ReplicateDirectory(LPCWSTR sSourcePath, LPCWSTR sDestinationPath)
{
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
//	ReplicateDirectory Method
//	Purpose:  Public method called by consumer to initiate replication process
//	Description:  
//				- performs pre-run checks to make sure paths are valid and log file is in place
//				- calls method that handles directory replication
//				- calls method that cleans-up destination to remove files / directories not present in source
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

	BOOL bReturn = false;

	CString sMsg;

	CTime timeStart =  CTime::GetCurrentTime();

	stats.StartTime = timeStart.Format( "%m/%d/%y %X" );


// check to see if SourcePath exists, if not raise exception

	if (! IsPathExisting(sSourcePath))
	{

		throw "Source folder does not exist";

		return false;

	}


	// if destination path does not exist, create it and confirm success else throw error

	if (! IsPathExisting(sDestinationPath))
	{

		bReturn = CreateDirectory((LPCWSTR) sDestinationPath, NULL);


		if (! bReturn)
		{

			throw "Failed to create destination folder";

			return false;

		}

	}


	// set-up archive location

	CString sArchivePath;

	sArchivePath.Format(_T("%s\\Archive"), sDestinationPath);

	if (! IsPathExisting(sArchivePath))
	{

		bReturn = CreateDirectory((LPCWSTR) sArchivePath, NULL);

		if (! bReturn)
		{

			throw "Failed to create archive folder";

			return false;

		}
	}

	// set-up log file

	cLogFile log;

	CString sLogPath;

	sLogPath.Format(_T("%s\\logfile.txt"), sArchivePath);

	bReturn = log.Initialize((LPCWSTR) sLogPath);

	if (! bReturn)
	{

		throw "Failed to initialize log file";

		return false;

	}

	// Setup complete:

	//  this call will mirror source onto destination

	cDirectoryReplicate::Replicate(sSourcePath, sDestinationPath, sArchivePath);


	//this call archives files in destination that no longer exist in source 

	cDirectoryReplicate::ArchiveDestinationNotInSource(sDestinationPath, sSourcePath, sArchivePath);

	
	// demo only delete this line for production

	Sleep(2000); 


	// calculate elapsed time

	CTime timeFinish =  CTime::GetCurrentTime();

	stats.FinishTime = timeFinish.Format( "%m/%d/%y %X" );

	CTimeSpan timeElapsed = timeFinish - timeStart;

	stats.SecondsElapsed = timeElapsed.GetTotalSeconds();


	// done processing files, write stats to log

	sMsg.Format(_T("%s\t%s\t%s\t%s\t%s\t%s\t%s"), _T("FilesProcessed"), _T("FilesCopied"), _T("FilesArchived"), _T("StartTime"), _T("FinishTime"), _T("SecondsElapsed"), _T("ErrorCount"));

	log.Write(sMsg);

	sMsg.Format(_T("%d\t%d\t%d\t%s\t%s\t%d\t%d"), stats.FilesProcessed, stats.FilesCopied, stats.FilesArchived, stats.StartTime, stats.FinishTime, stats.SecondsElapsed, stats.ErrorCount);

	log.Write(sMsg);

	if (stats.ErrorCount == 0)
	{

		return true;

	}
	else
	{
		return false;

	}

}



void cDirectoryReplicate::ArchiveDestinationNotInSource(LPCWSTR sSourcePath, LPCWSTR sDestinationPath, LPCWSTR sArchivePath)
{
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
//	ArchiveDestinationNotInSource Method
//	Purpose:  Remove files / directories from destination no longer present in source
//	Description:  recursion is key element
//				- for a given source / destination, files are processed first
//				- folders are processed second
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

	CFileFind findDestination;

	CString sSearch;

	CString sDestinationFilePath;

	CString sSourceFilePath;

	CString sArchiveFilePath;

	BOOL bWorking = false;

	int nReturn = 0;


	//first process all ~files~ in this directory

	sSearch.Format(_T("%s\\%s"), (LPCWSTR) sSourcePath, _T("*.*"));

	bWorking = findDestination.FindFile(sSearch);

	while (bWorking)
	{

		bWorking = findDestination.FindNextFile();

	 	if (! findDestination.IsDirectory())
		{
			// get all paths that may be needed for later use

			sDestinationFilePath = findDestination.GetFilePath();

			sSourceFilePath.Format(_T("%s\\%s"), sDestinationPath, findDestination.GetFileName());

			sArchiveFilePath.Format(_T("%s\\%s"), sArchivePath, findDestination.GetFileName());


			if (! IsPathExisting(sSourceFilePath))
			{

				nReturn = CopyFile(sDestinationFilePath, sArchiveFilePath,  FALSE);

				if (nReturn == 0)
				{

					// copy to archive failed, don't delete file

					stats.ErrorCount++;

				}
				else
				{

					nReturn = DeleteFile(sDestinationFilePath);

					if (nReturn == 0)
					{

						stats.ErrorCount++;

					}
					else
					{
						//successful file archive

						stats.FilesArchived++;

					}

				}

			}
			
		}

	}


	// files are done, now process ~folders~ with recursive call

	sSearch.Format(_T("%s\\%s"), sSourcePath, _T("*."));

	bWorking = findDestination.FindFile(sSearch);

	
	while (bWorking)
	{

		bWorking = findDestination.FindNextFile();

	    sSourceFilePath.Format(_T("%s\\%s"), sDestinationPath, findDestination.GetFileName());

		sDestinationFilePath = findDestination.GetFilePath();


		// need to make sure we aren't deleting archive folder in reference to source - archive folder isn't present on source 

	 	if (findDestination.IsDirectory() && ! findDestination.IsDots() &&  sDestinationFilePath != sArchivePath)
		{

			// directory is empty at this point

			if (! IsPathExisting(sSourceFilePath))
			{

				nReturn = RemoveDirectory(sDestinationFilePath); // remove the empty directory

				if (nReturn == 0)
				{

					stats.ErrorCount++;

				}

			}


			cDirectoryReplicate::ArchiveDestinationNotInSource(sDestinationFilePath, sSourceFilePath, sArchivePath);

		}

	}

}




void cDirectoryReplicate::Replicate(LPCWSTR SourcePath, LPCWSTR DestinationPath, LPCWSTR ArchivePath)
{
/////////////////////////////////////////////////////////////////////////////////////////////////////////////
//	Replicate Method
//	Purpose:  Mirror contents of source directory onto destination
//				- source files not existing on destination are copied to destination
//				- newer source files replace older ones on destination
//				- any files removed from source are placed in archive folder in destination
//				- this method does not remove files / folders from destination not present in source, 
//					see ArchiveDestinationNotInSource method
//	Description:  recursion is key element
//				- for a given source / destination, files are processed first
//				-	folders are processed second, assuring that destination directories are present prior to recursive call
/////////////////////////////////////////////////////////////////////////////////////////////////////////////

	CFileFind findSource;

	CFileFind findDestination;

	CTime timeSource;

	CTime timeDestination;

	CString sSearch;

	CString sSourceFilePath;

	CString sDestinationFilePath;

	CString sArchiveFilePath;

	BOOL bWorking = false;

	int nReturn = 0;


	//first process all ~files~ in this directory

	sSearch.Format(_T("%s\\%s"), (LPCWSTR) SourcePath, _T("*.*"));

	bWorking = findSource.FindFile(sSearch);

	while (bWorking)
	{

		bWorking = findSource.FindNextFile();

	 	if (! findSource.IsDirectory())
		{

			stats.FilesProcessed++;

			// get all paths that may be needed for later use

			sSourceFilePath = findSource.GetFilePath();

			sDestinationFilePath.Format(_T("%s\\%s"), DestinationPath, findSource.GetFileName());

			sArchiveFilePath.Format(_T("%s\\%s"), ArchivePath, findSource.GetFileName());

			if (! IsPathExisting(sDestinationFilePath))
			{

				// file doesn't exist in destination, so copy it now

				nReturn = CopyFile(sSourceFilePath, sDestinationFilePath, FALSE );

				if (nReturn == 0)
				{

					stats.ErrorCount++;

				}
				else
				{

					stats.FilesCopied++;

				}

			}
			else
			{
				
				// file exists in destination, only allow copy w/ replace if source file is newer than destination

					findDestination.FindFile(sDestinationFilePath);

					findDestination.FindNextFile();


					findSource.GetLastWriteTime(timeSource);

					findDestination.GetLastWriteTime(timeDestination);


					CTimeSpan timeSpan = timeSource - timeDestination;


					if (timeSpan.GetTotalSeconds() > 0)
					{
						//source is newer, archive destination and copy source 
						
						// using CopyFile rather than MoveFile so that any existing archive copy will be replaced

						nReturn = CopyFile(findDestination.GetFilePath() ,sArchiveFilePath,  FALSE);

						if (nReturn == 0)
						{

							//file archive failed

							stats.ErrorCount++;

						}
						else
						{

							stats.FilesArchived++;

						}


						//copy source to destination

						nReturn = CopyFile(findSource.GetFilePath(), sDestinationFilePath, FALSE );

						if (nReturn == 0)
						{

							stats.ErrorCount++;

						}
						else
						{

							stats.FilesCopied++;

						}

					}
					else
					{
						//leave destination alone, it's the newer file


					}


			}


		}

	}


	// files are done, now process ~folders~ with recursive call

	sSearch.Format(_T("%s\\%s"), (LPCWSTR) SourcePath, _T("*."));

	bWorking = findSource.FindFile(sSearch);

	
	while (bWorking)
	{

		bWorking = findSource.FindNextFile();

	    sDestinationFilePath.Format(_T("%s\\%s"), DestinationPath, findSource.GetFileName());

	 	if (findSource.IsDirectory() && ! findSource.IsDots() &&  sDestinationFilePath != ArchivePath)
		{


			// make sure destination folder is in place before recursive call that will start processing the files first

			if (! IsPathExisting(sDestinationFilePath))
			{

				nReturn = CreateDirectory((LPCWSTR) sDestinationFilePath, NULL);

				if (nReturn == 0)
				{

					// failed to create destination directory

					stats.ErrorCount++;

				}

			}


			cDirectoryReplicate::Replicate(findSource.GetFilePath(), sDestinationFilePath, ArchivePath);

		}

	}


}







bool cDirectoryReplicate::IsPathExisting(LPCWSTR sPath)
{
// Check for directory is existing status

	return (GetFileAttributes(sPath) != INVALID_FILE_ATTRIBUTES);

}





