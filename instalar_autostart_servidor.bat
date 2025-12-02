@echo off
echo === Instalando auto-start do SERVIDOR + CLIENTE (esta maquina sera o servidor) ===

set PROJETO=%~dp0
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

REM 1) criar iniciar_servidor.bat
echo @echo off > "%PROJETO%\iniciar_servidor.bat"
echo cd /d "%PROJETO%" >> "%PROJETO%\iniciar_servidor.bat"
echo python servidor_arduino.py >> "%PROJETO%\iniciar_servidor.bat"
echo pause >> "%PROJETO%\iniciar_servidor.bat"

REM 2) criar iniciar_cliente_servidor.vbs (cliente invisivel, com delay)
echo Set objShell = CreateObject("WScript.Shell") > "%PROJETO%\iniciar_cliente_servidor.vbs"
echo WScript.Sleep 10000 >> "%PROJETO%\iniciar_cliente_servidor.vbs"
echo objShell.Run "python %PROJETO%\cliente.py", 0, False >> "%PROJETO%\iniciar_cliente_servidor.vbs"

REM 3) copiar para Startup
copy "%PROJETO%\iniciar_servidor.bat" "%STARTUP%\iniciar_servidor.bat" >nul
copy "%PROJETO%\iniciar_cliente_servidor.vbs" "%STARTUP%\iniciar_cliente_servidor.vbs" >nul

echo.
echo [OK] Auto-start instalado para este PC como SERVIDOR+CLIENTE.
echo   - Servidor em iniciar_servidor.bat
echo   - Cliente em iniciar_cliente_servidor.vbs
echo.
pause
