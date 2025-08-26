@echo off
REM Cortex-M7 QEMU 시뮬레이션 스크립트 (Windows)

echo === Cortex-M7 Hello World QEMU 시뮬레이션 ===

REM 빌드 확인
if not exist "cortex_m7_hello_world.elf" (
    echo ELF 파일이 없습니다. 먼저 빌드하세요:
    echo make all
    pause
    exit /b 1
)

REM QEMU 명령어 구성
set QEMU_CMD=qemu-system-arm
set QEMU_OPTS=-M mps2-an385
set QEMU_OPTS=%QEMU_OPTS% -cpu cortex-m3
set QEMU_OPTS=%QEMU_OPTS% -kernel cortex_m7_hello_world.elf
set QEMU_OPTS=%QEMU_OPTS% -nographic
set QEMU_OPTS=%QEMU_OPTS% -serial mon:stdio
set QEMU_OPTS=%QEMU_OPTS% -semihosting
set QEMU_OPTS=%QEMU_OPTS% -s -S

echo QEMU 명령어: %QEMU_CMD% %QEMU_OPTS%
echo.
echo 시뮬레이션을 시작합니다...
echo 종료하려면 Ctrl+C를 누르세요.
echo.

REM QEMU 실행
%QEMU_CMD% %QEMU_OPTS%

echo.
echo QEMU 시뮬레이션이 종료되었습니다.
pause
