@echo off
setlocal enabledelayedexpansion

:: Ensure downloads folder exists
if not exist "Downloads\Soundcloud" mkdir "Downloads\Soundcloud"

:loop
set choice=1
cls
echo ======================================================
echo  SoundCloud
echo ======================================================
echo  Paste a SoundCloud track URL below
echo  (or type EXIT to quit)
echo ======================================================
set /p url=SoundCloud URL: 

if /i "!url!"=="EXIT" goto exit
if /i "!url!"=="exit" goto exit
if /i "!url!"=="Exit" goto exit

:menu
cls
echo ========================================
echo  SoundCloud Options
echo ========================================
echo  1. Copy direct MP3 URL to clipboard (DEFAULT)
echo  2. Download
echo  0. Go back
echo ========================================
set /p choice=Select an option [1-2]: 

:: Only pass cookies if file exists
set cookies_arg=
if exist "soundcloud.com_cookies.txt" set cookies_arg=--cookies "soundcloud.com_cookies.txt"

cls
if "!choice!"=="" set choice=1

if "!choice!"=="1" (
    echo Getting direct MP3 URL...
    yt-dlp -f mp3 --no-playlist !cookies_arg! --get-url "!url!" > temp_url.txt

    for /f "usebackq delims=" %%a in ("temp_url.txt") do (
        set "direct_url=%%a"
        goto copyurl
    )

    :copyurl
    echo !direct_url! > temp_url_quoted.txt
    powershell -Command "Get-Content temp_url_quoted.txt | Set-Clipboard"
    del temp_url.txt temp_url_quoted.txt
    echo.
    echo Direct MP3 URL copied to clipboard!
    timeout /t 5 >nul
    goto loop
)

if "!choice!"=="2" (
    echo Downloading track with cover art...
    yt-dlp -f mp3 --embed-thumbnail --add-metadata --no-playlist !cookies_arg! -o "Downloads/Soundcloud/%%(title)s.%%(ext)s" "!url!"
    echo.
    echo Download complete!
    timeout /t 5 >nul
    goto loop
)

if "!choice!"=="1" (
goto loop
)

:: Default fallback to copy
yt-dlp -f mp3 --no-playlist !cookies_arg! --get-url "!url!" > temp_url.txt
for /f "usebackq delims=" %%a in ("temp_url.txt") do (
    set "direct_url=%%a"
    goto copyurl
)

goto loop

:exit
echo Exiting...
timeout /t 1 >nul
exit
