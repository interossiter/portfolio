#include "StdAfx.h"
#include "cDirectoryRecursive.h"

cDirectoryRecursive::cDirectoryRecursive(void)
{
}

cDirectoryRecursive::~cDirectoryRecursive(void)
{
}

BOOL cDirectoryRecursive::ProcessDirectory(LPCWSTR sPath, LPCWSTR sWildcard)
{

    CFileFind finder;

	CString sSearch;

	sSearch.Format(_T("%s\\%s"), sPath, sWildcard);

	BOOL bWorking = finder.FindFile(sSearch);

    while (bWorking)
    {

        bWorking = finder.FindNextFile();

		if (finder.IsDirectory())
		{

			if (! finder.IsDots())
			{

				return FoundDirectory(finder.GetFilePath());

			}
			else
			{


				continue;

			}


		}
		else
		{

			return FoundFile(finder.GetFilePath());


		}

        
    }

    return TRUE;

}








