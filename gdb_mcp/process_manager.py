"""GDB와 QEMU 프로세스 관리 모듈."""

import asyncio
import os
import signal
import subprocess
import time
from typing import Optional, List, Dict, Any, Tuple
import pexpect
from pygdbmi.gdbcontroller import GdbController
from pygdbmi.constants import GdbTimeoutError
import logging

logger = logging.getLogger(__name__)


class QEMUManager:
    """QEMU 프로세스 관리자."""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.pid: Optional[int] = None
        self.port: Optional[int] = None
        self.arch: Optional[str] = None
        
    async def start(self, arch: str, kernel: Optional[str] = None, 
                   options: List[str] = None, gdb_stub: bool = True) -> Tuple[bool, Optional[str]]:
        """QEMU 프로세스를 시작합니다."""
        if options is None:
            options = []
            
        try:
            # QEMU 명령어 구성
            cmd = [f"qemu-system-{arch}"]
            
            if kernel:
                cmd.extend(["-kernel", kernel])
                
            if gdb_stub:
                cmd.extend(["-s", "-S"])  # GDB 스텁 활성화
                self.port = 1234
                
            cmd.extend(options)
            
            logger.info(f"QEMU 시작: {' '.join(cmd)}")
            
            # 비동기로 프로세스 시작
            loop = asyncio.get_event_loop()
            self.process = await loop.run_in_executor(
                None, lambda: subprocess.Popen(cmd, 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
            )
            
            self.pid = self.process.pid
            self.arch = arch
            
            # 프로세스가 정상적으로 시작되었는지 확인
            await asyncio.sleep(1)
            if self.process.poll() is not None:
                return False, "QEMU 프로세스가 즉시 종료되었습니다"
                
            logger.info(f"QEMU 시작 성공 (PID: {self.pid})")
            return True, None
            
        except Exception as e:
            logger.error(f"QEMU 시작 실패: {e}")
            return False, str(e)
    
    async def stop(self) -> Tuple[bool, Optional[str]]:
        """QEMU 프로세스를 중지합니다."""
        if not self.process:
            return True, None
            
        try:
            logger.info(f"QEMU 중지 (PID: {self.pid})")
            
            # 프로세스 종료
            self.process.terminate()
            
            # 5초 대기 후 강제 종료
            try:
                await asyncio.wait_for(
                    asyncio.get_event_loop().run_in_executor(None, self.process.wait),
                    timeout=5.0
                )
            except asyncio.TimeoutError:
                self.process.kill()
                await asyncio.get_event_loop().run_in_executor(None, self.process.wait)
                
            self.process = None
            self.pid = None
            self.port = None
            self.arch = None
            
            return True, None
            
        except Exception as e:
            logger.error(f"QEMU 중지 실패: {e}")
            return False, str(e)
    
    def is_running(self) -> bool:
        """QEMU가 실행 중인지 확인합니다."""
        if not self.process:
            return False
        return self.process.poll() is None


class GDBManager:
    """GDB 프로세스 관리자."""
    
    def __init__(self):
        self.controller: Optional[GdbController] = None
        self.pid: Optional[int] = None
        self.target: Optional[str] = None
        self.remote: Optional[str] = None
        self._output_buffer: List[str] = []
        
    async def start(self, target: Optional[str] = None, remote: Optional[str] = None,
                   options: List[str] = None) -> Tuple[bool, Optional[str]]:
        """GDB 프로세스를 시작합니다."""
        if options is None:
            options = []
            
        try:
            # GDB 명령어 구성
            gdb_cmd = ["gdb"]
            gdb_cmd.extend(options)
            
            if target:
                gdb_cmd.append(target)
                
            logger.info(f"GDB 시작: {' '.join(gdb_cmd)}")
            
            # GDB 컨트롤러 생성
            loop = asyncio.get_event_loop()
            self.controller = await loop.run_in_executor(
                None, lambda: GdbController(gdb_cmd)
            )
            
            # GDB 초기화 대기
            await asyncio.sleep(1)
            
            # 원격 연결 설정
            if remote:
                await self._connect_remote(remote)
                
            self.target = target
            self.remote = remote
            
            logger.info("GDB 시작 성공")
            return True, None
            
        except Exception as e:
            logger.error(f"GDB 시작 실패: {e}")
            return False, str(e)
    
    async def _connect_remote(self, remote: str) -> None:
        """원격 연결을 설정합니다."""
        try:
            await self.execute_command(f"target remote {remote}")
            logger.info(f"원격 연결 성공: {remote}")
        except Exception as e:
            logger.error(f"원격 연결 실패: {e}")
            raise
    
    async def execute_command(self, command: str, timeout: float = 30.0) -> Tuple[bool, str, Optional[str]]:
        """GDB 명령을 실행합니다."""
        if not self.controller:
            return False, "", "GDB가 시작되지 않았습니다"
            
        try:
            logger.info(f"GDB 명령 실행: {command}")
            
            # 명령 실행
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, self.controller.write, command, timeout
            )
            
            # 응답 처리
            output_lines = []
            for msg in response:
                if msg["type"] == "console":
                    output_lines.append(msg["payload"])
                elif msg["type"] == "log":
                    output_lines.append(f"[LOG] {msg['payload']}")
                elif msg["type"] == "error":
                    return False, "\n".join(output_lines), msg["payload"]
                    
            output = "\n".join(output_lines)
            self._output_buffer.append(f"$ {command}\n{output}")
            
            return True, output, None
            
        except GdbTimeoutError:
            error_msg = f"GDB 명령 타임아웃: {command}"
            logger.error(error_msg)
            return False, "", error_msg
        except Exception as e:
            error_msg = f"GDB 명령 실행 실패: {e}"
            logger.error(error_msg)
            return False, "", error_msg
    
    async def get_status(self) -> Dict[str, Any]:
        """GDB 상태를 가져옵니다."""
        if not self.controller:
            return {
                "running": False,
                "pid": None,
                "target": None,
                "breakpoints": [],
                "current_frame": None
            }
            
        try:
            # 브레이크포인트 정보 가져오기
            success, output, error = await self.execute_command("info breakpoints")
            breakpoints = []
            if success:
                # 브레이크포인트 파싱 (간단한 구현)
                lines = output.split('\n')
                for line in lines:
                    if 'breakpoint' in line.lower() and 'at' in line:
                        breakpoints.append({"info": line.strip()})
            
            # 현재 프레임 정보 가져오기
            success, output, error = await self.execute_command("info frame")
            current_frame = None
            if success:
                current_frame = {"info": output.strip()}
                
            return {
                "running": True,
                "pid": self.pid,
                "target": self.target,
                "breakpoints": breakpoints,
                "current_frame": current_frame
            }
            
        except Exception as e:
            logger.error(f"GDB 상태 조회 실패: {e}")
            return {
                "running": False,
                "pid": None,
                "target": None,
                "breakpoints": [],
                "current_frame": None
            }
    
    async def stop(self) -> Tuple[bool, Optional[str]]:
        """GDB 프로세스를 중지합니다."""
        if not self.controller:
            return True, None
            
        try:
            logger.info("GDB 중지")
            
            # GDB 종료
            await self.execute_command("quit")
            
            # 컨트롤러 정리
            self.controller.exit()
            self.controller = None
            self.pid = None
            self.target = None
            self.remote = None
            self._output_buffer.clear()
            
            return True, None
            
        except Exception as e:
            logger.error(f"GDB 중지 실패: {e}")
            return False, str(e)
    
    def is_running(self) -> bool:
        """GDB가 실행 중인지 확인합니다."""
        return self.controller is not None
    
    def get_output_buffer(self) -> List[str]:
        """출력 버퍼를 반환합니다."""
        return self._output_buffer.copy()

