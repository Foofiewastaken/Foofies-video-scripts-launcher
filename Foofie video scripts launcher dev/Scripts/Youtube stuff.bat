@echo off
setlocal enabledelayedexpansion

:loop
echo For age gated videos, ensure you have exported cookies from your browser to 'www.youtube.com_cookies.txt'.
echo for info on how to do this, open tips in the main GUI.
echo cookies expire after a while, so you may need to refresh them periodically.
echo =========================
set /p url=Paste YouTube URL (or type EXIT to quit) and press Enter: 
if /i "!url!"=="EXIT" goto end

:menu
cls
echo =========================
echo YouTube Download Options
echo =========================
echo 1. Video only (no sound)
echo 2. Audio only (mp3)
echo 3. Video + Audio (mp4)
echo 4. Copy direct video URL to clipboard
echo =========================
set /p choice=Select an option [1-4]: 

set cookies=www.youtube.com_cookies.txt

if "!choice!"=="1" (
    yt-dlp -f "bestvideo/best" --cookies %cookies% -o "Downloads/YT vids no sound/%%(title)s.%%(ext)s" !url!
) else if "!choice!"=="2" (
    yt-dlp -f "bestaudio/best" --extract-audio --audio-format mp3 --audio-quality 0 --cookies %cookies% -o "Downloads/YT sounds/%%(title)s.%%(ext)s" !url!
) else if "!choice!"=="3" (
    yt-dlp -f "bestvideo+bestaudio/best" --merge-output-format mp4 --cookies %cookies% -o "Downloads/YT vids/%%(title)s.%%(ext)s" !url!
) else if "!choice!"=="4" (
    rem Get direct video URL and copy to clipboard
    yt-dlp --no-playlist -f mp4 --get-url --cookies %cookies% "!url!" > temp_url.txt
    for /f "usebackq delims=" %%a in ("temp_url.txt") do (
        set "direct_url=%%a"
        goto copyurl
    )
    :copyurl
    echo !direct_url! > temp_url_quoted.txt
    powershell -Command "Get-Content temp_url_quoted.txt | Set-Clipboard"
    del temp_url.txt temp_url_quoted.txt
    echo The full direct video URL has been copied to the clipboard.
) else (
    echo Invalid choice, try again.
    pause
    goto menu
)

echo.
echo Done!
pause
goto loop

:end
echo Exiting...
pause
