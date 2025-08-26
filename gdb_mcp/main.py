"""GDB MCP 서버 메인 실행 파일."""

import asyncio
import logging
import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from gdb_mcp.server import GDBMCPServer


def setup_logging():
    """로깅 설정을 초기화합니다."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr),
        ]
    )


async def main():
    """메인 함수."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("GDB MCP 서버 시작...")
        server = GDBMCPServer()
        await server.run()
    except KeyboardInterrupt:
        logger.info("서버가 사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"서버 실행 중 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
