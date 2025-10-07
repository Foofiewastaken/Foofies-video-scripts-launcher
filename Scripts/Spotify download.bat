@echo off
setlocal enabledelayedexpansion
:loop
:: Prompt for Spotify URL
echo Paste Spotify URL (or type EXIT to quit) and press Enter:
set /p SPOTIFY_URL=
if /i "!url!"=="EXIT" goto end
:: Run spotdl and capture output
for /f "tokens=* delims=" %%i in ('spotdl download "%SPOTIFY_URL%" 2^>^&1') do (
    set "line=%%i"
    echo !line!

    :: Look for YT Music link
    echo !line! | findstr "https://music.youtube.com" >nul
    if not errorlevel 1 (
        for /f "tokens=*" %%a in ("!line!") do set "YTURL=%%a"
    )
)

:: Extract only the URL (remove error text)
for /f "tokens=6 delims= " %%x in ("!YTURL!") do set "YTURL=%%x"

:: Make sure the Music folder exists
if not exist "Music" (
    mkdir "Music"
)

:: Download using yt-dlp into Music\[Artist]\ folder, extract audio as mp3, embed thumbnail
yt-dlp "!YTURL!" --cookies music.youtube.com_cookies.txt -o "Download\Music\%%(artist)s\%%(title)s.%%(ext)s" --extract-audio --audio-format mp3 --embed-thumbnail -v

pause
