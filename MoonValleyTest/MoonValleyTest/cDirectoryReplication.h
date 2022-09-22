#pragma once
#include "cDirectoryRecursive.h"

class cDirectoryReplication :
	public cDirectoryRecursive
{
public:
	cDirectoryReplication(void);
public:
	~cDirectoryReplication(void);

public:

	BOOL FoundDirectory(LPCWSTR sPath);

	BOOL FoundFile(LPCWSTR sPath);


};
