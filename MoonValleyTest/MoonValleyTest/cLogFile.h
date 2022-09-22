#pragma once

class cLogFile
{
public:
	cLogFile(void);
public:
	~cLogFile(void);

public:
	bool IsInitialized;
	void Truncate();
	bool Initialize(CString cLogFile);


	// Add string value to log file
	void Write(LPCWSTR sInput);


private:
	CFile file;

	// Get system date time as CString
	CString GetDateTimeString(void);


};



