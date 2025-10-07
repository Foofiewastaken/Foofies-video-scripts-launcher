@echo off
setlocal enabledelayedexpansion

:loop
set "url="
set /p url=Paste Spotify URL (or type EXIT to quit) and press Enter: 

if /i "!url!"=="EXIT" goto end

:: Run spotdl with auto selection (no numeric prompt)
cmd /c echo 1 | spotdl "!url!" > spotdl_output.txt 2>&1

:: Initialize variable for YouTube Music link
set "ytmusic_link="

:: Look for YouTube Music link in output
for /f "usebackq tokens=*" %%a in ("spotdl_output.txt") do (
    set "line=%%a"
    echo !line! | findstr "https://music.youtube.com/watch?v=" >nul
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

:: Copy the link to clipboard
echo !ytmusic_link! | clip

echo The YouTube Music link has been copied to the clipboard.

:: Clean up
del spotdl_output.txt

goto loop

:end
echo Exiting...
pause
