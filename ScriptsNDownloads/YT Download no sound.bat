@echo off
:loop
set /p url=Paste YouTube URL (or type EXIT to quit) and press Enter: 
if /i "!url!"=="exit" goto end
yt-dlp -f "bestvideo/best" --cookies www.youtube.com_cookies.txt -o "YT vids no sound/%%(title)s.%%(ext)s" %url%
goto loop
:end
echo Exiting...
pause