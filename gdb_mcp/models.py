"""Pydantic models for GDB MCP server."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GDBExecuteRequest(BaseModel):
    """GDB 명령 실행 요청."""
    command: str = Field(..., description="실행할 GDB 명령")
    timeout: Optional[float] = Field(30.0, description="명령 실행 타임아웃 (초)")


class GDBExecuteResponse(BaseModel):
    """GDB 명령 실행 응답."""
    success: bool = Field(..., description="명령 실행 성공 여부")
    output: str = Field(..., description="GDB 출력")
    error: Optional[str] = Field(None, description="에러 메시지")


class QEMUStartRequest(BaseModel):
    """QEMU 시작 요청."""
    arch: str = Field(..., description="아키텍처 (예: x86_64, arm, aarch64)")
    kernel: Optional[str] = Field(None, description="커널 이미지 경로")
    options: List[str] = Field(default_factory=list, description="QEMU 옵션들")
    gdb_stub: bool = Field(True, description="GDB 스텁 활성화 여부")


class QEMUStartResponse(BaseModel):
    """QEMU 시작 응답."""
    success: bool = Field(..., description="QEMU 시작 성공 여부")
    pid: Optional[int] = Field(None, description="QEMU 프로세스 ID")
    port: Optional[int] = Field(None, description="GDB 스텁 포트")
    error: Optional[str] = Field(None, description="에러 메시지")


class GDBStartRequest(BaseModel):
    """GDB 시작 요청."""
    target: Optional[str] = Field(None, description="디버그할 파일 경로")
    remote: Optional[str] = Field(None, description="원격 연결 주소 (예: localhost:1234)")
    options: List[str] = Field(default_factory=list, description="GDB 옵션들")


class GDBStartResponse(BaseModel):
    """GDB 시작 응답."""
    success: bool = Field(..., description="GDB 시작 성공 여부")
    pid: Optional[int] = Field(None, description="GDB 프로세스 ID")
    error: Optional[str] = Field(None, description="에러 메시지")


class GDBStatusResponse(BaseModel):
    """GDB 상태 응답."""
    running: bool = Field(..., description="GDB 실행 중 여부")
    pid: Optional[int] = Field(None, description="GDB 프로세스 ID")
    target: Optional[str] = Field(None, description="현재 타겟")
    breakpoints: List[Dict[str, Any]] = Field(default_factory=list, description="브레이크포인트 목록")
    current_frame: Optional[Dict[str, Any]] = Field(None, description="현재 프레임 정보")


class ProcessStopRequest(BaseModel):
    """프로세스 중지 요청."""
    process_type: str = Field(..., description="프로세스 타입 (gdb 또는 qemu)")


class ProcessStopResponse(BaseModel):
    """프로세스 중지 응답."""
    success: bool = Field(..., description="중지 성공 여부")
    error: Optional[str] = Field(None, description="에러 메시지")

