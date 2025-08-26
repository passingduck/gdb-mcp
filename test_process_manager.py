"""프로세스 관리자 테스트 스크립트."""

import asyncio
import logging
from gdb_mcp.process_manager import GDBManager, QEMUManager

# 로깅 설정
logging.basicConfig(level=logging.INFO)


async def test_gdb_manager():
    """GDB 관리자 테스트."""
    print("=== GDB 관리자 테스트 ===")
    
    gdb_manager = GDBManager()
    
    # GDB 시작 테스트 (실제 GDB가 없으면 실패할 수 있음)
    print("1. GDB 시작 테스트...")
    try:
        success, error = await gdb_manager.start()
        print(f"   결과: {'성공' if success else '실패'}")
        if error:
            print(f"   오류: {error}")
    except Exception as e:
        print(f"   예외: {e}")
    
    # GDB 상태 확인
    print("2. GDB 상태 확인...")
    status = await gdb_manager.get_status()
    print(f"   실행 중: {status['running']}")
    print(f"   타겟: {status['target']}")
    
    # GDB 중지
    print("3. GDB 중지...")
    success, error = await gdb_manager.stop()
    print(f"   결과: {'성공' if success else '실패'}")


async def test_qemu_manager():
    """QEMU 관리자 테스트."""
    print("\n=== QEMU 관리자 테스트 ===")
    
    qemu_manager = QEMUManager()
    
    # QEMU 시작 테스트 (실제 QEMU가 없으면 실패할 수 있음)
    print("1. QEMU 시작 테스트...")
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
    
    # QEMU 상태 확인
    print("2. QEMU 상태 확인...")
    running = qemu_manager.is_running()
    print(f"   실행 중: {running}")
    
    # QEMU 중지
    print("3. QEMU 중지...")
    success, error = await qemu_manager.stop()
    print(f"   결과: {'성공' if success else '실패'}")


async def main():
    """메인 테스트 함수."""
    print("GDB MCP 프로세스 관리자 테스트 시작...\n")
    
    await test_gdb_manager()
    await test_qemu_manager()
    
    print("\n테스트 완료!")


if __name__ == "__main__":
    asyncio.run(main())
