@echo off
setlocal enabledelayedexpansion

:: Get script folder
set "SCRIPT_DIR=%~dp0"

:main
cls
echo =========================
echo Spotify Downloader
echo =========================
set /p SPOTIFY_URL=Paste Spotify URL (or type EXIT to quit): 
if /i "%SPOTIFY_URL%"=="EXIT" goto exit

:: Optional artist input
echo Artist name is optional but can help improve search accuracy.
set /p ARTIST=Optional: Enter main artist (or leave empty): 

:menu
cls
echo =========================
echo Spotify Download Options
echo =========================
echo 1. Copy YouTube link
echo 2. Copy direct YouTube link
echo 3. Download
echo =========================
set /p OPTION=Select an option [1-3]: 

if "%OPTION%"=="1" goto copy_link
if "%OPTION%"=="2" goto copy_direct
if "%OPTION%"=="3" goto download
echo Invalid choice, try again.
pause
goto menu

:copy_link
for /f "delims=" %%i in ('python "%SCRIPT_DIR%spotify_tool.py" link "%SPOTIFY_URL%" "%ARTIST%"') do set YT_LINK=%%i
echo YouTube link copied to clipboard: %YT_LINK%
pause
goto main

:copy_direct
for /f "delims=" %%i in ('python "%SCRIPT_DIR%spotify_tool.py" direct "%SPOTIFY_URL%" "%ARTIST%"') do set DIRECT_URL=%%i
echo Direct playable URL copied to clipboard: %DIRECT_URL%
pause
goto main

:download
set /p VIDEO_CHOICE=Do you want the music video? (y/n): 
python "%SCRIPT_DIR%spotify_tool.py" download "%SPOTIFY_URL%" "%ARTIST%" %VIDEO_CHOICE%
pause
goto main

:exit
echo Exiting...
pause
exit
