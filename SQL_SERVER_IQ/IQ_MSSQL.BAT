ECHO OFF
ECHO SERVER %1

sqlcmd -s %1 -d "master" -o "IQ_MSSQL.CSV"  -i "IQ_MSSQL.SQL"

IF %ERRORLEVEL% == 0 ECHO SCRIPT COMPLETED





