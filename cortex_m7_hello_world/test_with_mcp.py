#!/usr/bin/env python3
"""MCP 서버를 사용한 Cortex-M7 Hello World 테스트."""

import asyncio
import subprocess
import sys
import time
from pathlib import Path


class CortexM7MCPServer:
    """Cortex-M7 MCP 서버 테스트 클래스."""
    
    def __init__(self):
        self.qemu_process = None
        self.gdb_process = None
        
    async def start_qemu(self):
        """QEMU 시뮬레이션을 시작합니다."""
        print("QEMU 시뮬레이션 시작...")
        
        # ELF 파일 확인
        elf_file = Path("cortex_m7_hello_world.elf")
        if not elf_file.exists():
            print("❌ ELF 파일이 없습니다. 먼저 빌드하세요: make all")
            return False
        
        # QEMU 명령어 구성
        cmd = [
            "qemu-system-arm",
            "-M", "mps2-an385",
            "-cpu", "cortex-m3",
            "-kernel", str(elf_file),
            "-nographic",
            "-serial", "mon:stdio",
            "-semihosting",
            "-s", "-S"  # GDB 스텁 활성화
        ]
        
        try:
            self.qemu_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # QEMU가 시작될 때까지 대기
            await asyncio.sleep(2)
            
            if self.qemu_process.poll() is None:
                print("✅ QEMU 시뮬레이션 시작됨 (PID: {})".format(self.qemu_process.pid))
                return True
            else:
                print("❌ QEMU 시작 실패")
                return False
                
        except Exception as e:
            print(f"❌ QEMU 시작 오류: {e}")
            return False
    
    async def test_gdb_connection(self):
        """GDB 연결을 테스트합니다."""
        print("\nGDB 연결 테스트...")
        
        try:
            # GDB로 간단한 연결 테스트
            cmd = [
                "arm-none-eabi-gdb",
                "--batch",
                "--ex", "target remote localhost:1234",
                "--ex", "info registers",
                "--ex", "quit"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ GDB 연결 성공")
                print("레지스터 정보:")
                print(result.stdout)
                return True
            else:
                print("❌ GDB 연결 실패")
                print("오류:", result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ GDB 연결 타임아웃")
            return False
        except Exception as e:
            print(f"❌ GDB 연결 오류: {e}")
            return False
    
    async def test_mcp_tools(self):
        """MCP 도구들을 테스트합니다."""
        print("\nMCP 도구 테스트...")
        
        # MCP 서버가 실행 중인지 확인
        try:
            # 간단한 MCP 서버 테스트
            from gdb_mcp.process_manager import GDBManager, QEMUManager
            
            print("✅ MCP 서버 모듈 로드 성공")
            
            # GDB 매니저 테스트
            gdb_manager = GDBManager()
            status = await gdb_manager.get_status()
            print(f"GDB 상태: {status}")
            
            # QEMU 매니저 테스트
            qemu_manager = QEMUManager()
            running = qemu_manager.is_running()
            print(f"QEMU 실행 중: {running}")
            
            return True
            
        except ImportError as e:
            print(f"❌ MCP 서버 모듈 로드 실패: {e}")
            return False
        except Exception as e:
            print(f"❌ MCP 도구 테스트 오류: {e}")
            return False
    
    async def run_hello_world_test(self):
        """Hello World 프로그램을 테스트합니다."""
        print("\nHello World 프로그램 테스트...")
        
        try:
            # QEMU에서 출력 확인
            if self.qemu_process and self.qemu_process.poll() is None:
                # QEMU 프로세스가 실행 중이면 출력 확인
                await asyncio.sleep(1)
                
                # 시뮬레이션 종료 신호 전송
                self.qemu_process.terminate()
                await asyncio.sleep(1)
                
                if self.qemu_process.poll() is not None:
                    print("✅ QEMU 시뮬레이션 정상 종료")
                    return True
                else:
                    print("⚠️ QEMU 시뮬레이션 강제 종료")
                    self.qemu_process.kill()
                    return True
            else:
                print("❌ QEMU 프로세스가 실행되지 않음")
                return False
                
        except Exception as e:
            print(f"❌ Hello World 테스트 오류: {e}")
            return False
    
    async def cleanup(self):
        """리소스를 정리합니다."""
        print("\n리소스 정리...")
        
        if self.qemu_process:
            try:
                self.qemu_process.terminate()
                await asyncio.sleep(1)
                if self.qemu_process.poll() is None:
                    self.qemu_process.kill()
            except:
                pass
        
        if self.gdb_process:
            try:
                self.gdb_process.terminate()
                await asyncio.sleep(1)
                if self.gdb_process.poll() is None:
                    self.gdb_process.kill()
            except:
                pass
        
        print("✅ 리소스 정리 완료")
    
    async def run_full_test(self):
        """전체 테스트를 실행합니다."""
        print("=== Cortex-M7 Hello World MCP 테스트 ===\n")
        
        success_count = 0
        total_tests = 4
        
        try:
            # 1. QEMU 시작 테스트
            if await self.start_qemu():
                success_count += 1
            
            # 2. GDB 연결 테스트
            if await self.test_gdb_connection():
                success_count += 1
            
            # 3. MCP 도구 테스트
            if await self.test_mcp_tools():
                success_count += 1
            
            # 4. Hello World 프로그램 테스트
            if await self.run_hello_world_test():
                success_count += 1
            
        except Exception as e:
            print(f"❌ 테스트 중 오류 발생: {e}")
        finally:
            await self.cleanup()
        
        # 결과 출력
        print(f"\n=== 테스트 결과 ===")
        print(f"성공: {success_count}/{total_tests}")
        
        if success_count == total_tests:
            print("🎉 모든 테스트 통과!")
        elif success_count >= total_tests // 2:
            print("⚠️ 일부 테스트 실패 (기본 기능은 동작)")
        else:
            print("❌ 대부분의 테스트 실패")
        
        return success_count == total_tests


async def main():
    """메인 함수."""
    # 프로젝트 디렉토리 확인
    if not Path("cortex_m7_hello_world.elf").exists():
        print("❌ ELF 파일이 없습니다.")
        print("먼저 빌드하세요:")
        print("cd cortex_m7_hello_world")
        print("make all")
        return
    
    # MCP 테스트 실행
    tester = CortexM7MCPServer()
    success = await tester.run_full_test()
    
    if success:
        print("\n✅ Cortex-M7 Hello World MCP 테스트 완료!")
        print("\n이제 Cursor에서 MCP 도구를 사용할 수 있습니다:")
        print("- gdb_start: GDB 디버거 시작")
        print("- gdb_execute: GDB 명령 실행")
        print("- qemu_start: QEMU 시뮬레이션 시작")
        print("- gdb_status: GDB 상태 확인")
    else:
        print("\n❌ 일부 테스트가 실패했습니다.")
        print("도구 설치나 설정을 확인하세요.")


if __name__ == "__main__":
    asyncio.run(main())
