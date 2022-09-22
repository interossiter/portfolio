USE master

GO

EXEC sp_configure 'show advanced option', '1';

GO

RECONFIGURE

GO

EXEC sp_configure