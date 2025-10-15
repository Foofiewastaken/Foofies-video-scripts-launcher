@echo off
setlocal enabledelayedexpansion

:loop
set /p url=Paste YouTube URL (or type EXIT to quit) and press Enter (For this script to work, you need to download FFMPEG):

if /i "!url!"=="EXIT" goto end

yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 --cookies www.youtube.com_cookies.txt -o "Downloads/YT vids/%%(title)s.%%(ext)s" !url!

goto loop

:end
echo Exiting...
pause
