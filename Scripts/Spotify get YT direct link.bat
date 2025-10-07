@echo off
setlocal enabledelayedexpansion

:loop
set "url="
set /p url=Paste Spotify URL (or type EXIT to quit) and press Enter: 

if /i "!url!"=="EXIT" goto end

:: Run spotdl in isolated cmd session
cmd /c spotdl "%url%" > spotdl_output.txt 2>&1

:: Initialize variable to hold YouTube Music link
set "ytmusic_link="

:: Search for YouTube Music link in spotdl output file
for /f "usebackq tokens=*" %%a in ("spotdl_output.txt") do (
    set "line=%%a"
    echo !line! | findstr /c:"https://music.youtube.com/watch?v=" >nul
    if !errorlevel! == 0 (
        for /f "tokens=1" %%b in ("!line!") do (
            set "ytmusic_link=%%b"
            goto got_link
        )
    )
)

:got_link
if not defined ytmusic_link (
    echo Could not find YouTube Music link in spotdl output.
    del spotdl_output.txt
    goto loop
)

echo Found YouTube Music link: !ytmusic_link!

:: Use yt-dlp to get direct playable URL from YouTube Music link
cmd /c yt-dlp -f mp4 --get-url "!ytmusic_link!" > temp_url.txt

set "direct_url="

for /f "usebackq delims=" %%u in ("temp_url.txt") do (
    set "direct_url=%%u"
    goto copyurl
)

:copyurl
if not defined direct_url (
    echo Failed to get direct URL from yt-dlp.
    del temp_url.txt spotdl_output.txt
    goto loop
)

:: Copy direct URL to clipboard
echo !direct_url! > temp_url_quoted.txt
powershell -Command "Get-Content temp_url_quoted.txt | Set-Clipboard"

echo The direct playable URL has been copied to the clipboard.

:: Clean up temp files
del temp_url.txt temp_url_quoted.txt spotdl_output.txt

goto loop

:end
echo Exiting...
pause
