@echo off
if "%~1"=="" (
  echo version is required for the release build
  echo Usage: %~0 ^<version^>
  goto :EOF
)
echo Building version %~1
docker build . -t littleorange666/book_reader:%~1 --no-cache || exit /b 1
echo Pushing version %~1
docker push littleorange666/book_reader:%~1
echo Building latest
docker build . -t littleorange666/book_reader:latest || exit /b 1
echo Pushing latest
docker push littleorange666/book_reader:latest