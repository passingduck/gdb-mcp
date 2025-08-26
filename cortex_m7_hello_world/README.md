# Cortex-M7 Hello World 예제

STM32F7xx 시리즈 Cortex-M7 마이크로컨트롤러용 Hello World 예제입니다.

## 기능

- UART를 통한 "Hello World" 메시지 출력
- 사용자 입력 처리
- 카운터 증가 및 표시
- QEMU 시뮬레이션 지원
- GDB 디버깅 지원
- **Windows와 Linux 환경 모두 지원**

## 하드웨어 요구사항

- STM32F7xx 시리즈 마이크로컨트롤러
- UART 연결 (PA9: TX, PA10: RX)
- ST-Link 디버거 (선택사항)

## 소프트웨어 요구사항

### 필수 도구

1. **ARM GCC 도구체인**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install gcc-arm-none-eabi
   
   # Windows (MSYS2)
   pacman -S mingw-w64-x86_64-arm-none-eabi-gcc
   
   # Windows (Chocolatey)
   choco install gcc-arm-embedded
   
   # macOS
   brew install arm-none-eabi-gcc
   ```

2. **Make**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install make
   
   # Windows (MSYS2)
   pacman -S make
   
   # Windows (Chocolatey)
   choco install make
   
   # macOS
   brew install make
   ```

### 선택 도구

3. **QEMU** (시뮬레이션용)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install qemu-system-arm
   
   # Windows (MSYS2)
   pacman -S mingw-w64-x86_64-qemu
   
   # Windows (Chocolatey)
   choco install qemu
   
   # macOS
   brew install qemu
   ```

4. **OpenOCD** (실제 하드웨어 플래시용)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install openocd
   
   # Windows (MSYS2)
   pacman -S mingw-w64-x86_64-openocd
   
   # Windows (Chocolatey)
   choco install openocd
   
   # macOS
   brew install openocd
   ```

## 빌드 및 실행

### 1. 빌드

```bash
# 프로젝트 디렉토리로 이동
cd cortex_m7_hello_world

# 빌드
make all
```

빌드 결과:
- `cortex_m7_hello_world.elf` - ELF 실행 파일
- `cortex_m7_hello_world.bin` - 바이너리 파일 (플래시용)
- `cortex_m7_hello_world.hex` - HEX 파일

### 2. QEMU 시뮬레이션

#### Linux/macOS
```bash
# QEMU로 시뮬레이션 실행
./qemu_run.sh

# 또는 Makefile 사용
make qemu
```

#### Windows
```cmd
# QEMU로 시뮬레이션 실행
qemu_run.bat

# 또는 Makefile 사용
make qemu
```

#### 직접 실행
```bash
qemu-system-arm -M mps2-an385 -cpu cortex-m3 \
  -kernel cortex_m7_hello_world.elf \
  -nographic -serial mon:stdio -s -S
```

### 3. GDB 디버깅

#### Linux/macOS
```bash
# 터미널 1: QEMU 실행
./qemu_run.sh

# 터미널 2: GDB 디버깅
./gdb_debug.sh

# 또는 Makefile 사용
make gdb-debug
```

#### Windows
```cmd
# 터미널 1: QEMU 실행
qemu_run.bat

# 터미널 2: GDB 디버깅
gdb_debug.bat

# 또는 Makefile 사용
make gdb-debug
```

### 4. 실제 하드웨어 플래시

```bash
# ST-Link 연결 후 플래시
make flash

# 또는 OpenOCD 직접 사용
openocd -f interface/stlink.cfg -f target/stm32f7x.cfg \
  -c "program cortex_m7_hello_world.bin verify reset exit"
```

### 5. 시리얼 모니터

```bash
# 시리얼 포트 정보 확인
make monitor
```

#### Linux/macOS
```bash
# 실제 시리얼 연결
screen /dev/ttyUSB0 115200
# 또는
minicom -D /dev/ttyUSB0 -b 115200
```

#### Windows
```cmd
# PuTTY, Tera Term, HyperTerminal 등 사용
# 포트: COM3, COM4, COM5 등
# 보드레이트: 115200
```

## 프로젝트 구조

```
cortex_m7_hello_world/
├── main.c              # 메인 프로그램
├── startup.c           # 시작 코드 및 벡터 테이블
├── stm32f7xx.ld        # 링커 스크립트
├── Makefile            # 빌드 스크립트 (Windows/Linux 지원)
├── qemu_run.sh         # QEMU 실행 스크립트 (Linux/macOS)
├── qemu_run.bat        # QEMU 실행 스크립트 (Windows)
├── gdb_debug.sh        # GDB 디버깅 스크립트 (Linux/macOS)
├── gdb_debug.bat       # GDB 디버깅 스크립트 (Windows)
├── test_with_mcp.py    # MCP 서버 테스트
└── README.md           # 이 파일
```

## 코드 설명

### main.c
- UART 초기화 및 설정
- "Hello World" 메시지 출력
- 사용자 입력 처리
- 카운터 증가 및 표시

### startup.c
- Cortex-M7 벡터 테이블
- 리셋 핸들러
- 기본 인터럽트 핸들러들

### stm32f7xx.ld
- 메모리 맵 정의
- 섹션 배치
- 스택 설정

## UART 설정

- **Baud Rate**: 115200
- **Data Bits**: 8
- **Stop Bits**: 1
- **Parity**: None
- **Flow Control**: None
- **TX Pin**: PA9
- **RX Pin**: PA10

## 디버깅

### GDB 명령어 예제

```bash
# 타겟 연결
target remote localhost:1234

# 브레이크포인트 설정
break main
break uart_init

# 레지스터 확인
info registers

# 메모리 확인
x/16x 0x40011000

# 변수 확인
print counter

# 단계 실행
step
next
continue
```

### OpenOCD 명령어 예제

```bash
# 타겟 연결
openocd -f interface/stlink.cfg -f target/stm32f7x.cfg

# 프로그램 플래시
program cortex_m7_hello_world.bin verify reset

# 타겟 리셋
reset
```

## Makefile 사용법

```bash
# 모든 타겟 확인
make help

# 빌드
make all

# 정리
make clean

# QEMU 시뮬레이션 (OS 자동 감지)
make qemu

# GDB 디버깅 (OS 자동 감지)
make gdb-debug

# 시리얼 모니터 정보
make monitor
```

## 문제 해결

### 빌드 오류

1. **ARM GCC 도구체인이 설치되지 않음**
   ```bash
   # 도구체인 설치 확인
   arm-none-eabi-gcc --version
   ```

2. **Makefile 오류**
   ```bash
   # Make 버전 확인
   make --version
   ```

### 실행 오류

1. **QEMU 실행 실패**
   ```bash
   # QEMU 설치 확인
   qemu-system-arm --version
   ```

2. **GDB 연결 실패**
   - QEMU가 실행 중인지 확인
   - 포트 1234가 사용 가능한지 확인

### 하드웨어 문제

1. **UART 출력이 안됨**
   - 보드레이트 설정 확인 (115200)
   - TX/RX 핀 연결 확인
   - 전원 공급 확인

2. **플래시 실패**
   - ST-Link 연결 확인
   - OpenOCD 설정 확인
   - 보드 전원 확인

### Windows 특별 주의사항

1. **PowerShell 실행 정책**
   ```powershell
   # 스크립트 실행 허용
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **PATH 환경변수**
   - ARM GCC 도구체인이 PATH에 추가되었는지 확인
   - QEMU가 PATH에 추가되었는지 확인

3. **터미널 프로그램**
   - Windows Terminal, PowerShell, CMD 중 선택
   - WSL 사용 시 Linux 스크립트 사용 가능

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 기여

버그 리포트나 기능 요청은 이슈로 등록해주세요.
Pull Request도 환영합니다.
