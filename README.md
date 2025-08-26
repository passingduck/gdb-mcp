# GDB MCP Server

GDB와 QEMU 프로세스를 관리하는 MCP (Model Context Protocol) 서버입니다.

## 기능

- GDB 프로세스 관리 및 제어
- QEMU 시스템 에뮬레이터 실행 및 관리
- LLM과의 인터페이스를 통한 GDB 명령 실행
- GDB 출력 및 상태 스트리밍
- **Windows와 Linux 환경 모두 지원**

## 설치

```bash
pip install -e .
```

## 사용법

### 서버 실행

MCP 서버는 stdio를 통해 통신하므로 직접 실행하면 바로 종료됩니다. 
실제 사용시에는 MCP 클라이언트(예: Claude Desktop, Cursor 등)에서 설정하여 사용합니다.

```bash
# 서버가 정상적으로 시작되는지 확인 (바로 종료됨)
python -m gdb_mcp.main
```

### MCP 클라이언트 설정

MCP 클라이언트에서 다음과 같이 설정하세요:

```json
{
  "mcpServers": {
    "gdb-mcp": {
      "command": "python",
      "args": ["-m", "gdb_mcp.main"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

### MCP 클라이언트에서 사용

```python
# GDB 시작
await client.call_tool("gdb_start", {"target": "my_program"})

# GDB 명령 실행
await client.call_tool("gdb_execute", {"command": "break main"})

# QEMU 시작
await client.call_tool("qemu_start", {
    "arch": "x86_64",
    "kernel": "vmlinux",
    "options": ["-s", "-S"]
})

# GDB 상태 확인
await client.call_tool("gdb_status", {})

# 프로세스 중지
await client.call_tool("process_stop", {"process_type": "gdb"})
```

### 테스트

```bash
# 기본 테스트
python simple_test.py

# 프로세스 관리자 테스트
python test_process_manager.py

# 전체 데모 실행
python demo.py
```

## Cortex-M7 Hello World 예제

Cortex-M7 마이크로컨트롤러용 Hello World 예제가 포함되어 있습니다.

### 예제 위치
```
cortex_m7_hello_world/
├── main.c              # 메인 프로그램 (UART Hello World)
├── startup.c           # 시작 코드 및 벡터 테이블
├── stm32f7xx.ld        # 링커 스크립트
├── Makefile            # 빌드 스크립트 (Windows/Linux 지원)
├── qemu_run.sh         # QEMU 실행 스크립트 (Linux/macOS)
├── qemu_run.bat        # QEMU 실행 스크립트 (Windows)
├── gdb_debug.sh        # GDB 디버깅 스크립트 (Linux/macOS)
├── gdb_debug.bat       # GDB 디버깅 스크립트 (Windows)
├── test_with_mcp.py    # MCP 서버 테스트
└── README.md           # 상세 문서
```

### 빌드 및 실행

#### Linux/macOS
```bash
# 프로젝트 디렉토리로 이동
cd cortex_m7_hello_world

# 빌드 (ARM GCC 도구체인 필요)
make all

# QEMU 시뮬레이션
./qemu_run.sh
# 또는
make qemu

# GDB 디버깅 (QEMU 실행 후 다른 터미널에서)
./gdb_debug.sh
# 또는
make gdb-debug
```

#### Windows
```cmd
# 프로젝트 디렉토리로 이동
cd cortex_m7_hello_world

# 빌드 (ARM GCC 도구체인 필요)
make all

# QEMU 시뮬레이션
qemu_run.bat
# 또는
make qemu

# GDB 디버깅 (QEMU 실행 후 다른 터미널에서)
gdb_debug.bat
# 또는
make gdb-debug
```

### MCP 서버와 함께 사용

```python
# QEMU로 Cortex-M7 시뮬레이션 시작
await client.call_tool("qemu_start", {
    "arch": "arm",
    "gdb_stub": True,
    "options": ["-M", "mps2-an385", "-cpu", "cortex-m3"]
})

# GDB로 디버깅 시작
await client.call_tool("gdb_start", {
    "target": "cortex_m7_hello_world.elf",
    "remote": "localhost:1234"
})

# 브레이크포인트 설정
await client.call_tool("gdb_execute", {"command": "break main"})

# 프로그램 실행
await client.call_tool("gdb_execute", {"command": "continue"})
```

## 개발

```bash
# 개발 의존성 설치
pip install -e ".[dev]"

# 코드 포맷팅
black .
isort .

# 타입 체크
mypy .

# 테스트 실행
pytest
```

## 요구사항

### 필수 도구
- Python 3.8+
- ARM GCC 도구체인 (Cortex-M7 예제용)
- Make

### 선택 도구
- QEMU (시뮬레이션용)
- OpenOCD (실제 하드웨어 플래시용)
- ST-Link (STM32 디버깅용)

### Windows 특별 요구사항
- PowerShell 또는 CMD
- Windows Terminal (권장)
- Chocolatey 또는 MSYS2 (패키지 관리)

### Linux 특별 요구사항
- Bash shell
- GCC 및 Make
- udev 규칙 (USB 장치 접근용)

## 라이선스

MIT License

