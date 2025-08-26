"""GDB MCP 서버 기본 사용 예제."""

import asyncio
import json
from pathlib import Path

# 간단한 테스트 프로그램 생성
def create_test_program():
    """테스트용 C 프로그램을 생성합니다."""
    test_c = """
#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    int x = 42;
    printf("x = %d\\n", x);
    return 0;
}
"""
    
    test_file = Path("test_program.c")
    test_file.write_text(test_c)
    
    # 컴파일
    import subprocess
    subprocess.run(["gcc", "-g", "-o", "test_program", "test_program.c"], check=True)
    
    return "test_program"


async def test_gdb_mcp():
    """GDB MCP 서버 테스트."""
    print("GDB MCP 서버 테스트 시작...")
    
    # 테스트 프로그램 생성
    test_program = create_test_program()
    print(f"테스트 프로그램 생성: {test_program}")
    
    # 여기서는 실제 MCP 클라이언트 연결을 시뮬레이션합니다
    # 실제 사용시에는 MCP 클라이언트 라이브러리를 사용해야 합니다
    
    print("\n=== GDB MCP 서버 사용 예제 ===")
    print("1. GDB 시작:")
    print('   await client.call_tool("gdb_start", {"target": "test_program"})')
    
    print("\n2. 브레이크포인트 설정:")
    print('   await client.call_tool("gdb_execute", {"command": "break main"})')
    
    print("\n3. 프로그램 실행:")
    print('   await client.call_tool("gdb_execute", {"command": "run"})')
    
    print("\n4. 변수 값 확인:")
    print('   await client.call_tool("gdb_execute", {"command": "print x"})')
    
    print("\n5. GDB 상태 확인:")
    print('   await client.call_tool("gdb_status", {})')
    
    print("\n6. GDB 종료:")
    print('   await client.call_tool("process_stop", {"process_type": "gdb"})')
    
    print("\n=== QEMU 사용 예제 ===")
    print("1. QEMU 시작 (x86_64):")
    print('   await client.call_tool("qemu_start", {')
    print('       "arch": "x86_64",')
    print('       "kernel": "vmlinux",')
    print('       "options": ["-s", "-S"]')
    print('   })')
    
    print("\n2. GDB로 QEMU에 연결:")
    print('   await client.call_tool("gdb_start", {')
    print('       "remote": "localhost:1234"')
    print('   })')
    
    # 테스트 파일 정리
    for file in ["test_program.c", "test_program"]:
        Path(file).unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(test_gdb_mcp())
