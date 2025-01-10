@echo off
setlocal

:: Set default log file name and event type
set "LogFileName=EventLog.txt"
set "EventType=Default Event"

:: Check if parameters were passed, and override default values
if not "%1"=="" set "EventType=%1"

:: Get the directory of the current script
set "ScriptDirectory=%~dp0"

:: Define the log file path
set "LogFilePath=%ScriptDirectory%%LogFileName%"

:: Ensure the directory exists
if not exist "%ScriptDirectory%" mkdir "%ScriptDirectory%"

:: Write the event to the log file
echo %date% %time%-%EventType% >> "%LogFilePath%"

:: Display the message for testing purposes
echo Event "%EventType%" logged to "%LogFilePath%"

endlocal
