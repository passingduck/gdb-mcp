"""간단한 테스트 스크립트."""

import asyncio
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)

async def simple_test():
    """간단한 테스트."""
    print("간단한 테스트 시작...")
    
    try:
        from gdb_mcp.process_manager import GDBManager
        print("GDBManager 임포트 성공")
        
        gdb_manager = GDBManager()
        print("GDBManager 인스턴스 생성 성공")
        
        # 상태 확인
        status = await gdb_manager.get_status()
        print(f"GDB 상태: {status}")
        
    except Exception as e:
        print(f"오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(simple_test())
