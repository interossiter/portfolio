ECHO OFF
ECHO SERVER %1 > %4
ECHO DATABASE %2 >> %4
ECHO SCRIPT %3 >> %4
sqlcmd -S %1 -d %2 -i %3 -W -w 999 -s "	" >> %4 2>&1
IF %ERRORLEVEL% == 0 ECHO SCRIPT COMPLETED
IF NOT %ERRORLEVEL% == 0 ECHO SCRIPT FAILED WITH ERRORLEVEL %ERRORLEVEL%
IF NOT %ERRORLEVEL% == 0 ECHO "PARAMETERS: <server\instance> <databaseName> <inputSqlScriptFile> <outputFile>"
