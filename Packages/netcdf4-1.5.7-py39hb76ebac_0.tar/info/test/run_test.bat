



ncinfo -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
nc4tonc3 -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
nc3tonc4 -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
