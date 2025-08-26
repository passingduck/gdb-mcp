"""GDB MCP 서버 테스트 스크립트."""

import asyncio
import json
import subprocess
import sys
from pathlib import Path


async def test_server_communication():
    """서버와의 통신을 테스트합니다."""
    print("GDB MCP 서버 테스트 시작...")
    
    # 서버 프로세스 시작
    server_process = subprocess.Popen(
        [sys.executable, "-m", "gdb_mcp.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # 초기화 메시지 전송
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("초기화 메시지 전송...")
        server_process.stdin.write(json.dumps(init_message) + "\n")
        server_process.stdin.flush()
        
        # 응답 읽기
        response = server_process.stdout.readline()
        print(f"서버 응답: {response}")
        
        # 도구 목록 요청
        list_tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("도구 목록 요청...")
        server_process.stdin.write(json.dumps(list_tools_message) + "\n")
        server_process.stdin.flush()
        
        response = server_process.stdout.readline()
        print(f"도구 목록 응답: {response}")
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
    finally:
        # 서버 종료
        server_process.terminate()
        server_process.wait()
        print("서버 종료됨")


if __name__ == "__main__":
    asyncio.run(test_server_communication())
