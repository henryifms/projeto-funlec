@echo off
echo === Instalando auto-start do CLIENTE (esta maquina NAO sera servidor) ===

set PROJETO=%~dp0
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

REM 1) pedir o IP do servidor (ou voce pode editar direto no cliente.py antes)
set /p SERVER_IP=Digite o IP do servidor (ex: 10.8.33.158): 

REM 2) ajustar temporariamente o cliente.py com esse IP (simples: so registrar em um .txt)
echo %SERVER_IP% > "%PROJETO%\server_ip_config.txt"

REM 3) criar iniciar_cliente.vbs (cliente invisivel)
echo Set objShell = CreateObject("WScript.Shell") > "%PROJETO%\iniciar_cliente.vbs"
echo objShell.Run "python %PROJETO%\cliente.py", 0, False >> "%PROJETO%\iniciar_cliente.vbs"

REM 4) copiar para Startup
copy "%PROJETO%\iniciar_cliente.vbs" "%STARTUP%\iniciar_cliente.vbs" >nul

echo.
echo [ATENCAO] Certifique-se de que, no cliente.py, a variavel SERVER_IP esta igual a %SERVER_IP%.
echo.
echo [OK] Auto-start instalado para este PC como CLIENTE.
echo.
pause
