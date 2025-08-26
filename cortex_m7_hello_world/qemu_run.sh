#!/bin/bash

# Cortex-M7 QEMU 시뮬레이션 스크립트

echo "=== Cortex-M7 Hello World QEMU 시뮬레이션 ==="

# 빌드 확인
if [ ! -f "cortex_m7_hello_world.elf" ]; then
    echo "ELF 파일이 없습니다. 먼저 빌드하세요:"
    echo "make all"
    exit 1
fi

# QEMU 명령어 구성
QEMU_CMD="qemu-system-arm"
QEMU_OPTS="-M mps2-an385"  # ARM MPS2-AN385 보드 (Cortex-M3 기반이지만 M7과 호환)
QEMU_OPTS="$QEMU_OPTS -cpu cortex-m3"  # Cortex-M3 CPU (M7과 유사한 명령어셋)
QEMU_OPTS="$QEMU_OPTS -kernel cortex_m7_hello_world.elf"
QEMU_OPTS="$QEMU_OPTS -nographic"  # 그래픽 없이 콘솔만
QEMU_OPTS="$QEMU_OPTS -serial mon:stdio"  # 시리얼 출력을 표준 입출력으로
QEMU_OPTS="$QEMU_OPTS -semihosting"  # 세미호스팅 활성화
QEMU_OPTS="$QEMU_OPTS -s -S"  # GDB 스텁 활성화 (포트 1234)

echo "QEMU 명령어: $QEMU_CMD $QEMU_OPTS"
echo ""
echo "시뮬레이션을 시작합니다..."
echo "종료하려면 Ctrl+C를 누르세요."
echo ""

# QEMU 실행
$QEMU_CMD $QEMU_OPTS

echo ""
echo "QEMU 시뮬레이션이 종료되었습니다."
