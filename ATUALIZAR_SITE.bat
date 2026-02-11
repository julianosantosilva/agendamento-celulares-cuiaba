@echo off
echo ================================================
echo   ATUALIZANDO SITE PARA PORTAL DE NOTICIAS IA
echo ================================================
echo.
cd /d "%~dp0"

echo Enviando para GitHub...
git push origin main

echo.
echo ================================================
echo   PRONTO! O Render vai atualizar automaticamente
echo ================================================
echo.
echo Aguarde 2-3 minutos e acesse:
echo https://agendamento-celulares-cuiaba.onrender.com
echo.
pause
