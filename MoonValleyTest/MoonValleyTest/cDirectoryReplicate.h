#pragma once

class cDirectoryReplicate
{
public:
	cDirectoryReplicate(void);
public:
	~cDirectoryReplicate(void);
public:
	BOOL ReplicateDirectory(LPCWSTR sSourcePath, LPCWSTR sDestinationPath);


bool IsPathExisting(LPCWSTR sPath);

private:

	void Replicate(LPCWSTR SourcePath, LPCWSTR DestinationPath, LPCWSTR ArchivePath);

	void ArchiveDestinationNotInSource(LPCWSTR sSourcePath, LPCWSTR sDestinationPath, LPCWSTR sArchivePath);




};


