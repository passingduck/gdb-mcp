"""MCP 통합 테스트."""

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path


class MCPIntegrationTest:
    """MCP 통합 테스트 클래스."""
    
    def __init__(self):
        self.process = None
        self.request_id = 1
    
    async def start_server(self):
        """서버를 시작합니다."""
        print("MCP 서버 시작 중...")
        
        # 현재 디렉토리를 PYTHONPATH에 추가
        current_dir = str(Path.cwd())
        
        self.process = subprocess.Popen(
            [sys.executable, "-m", "gdb_mcp.main"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={"PYTHONPATH": current_dir}
        )
        
        # 서버가 시작될 때까지 잠시 대기
        await asyncio.sleep(1)
        print("서버 시작됨")
    
    async def send_request(self, method: str, params: dict = None) -> dict:
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
        print(f"전송: {request_str.strip()}")
        
        try:
            self.process.stdin.write(request_str)
            self.process.stdin.flush()
            
            # 응답 읽기
            response_line = self.process.stdout.readline()
            if response_line:
                response = json.loads(response_line)
                print(f"응답: {json.dumps(response, indent=2, ensure_ascii=False)}")
                return response
            else:
                print("응답 없음")
                return {"error": "응답 없음"}
                
        except Exception as e:
            print(f"통신 오류: {e}")
            return {"error": str(e)}
    
    async def stop_server(self):
        """서버를 중지합니다."""
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            print("서버 중지됨")


async def test_mcp_integration():
    """MCP 통합 테스트."""
    print("=== MCP 통합 테스트 시작 ===\n")
    
    test = MCPIntegrationTest()
    
    try:
        # 1. 서버 시작
        await test.start_server()
        
        # 2. 초기화 테스트
        print("\n1. 초기화 테스트")
        init_response = await test.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        if "error" in init_response:
            print("❌ 초기화 실패")
            return
        else:
            print("✅ 초기화 성공")
        
        # 3. 도구 목록 테스트
        print("\n2. 도구 목록 테스트")
        tools_response = await test.send_request("tools/list")
        
        if "error" in tools_response:
            print("❌ 도구 목록 조회 실패")
        else:
            print("✅ 도구 목록 조회 성공")
            if "result" in tools_response and "tools" in tools_response["result"]:
                tools = tools_response["result"]["tools"]
                print(f"   발견된 도구 수: {len(tools)}")
                for tool in tools:
                    print(f"   - {tool['name']}: {tool['description']}")
        
        # 4. GDB 상태 테스트
        print("\n3. GDB 상태 테스트")
        status_response = await test.send_request("tools/call", {
            "name": "gdb_status",
            "arguments": {}
        })
        
        if "error" in status_response:
            print("❌ GDB 상태 조회 실패")
        else:
            print("✅ GDB 상태 조회 성공")
            if "result" in status_response:
                print(f"   결과: {status_response['result']}")
        
        # 5. QEMU 시작 테스트 (실제 QEMU가 없으면 실패할 수 있음)
        print("\n4. QEMU 시작 테스트")
        qemu_response = await test.send_request("tools/call", {
            "name": "qemu_start",
            "arguments": {
                "arch": "x86_64",
                "gdb_stub": True
            }
        })
        
        if "error" in qemu_response:
            print("❌ QEMU 시작 실패 (예상됨 - QEMU가 설치되지 않음)")
        else:
            print("✅ QEMU 시작 성공")
        
        print("\n=== 테스트 완료 ===")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await test.stop_server()


if __name__ == "__main__":
    asyncio.run(test_mcp_integration())
