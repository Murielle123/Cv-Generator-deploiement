@echo off

REM Check if the image exists
docker inspect cv-app > nul 2>&1
if %errorlevel% equ 0 (
    echo L'image existe. Lancement de l'application...
) else (
    echo L'image n'existe pas. Construction de l'image...
    docker build -t cv-app .
    echo Construction de l'image terminée. Lancement de l'application...
)
REM Running image
docker run -d -p 8501:8501 cv-app  
echo Fin de l'installation. Ouverture dans le navigateur...

REM Lancement de l'application
start "" "http://localhost:8501"