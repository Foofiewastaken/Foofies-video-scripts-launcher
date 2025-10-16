@echo off
setlocal enabledelayedexpansion

:loop
set choice=1
cls
echo  For age gated videos, ensure you have exported cookies from your browser to 'www.youtube.com_cookies.txt'.
echo  for info on how to do this, open tips in the main GUI.
echo  cookies expire after a while, so you may need to refresh them periodically.
echo ============================================================================
echo  Paste Youtube link below
echo  (or type EXIT to quit)
echo ============================================================================
set /p url=Youtube URL: 
if /i "!url!"=="EXIT" goto exit
else if /i "!url!"=="exit" goto exit
cls
else if /i "!url!"=="Exit" goto exit
cls
:menu
cls
echo ========================================
echo  YouTube Download Options
echo ========================================
echo  1. Video + Audio (mp4) (DEFAULT)
echo  2. Audio only (mp3)
echo  3. Video only (no sound)
echo  4. Copy direct video URL to clipboard
echo  0. Go back
echo ========================================
set /p choice=Select an option [1-4]: 
cls
set cookies=www.youtube.com_cookies.txt
cls
if "!choice!"=="1" (
cls
    yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 --cookies %cookies% -o "Downloads/YT vids/%%(title)s.%%(ext)s" !url!
) else if "!choice!"=="2" (
cls
    yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3 --audio-quality 0 --cookies %cookies% -o "Downloads/YT sounds/%%(title)s.%%(ext)s" !url!
) else if "!choice!"=="3" (
cls
    yt-dlp -f "bestvideo/best" --cookies %cookies% -o "Downloads/YT vids no sound/%%(title)s.%%(ext)s" !url!
) else if "!choice!"=="0" (
cls
goto loop
)
cls

 else if "!choice!"=="4" (
    rem Get direct video URL and copy to clipboard
    yt-dlp --no-playlist -t mp4 --get-url --cookies %cookies% "!url!" > temp_url.txt
    for /f "usebackq delims=" %%a in ("temp_url.txt") do (
        set "direct_url=%%a"
        goto copyurl
    )
    :copyurl
	cls
    echo !direct_url! > temp_url_quoted.txt
	cls
    powershell -Command "Get-Content temp_url_quoted.txt | Set-Clipboard"
	cls
    del temp_url.txt temp_url_quoted.txt
	cls
    echo The full direct video URL has been copied to the clipboard.
	timeout /t 5 >nul
	goto loop
) else (
cls
    yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 --cookies %cookies% -o "Downloads/YT vids/%%(title)s.%%(ext)s" !url!
)
cls
echo.
echo Done!
timeout /t 5 >nul
goto loop

:exit
echo Exiting...
timeout /t 1 >nul
exit