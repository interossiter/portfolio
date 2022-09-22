#include "StdAfx.h"
#include "cLogFile.h"

// used to add to end of each line on write
const TCHAR CharReturn[3] = {(char)13, (char)10, NULL};


cLogFile::cLogFile(void)
{

	IsInitialized = false;

}

cLogFile::~cLogFile(void)
{
}


// Add string value to log file
void cLogFile::Write(LPCWSTR sInput)
{

	if (IsInitialized)
	{

		file.SeekToEnd();

		CArchive ar(&file, CArchive::store);

		CString sLog;

		sLog.Format(_T("%s\t%s"), GetDateTimeString(), sInput);

		ar.WriteString((LPCWSTR) sLog);

		ar.WriteString((LPCWSTR) CharReturn);

		ar.Close();

	}

}


// initialize log file to full file path
bool cLogFile::Initialize(CString sLogPath)
{
	if (file.Open(sLogPath, CFile::modeCreate | CFile::modeNoTruncate  | CFile::modeWrite) == TRUE)
	{
		IsInitialized = true;
		return true;
	}
	else
	{
		IsInitialized = false;
		return false;
	}
}


// truncate existing file
void cLogFile::Truncate()
{
	file.SetLength((DWORD) 0);
}




// Get system date as CString
CString cLogFile::GetDateTimeString(void)
{

//grab current time and return formatted 

	CTime time = CTime::GetCurrentTime();

	return time.Format( "%m/%d/%y %X" );

}




