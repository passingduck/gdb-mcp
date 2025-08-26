#!/bin/bash

# Cortex-M7 GDB 디버깅 스크립트

echo "=== Cortex-M7 Hello World GDB 디버깅 ==="

# 빌드 확인
if [ ! -f "cortex_m7_hello_world.elf" ]; then
    echo "ELF 파일이 없습니다. 먼저 빌드하세요:"
    echo "make all"
    exit 1
fi

# GDB 명령어 구성
GDB_CMD="arm-none-eabi-gdb"
GDB_OPTS="--tui"  # 텍스트 UI 활성화
GDB_SCRIPT="gdb_commands.gdb"

# GDB 명령어 스크립트 생성
cat > $GDB_SCRIPT << 'EOF'
# GDB 초기화 명령어들
set architecture arm
set endian little
set target-charset ASCII

# 타겟 연결 (QEMU GDB 스텁)
target remote localhost:1234

# 프로그램 로드
load

# 브레이크포인트 설정
break main
break uart_init
break uart_putchar

# 레지스터 표시
layout regs

# 소스 코드 표시
layout src

# 실행
continue
EOF

echo "GDB 명령어: $GDB_CMD $GDB_OPTS -x $GDB_SCRIPT cortex_m7_hello_world.elf"
echo ""
echo "GDB 디버깅을 시작합니다..."
echo "QEMU가 실행 중이어야 합니다 (qemu_run.sh 실행 후)."
echo ""

# GDB 실행
$GDB_CMD $GDB_OPTS -x $GDB_SCRIPT cortex_m7_hello_world.elf

# 임시 파일 정리
rm -f $GDB_SCRIPT

echo ""
echo "GDB 디버깅이 종료되었습니다."
