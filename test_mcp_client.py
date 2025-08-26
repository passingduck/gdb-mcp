"""MCP 클라이언트 테스트."""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any


class MCPClient:
    """간단한 MCP 클라이언트."""
    
    def __init__(self, server_cmd: list):
        self.server_cmd = server_cmd
        self.process = None
        self.request_id = 1
    
    async def start(self):
        """서버를 시작합니다."""
        self.process = subprocess.Popen(
            self.server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("MCP 서버 시작됨")
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """요청을 보냅니다."""
        if not self.process:
            raise RuntimeError("서버가 시작되지 않았습니다")
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        self.request_id += 1
        
        # 요청 전송
        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str)
        self.process.stdin.flush()
        
        # 응답 읽기
        response_line = self.process.stdout.readline()
        if response_line:
            return json.loads(response_line)
        else:
            return {"error": "응답 없음"}
    
    async def stop(self):
        """서버를 중지합니다."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("MCP 서버 중지됨")


async def test_mcp_server():
    """MCP 서버 테스트."""
    print("MCP 서버 테스트 시작...")
    
    # 클라이언트 생성
    client = MCPClient([sys.executable, "-m", "gdb_mcp.main"])
    
    try:
        # 서버 시작
        await client.start()
        
        # 초기화
        print("1. 서버 초기화...")
        init_response = await client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        print(f"초기화 응답: {init_response}")
        
        # 도구 목록 요청
        print("\n2. 도구 목록 요청...")
        tools_response = await client.send_request("tools/list")
        print(f"도구 목록: {tools_response}")
        
        # GDB 상태 확인
        print("\n3. GDB 상태 확인...")
        status_response = await client.send_request("tools/call", {
            "name": "gdb_status",
            "arguments": {}
        })
        print(f"GDB 상태: {status_response}")
        
    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 서버 중지
        await client.stop()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
