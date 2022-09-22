// MoonValleyTest.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "MoonValleyTest_SteveMuller.h"
#include "cLogFile.h"
#include "cDirectoryReplicate.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// The one and only application object

CWinApp theApp;

using namespace std;

int _tmain(int argc, TCHAR* argv[], TCHAR* envp[])
{
	int nRetCode = 0;

	BOOL bReturn = false;

	// initialize MFC and print and error on failure
	if (!AfxWinInit(::GetModuleHandle(NULL), NULL, ::GetCommandLine(), 0))
	{
		// TODO: change error code to suit your needs
		_tprintf(_T("Fatal Error: MFC initialization failed\n"));
		nRetCode = 1;
	}
	else
	{

		try
		{

			// get intput params and check for source and destination paths

			LPCWSTR sSourcePath = argv[1];

			LPCWSTR sDestintationPath = argv[2];

			cDirectoryReplicate replicate;

			bReturn = replicate.ReplicateDirectory(sSourcePath, sDestintationPath);

		}
		catch(const char ErrorMessage[])
		{

			// catch first errorMessage thrown directly from cDirectoryReplicate - errors relate to bad input paths and failures to create log file
			//		-> these errors lead to cDirectoryReplicate not being able to start processing

			nRetCode = 1;

			printf(ErrorMessage);

			// delay so user can see error or use getchar to hold on screen until user hits enter

			Sleep(3000);

			//getchar();

			return nRetCode;

		}

		if (! bReturn)
		{

			// cDirectoryReplicate counts errors related to failure to move or archive files and reports existence of those errors
			//		through bReturn if error count > 0

			nRetCode = 1;

			printf("Error returned by ReplicateDirectory");

			// delay so user can see error or use getchar to hold on screen until user hits enter

			//Sleep(3000);

			getchar();

			return nRetCode;

		}


	}


	return nRetCode;

}
