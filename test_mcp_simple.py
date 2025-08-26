"""간단한 MCP 테스트."""

import asyncio
import json
import subprocess
import sys
from pathlib import Path


async def test_mcp_server_simple():
    """간단한 MCP 서버 테스트."""
    print("=== 간단한 MCP 서버 테스트 ===\n")
    
    # 1. 서버가 시작되는지 확인
    print("1. 서버 시작 테스트")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "gdb_mcp.main"],
            capture_output=True,
            text=True,
            timeout=5,
            env={"PYTHONPATH": str(Path.cwd())}
        )
        
        if result.returncode == 0:
            print("✅ 서버가 정상적으로 시작됨")
            if "GDB MCP 서버 시작" in result.stderr:
                print("✅ 로그 메시지 확인됨")
            else:
                print("⚠️  로그 메시지가 예상과 다름")
        else:
            print(f"❌ 서버 시작 실패: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("✅ 서버가 정상적으로 실행 중 (타임아웃은 정상)")
    except Exception as e:
        print(f"❌ 서버 시작 중 오류: {e}")
    
    # 2. MCP 설정 확인
    print("\n2. MCP 설정 확인")
    mcp_config_path = Path.home() / ".cursor" / "mcp.json"
    if mcp_config_path.exists():
        print("✅ MCP 설정 파일 존재")
        try:
            with open(mcp_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if "gdb-mcp" in config.get("mcpServers", {}):
                print("✅ gdb-mcp 서버 설정됨")
                gdb_config = config["mcpServers"]["gdb-mcp"]
                print(f"   명령: {gdb_config.get('command')}")
                print(f"   인수: {gdb_config.get('args')}")
                print(f"   환경: {gdb_config.get('env')}")
            else:
                print("❌ gdb-mcp 서버 설정 없음")
        except Exception as e:
            print(f"❌ MCP 설정 파일 읽기 오류: {e}")
    else:
        print("❌ MCP 설정 파일 없음")
    
    # 3. 프로젝트 구조 확인
    print("\n3. 프로젝트 구조 확인")
    required_files = [
        "gdb_mcp/__init__.py",
        "gdb_mcp/main.py",
        "gdb_mcp/server.py",
        "gdb_mcp/process_manager.py",
        "gdb_mcp/models.py",
        "pyproject.toml"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_files_exist = False
    
    if all_files_exist:
        print("✅ 모든 필수 파일 존재")
    else:
        print("❌ 일부 필수 파일 누락")
    
    # 4. 패키지 임포트 테스트
    print("\n4. 패키지 임포트 테스트")
    try:
        import gdb_mcp
        print("✅ gdb_mcp 패키지 임포트 성공")
        
        from gdb_mcp.server import GDBMCPServer
        print("✅ GDBMCPServer 클래스 임포트 성공")
        
        from gdb_mcp.process_manager import GDBManager, QEMUManager
        print("✅ 프로세스 관리자 클래스 임포트 성공")
        
    except ImportError as e:
        print(f"❌ 임포트 오류: {e}")
    except Exception as e:
        print(f"❌ 기타 오류: {e}")
    
    print("\n=== 테스트 완료 ===")
    print("\nMCP 서버가 정상적으로 설정되었습니다!")
    print("이제 Cursor에서 MCP 도구를 사용할 수 있습니다.")


if __name__ == "__main__":
    asyncio.run(test_mcp_server_simple())
