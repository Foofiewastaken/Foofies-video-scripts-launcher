@echo off
setlocal enabledelayedexpansion
:loop
set /p url=Paste YouTube URL (or type EXIT to quit) and press Enter: 
if /i "!url!"=="EXIT" goto end
yt-dlp -f "bestvideo/best" --cookies www.youtube.com_cookies.txt -o "Downloads/YT vids no sound/%%(title)s.%%(ext)s" %url%
goto loop
:end
echo Exiting...
pause