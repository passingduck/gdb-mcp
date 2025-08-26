"""GDB MCP 서버 데모."""

import asyncio
import logging
from gdb_mcp.process_manager import GDBManager, QEMUManager

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


async def demo_gdb_operations():
    """GDB 작업 데모."""
    print("=== GDB MCP 서버 데모 ===\n")
    
    gdb_manager = GDBManager()
    
    print("1. GDB 상태 확인")
    status = await gdb_manager.get_status()
    print(f"   실행 중: {status['running']}")
    print(f"   타겟: {status['target']}")
    print(f"   브레이크포인트 수: {len(status['breakpoints'])}")
    
    print("\n2. GDB 시작 시도 (GDB가 설치되어 있지 않으면 실패)")
    try:
        success, error = await gdb_manager.start()
        print(f"   결과: {'성공' if success else '실패'}")
        if error:
            print(f"   오류: {error}")
    except Exception as e:
        print(f"   예외: {e}")
    
    print("\n3. GDB 상태 재확인")
    status = await gdb_manager.get_status()
    print(f"   실행 중: {status['running']}")
    
    print("\n4. GDB 중지")
    success, error = await gdb_manager.stop()
    print(f"   결과: {'성공' if success else '실패'}")


async def demo_qemu_operations():
    """QEMU 작업 데모."""
    print("\n=== QEMU 작업 데모 ===\n")
    
    qemu_manager = QEMUManager()
    
    print("1. QEMU 시작 시도 (QEMU가 설치되어 있지 않으면 실패)")
    try:
        success, error = await qemu_manager.start("x86_64", gdb_stub=True)
        print(f"   결과: {'성공' if success else '실패'}")
        if error:
            print(f"   오류: {error}")
        else:
            print(f"   PID: {qemu_manager.pid}")
            print(f"   포트: {qemu_manager.port}")
    except Exception as e:
        print(f"   예외: {e}")
    
    print("\n2. QEMU 상태 확인")
    running = qemu_manager.is_running()
    print(f"   실행 중: {running}")
    
    print("\n3. QEMU 중지")
    success, error = await qemu_manager.stop()
    print(f"   결과: {'성공' if success else '실패'}")


async def demo_mcp_tools():
    """MCP 도구 데모."""
    print("\n=== MCP 도구 데모 ===\n")
    
    print("사용 가능한 MCP 도구들:")
    tools = [
        ("gdb_start", "GDB 디버거를 시작합니다"),
        ("gdb_execute", "GDB 명령을 실행합니다"),
        ("gdb_status", "GDB 상태를 조회합니다"),
        ("qemu_start", "QEMU 에뮬레이터를 시작합니다"),
        ("process_stop", "프로세스를 중지합니다")
    ]
    
    for i, (name, description) in enumerate(tools, 1):
        print(f"{i}. {name}: {description}")
    
    print("\n사용 예제:")
    print("  await client.call_tool('gdb_start', {'target': 'my_program'})")
    print("  await client.call_tool('gdb_execute', {'command': 'break main'})")
    print("  await client.call_tool('qemu_start', {'arch': 'x86_64'})")


async def main():
    """메인 데모 함수."""
    print("GDB MCP 서버 데모 시작...\n")
    
    await demo_gdb_operations()
    await demo_qemu_operations()
    await demo_mcp_tools()
    
    print("\n=== 데모 완료 ===")
    print("\n실제 사용시에는 MCP 클라이언트에서 설정하여 사용하세요.")
    print("예: Claude Desktop, Cursor 등의 MCP 클라이언트")


if __name__ == "__main__":
    asyncio.run(main())
