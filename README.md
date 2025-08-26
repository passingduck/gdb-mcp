# GDB MCP Server

GDB와 QEMU 프로세스를 관리하는 MCP (Model Context Protocol) 서버입니다.

## 기능

- GDB 프로세스 관리 및 제어
- QEMU 시스템 에뮬레이터 실행 및 관리
- LLM과의 인터페이스를 통한 GDB 명령 실행
- GDB 출력 및 상태 스트리밍

## 설치

```bash
pip install -e .
```

## 사용법

### 서버 실행

```bash
python -m gdb_mcp.main
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

