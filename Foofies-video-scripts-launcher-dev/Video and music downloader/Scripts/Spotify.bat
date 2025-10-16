@echo off
setlocal enabledelayedexpansion

:: Get script folder
set "SCRIPT_DIR=%~dp0"

:loop
set choice=1
cls
echo  For age gated videos, ensure you have exported cookies from your browser to 'www.youtube.com_cookies.txt'.
echo  For info on how to do this, open tips in the main GUI.
echo  Cookies expire after a while, so you may need to refresh them periodically.
echo ============================================================================
echo  Paste Spotify URL 
echo  (or type EXIT to quit)
echo ============================================================================
set /p SPOTIFY_URL=Spotify URL: 
if /i "%SPOTIFY_URL%"=="EXIT" goto exit
if /i "%SPOTIFY_URL%"=="exit" goto exit
if /i "%SPOTIFY_URL%"=="Exit" goto exit

:: Optional artist input
cls
echo ================================================================
echo  Artist name is optional but can help improve search accuracy.
echo ================================================================
set /p ARTIST= Optional: Enter main artist (or leave empty): 

:menu
cls
echo ========================================
echo  Spotify Download Options				
echo ========================================
echo  1. Copy YouTube link	(DEFAULT)				
echo  2. Copy direct video URL to clipboard			
echo  3. Download	
echo  0. Go back						
echo ========================================
set /p OPTION=Select an option [1-3]: 
cls
if "%OPTION%"=="1" goto copy_link
if "%OPTION%"=="2" goto copy_direct
if "%OPTION%"=="3" goto download
if "%OPTION%"=="0" goto loop
goto copy_link
pause
goto menu

:copy_link
for /f "delims=" %%i in ('python "%SCRIPT_DIR%spotify_tool.py" link "%SPOTIFY_URL%" "%ARTIST%"') do set YT_LINK=%%i
echo YouTube link copied to clipboard: %YT_LINK%
pause
goto loop

:copy_direct
for /f "delims=" %%i in ('python "%SCRIPT_DIR%spotify_tool.py" direct "%SPOTIFY_URL%" "%ARTIST%"') do set DIRECT_URL=%%i
echo Direct playable URL copied to clipboard: %DIRECT_URL%
pause
goto loop

:download
set /p VIDEO_CHOICE=Do you want the music video? (y/n): 
python "%SCRIPT_DIR%spotify_tool.py" download "%SPOTIFY_URL%" "%ARTIST%" %VIDEO_CHOICE%
pause
goto loop

:exit
echo Exiting...
timeout /t 1 >nul
exit
