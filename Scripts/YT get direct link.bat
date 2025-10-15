@echo off
setlocal enabledelayedexpansion
:loop
set /p url=Paste Youtube URL (or type EXIT to quit) and press Enter: 

if /i "!url!"=="EXIT" goto end

yt-dlp --no-playlist -f mp4 --get-url --cookies www.youtube.com_cookies.txt "%url%" > temp_url.txt

for /f "usebackq delims=" %%a in ("temp_url.txt") do (
    set "direct_url=%%a"
    goto copyurl
)

:copyurl
rem Echo the URL with quotes so & doesn't split it, then remove quotes with PowerShell before copying
echo !direct_url! > temp_url_quoted.txt
powershell -Command "Get-Content temp_url_quoted.txt | Set-Clipboard"
del temp_url.txt temp_url_quoted.txt

echo The full direct mp3 URL has been copied to the clipboard.
goto loop
:end
echo Exitting...
pause