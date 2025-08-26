"""GDB MCP 서버."""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
    Text,
    Image,
    Resource,
    ToolMessage,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel,
    Text,
    Image,
    Resource,
    ToolMessage,
)

from .models import (
    GDBExecuteRequest,
    GDBExecuteResponse,
    QEMUStartRequest,
    QEMUStartResponse,
    GDBStartRequest,
    GDBStartResponse,
    GDBStatusResponse,
    ProcessStopRequest,
    ProcessStopResponse,
)
from .process_manager import GDBManager, QEMUManager

logger = logging.getLogger(__name__)


class GDBMCPServer:
    """GDB MCP 서버."""
    
    def __init__(self):
        self.gdb_manager = GDBManager()
        self.qemu_manager = QEMUManager()
        self.server = Server("gdb-mcp")
        
        # 도구 등록
        self._register_tools()
        
    def _register_tools(self):
        """MCP 도구들을 등록합니다."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """사용 가능한 도구 목록을 반환합니다."""
            return ListToolsResult(
                tools=[
                    Tool(
                        name="gdb_start",
                        description="GDB 디버거를 시작합니다",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "target": {"type": "string", "description": "디버그할 파일 경로"},
                                "remote": {"type": "string", "description": "원격 연결 주소 (예: localhost:1234)"},
                                "options": {"type": "array", "items": {"type": "string"}, "description": "GDB 옵션들"}
                            }
                        }
                    ),
                    Tool(
                        name="gdb_execute",
                        description="GDB 명령을 실행합니다",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "command": {"type": "string", "description": "실행할 GDB 명령"},
                                "timeout": {"type": "number", "description": "명령 실행 타임아웃 (초)"}
                            },
                            "required": ["command"]
                        }
                    ),
                    Tool(
                        name="gdb_status",
                        description="GDB 상태를 조회합니다",
                        inputSchema={
                            "type": "object",
                            "properties": {}
                        }
                    ),
                    Tool(
                        name="qemu_start",
                        description="QEMU 에뮬레이터를 시작합니다",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "arch": {"type": "string", "description": "아키텍처 (예: x86_64, arm, aarch64)"},
                                "kernel": {"type": "string", "description": "커널 이미지 경로"},
                                "options": {"type": "array", "items": {"type": "string"}, "description": "QEMU 옵션들"},
                                "gdb_stub": {"type": "boolean", "description": "GDB 스텁 활성화 여부"}
                            },
                            "required": ["arch"]
                        }
                    ),
                    Tool(
                        name="process_stop",
                        description="프로세스를 중지합니다",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "process_type": {"type": "string", "description": "프로세스 타입 (gdb 또는 qemu)"}
                            },
                            "required": ["process_type"]
                        }
                    ),
                ]
            )
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """도구 호출을 처리합니다."""
            try:
                if name == "gdb_start":
                    return await self._handle_gdb_start(arguments)
                elif name == "gdb_execute":
                    return await self._handle_gdb_execute(arguments)
                elif name == "gdb_status":
                    return await self._handle_gdb_status(arguments)
                elif name == "qemu_start":
                    return await self._handle_qemu_start(arguments)
                elif name == "process_stop":
                    return await self._handle_process_stop(arguments)
                else:
                    return CallToolResult(
                        content=[TextContent(type="text", text=f"알 수 없는 도구: {name}")]
                    )
            except Exception as e:
                logger.error(f"도구 실행 중 오류: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"오류: {str(e)}")]
                )
    
    async def _handle_gdb_start(self, arguments: Dict[str, Any]) -> CallToolResult:
        """GDB 시작을 처리합니다."""
        try:
            request = GDBStartRequest(**arguments)
            success, error = await self.gdb_manager.start(
                target=request.target,
                remote=request.remote,
                options=request.options
            )
            
            response = GDBStartResponse(
                success=success,
                pid=self.gdb_manager.pid,
                error=error
            )
            
            content = f"GDB 시작: {'성공' if success else '실패'}"
            if response.pid:
                content += f" (PID: {response.pid})"
            if response.error:
                content += f"\n오류: {response.error}"
                
            return CallToolResult(
                content=[TextContent(type="text", text=content)]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"GDB 시작 오류: {str(e)}")]
            )
    
    async def _handle_gdb_execute(self, arguments: Dict[str, Any]) -> CallToolResult:
        """GDB 명령 실행을 처리합니다."""
        try:
            request = GDBExecuteRequest(**arguments)
            success, output, error = await self.gdb_manager.execute_command(
                request.command, request.timeout
            )
            
            content = f"명령: {request.command}\n"
            content += f"결과: {'성공' if success else '실패'}\n"
            if output:
                content += f"출력:\n{output}\n"
            if error:
                content += f"오류: {error}"
                
            return CallToolResult(
                content=[TextContent(type="text", text=content)]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"GDB 명령 실행 오류: {str(e)}")]
            )
    
    async def _handle_gdb_status(self, arguments: Dict[str, Any]) -> CallToolResult:
        """GDB 상태 조회를 처리합니다."""
        try:
            status = await self.gdb_manager.get_status()
            
            content = f"GDB 상태:\n"
            content += f"실행 중: {'예' if status['running'] else '아니오'}\n"
            if status['pid']:
                content += f"PID: {status['pid']}\n"
            if status['target']:
                content += f"타겟: {status['target']}\n"
            if status['breakpoints']:
                content += f"브레이크포인트 수: {len(status['breakpoints'])}\n"
            if status['current_frame']:
                content += f"현재 프레임: {status['current_frame']['info']}\n"
                
            return CallToolResult(
                content=[TextContent(type="text", text=content)]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"GDB 상태 조회 오류: {str(e)}")]
            )
    
    async def _handle_qemu_start(self, arguments: Dict[str, Any]) -> CallToolResult:
        """QEMU 시작을 처리합니다."""
        try:
            request = QEMUStartRequest(**arguments)
            success, error = await self.qemu_manager.start(
                arch=request.arch,
                kernel=request.kernel,
                options=request.options,
                gdb_stub=request.gdb_stub
            )
            
            response = QEMUStartResponse(
                success=success,
                pid=self.qemu_manager.pid,
                port=self.qemu_manager.port,
                error=error
            )
            
            content = f"QEMU 시작: {'성공' if success else '실패'}"
            if response.pid:
                content += f" (PID: {response.pid})"
            if response.port:
                content += f" (포트: {response.port})"
            if response.error:
                content += f"\n오류: {response.error}"
                
            return CallToolResult(
                content=[TextContent(type="text", text=content)]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"QEMU 시작 오류: {str(e)}")]
            )
    
    async def _handle_process_stop(self, arguments: Dict[str, Any]) -> CallToolResult:
        """프로세스 중지를 처리합니다."""
        try:
            request = ProcessStopRequest(**arguments)
            
            if request.process_type.lower() == "gdb":
                success, error = await self.gdb_manager.stop()
            elif request.process_type.lower() == "qemu":
                success, error = await self.qemu_manager.stop()
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"알 수 없는 프로세스 타입: {request.process_type}")]
                )
            
            response = ProcessStopResponse(success=success, error=error)
            
            content = f"{request.process_type.upper()} 중지: {'성공' if success else '실패'}"
            if response.error:
                content += f"\n오류: {response.error}"
                
            return CallToolResult(
                content=[TextContent(type="text", text=content)]
            )
            
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"프로세스 중지 오류: {str(e)}")]
            )
    
    async def run(self):
        """서버를 실행합니다."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="gdb-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities={},
                    ),
                ),
            )

