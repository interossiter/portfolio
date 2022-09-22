#pragma once

class cDirectoryRecursive
{

protected:
	cDirectoryRecursive(void);

public:
	~cDirectoryRecursive(void);

public:

	BOOL ProcessDirectory(LPCWSTR sPath, LPCWSTR sWildcard);

	virtual BOOL FoundDirectory(LPCWSTR sPath) const;

	virtual BOOL FoundFile(LPCWSTR sPath) const;


};
