@echo off
:: Get the folder where the batch file is located
set "SCRIPT_DIR=%~dp0"

:loop
set /p SPOTIFY_LINK=Paste Spotify URL (or type EXIT to quit) and press Enter: 
if /i "%SPOTIFY_LINK%"=="EXIT" goto exit /b

:: Call the Python script in the same folder
for /f "delims=" %%i in ('python "%SCRIPT_DIR%spotify_to_ytm.py" "%SPOTIFY_LINK%"') do set YT_LINK=%%i

:: Copy to clipboard
echo %YT_LINK% | clip
echo YouTube Music link copied to clipboard:
goto loop

:exit
echo Exiting...
pause
