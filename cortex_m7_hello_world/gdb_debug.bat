@echo off
REM Cortex-M7 GDB 디버깅 스크립트 (Windows)

echo === Cortex-M7 Hello World GDB 디버깅 ===

REM 빌드 확인
if not exist "cortex_m7_hello_world.elf" (
    echo ELF 파일이 없습니다. 먼저 빌드하세요:
    echo make all
    pause
    exit /b 1
)

REM GDB 명령어 구성
set GDB_CMD=arm-none-eabi-gdb
set GDB_OPTS=--tui
set GDB_SCRIPT=gdb_commands.gdb

REM GDB 명령어 스크립트 생성
echo # GDB 초기화 명령어들 > %GDB_SCRIPT%
echo set architecture arm >> %GDB_SCRIPT%
echo set endian little >> %GDB_SCRIPT%
echo set target-charset ASCII >> %GDB_SCRIPT%
echo. >> %GDB_SCRIPT%
echo # 타겟 연결 (QEMU GDB 스텁) >> %GDB_SCRIPT%
echo target remote localhost:1234 >> %GDB_SCRIPT%
echo. >> %GDB_SCRIPT%
echo # 프로그램 로드 >> %GDB_SCRIPT%
echo load >> %GDB_SCRIPT%
echo. >> %GDB_SCRIPT%
echo # 브레이크포인트 설정 >> %GDB_SCRIPT%
echo break main >> %GDB_SCRIPT%
echo break uart_init >> %GDB_SCRIPT%
echo break uart_putchar >> %GDB_SCRIPT%
echo. >> %GDB_SCRIPT%
echo # 레지스터 표시 >> %GDB_SCRIPT%
echo layout regs >> %GDB_SCRIPT%
echo. >> %GDB_SCRIPT%
echo # 소스 코드 표시 >> %GDB_SCRIPT%
echo layout src >> %GDB_SCRIPT%
echo. >> %GDB_SCRIPT%
echo # 실행 >> %GDB_SCRIPT%
echo continue >> %GDB_SCRIPT%

echo GDB 명령어: %GDB_CMD% %GDB_OPTS% -x %GDB_SCRIPT% cortex_m7_hello_world.elf
echo.
echo GDB 디버깅을 시작합니다...
echo QEMU가 실행 중이어야 합니다 (qemu_run.bat 실행 후).
echo.

REM GDB 실행
%GDB_CMD% %GDB_OPTS% -x %GDB_SCRIPT% cortex_m7_hello_world.elf

REM 임시 파일 정리
if exist %GDB_SCRIPT% del %GDB_SCRIPT%

echo.
echo GDB 디버깅이 종료되었습니다.
pause
