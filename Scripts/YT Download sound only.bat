@echo off
setlocal enabledelayedexpansion
:loop
set /p url=Paste YouTube URL (or type EXIT) and press Enter: 
if /i "!url!"=="EXIT" goto end
yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3 --audio-quality 0 --cookies www.youtube.com_cookies.txt -o "Downloads/YT sounds/%%(title)s.%%(ext)s" %url%
goto loop

:exit
echo Exitting...
pause