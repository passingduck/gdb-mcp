# Cortex-M7 Hello World Makefile

# OS 감지
ifeq ($(OS),Windows_NT)
    # Windows 환경
    RM = del /Q
    RMDIR = rmdir /S /Q
    MKDIR = mkdir
    SEP = \\
    EXE = .exe
    SHELL = cmd
else
    # Linux/Unix 환경
    RM = rm -f
    RMDIR = rm -rf
    MKDIR = mkdir -p
    SEP = /
    EXE =
    SHELL = /bin/bash
endif

# 도구체인 설정
CC = arm-none-eabi-gcc
AS = arm-none-eabi-as
LD = arm-none-eabi-ld
OBJCOPY = arm-none-eabi-objcopy
OBJDUMP = arm-none-eabi-objdump
SIZE = arm-none-eabi-size

# 타겟 설정
TARGET = cortex_m7_hello_world
MCU = cortex-m7
FPU = fpv5-d16

# 컴파일러 플래그
CFLAGS = -mcpu=$(MCU) -mfpu=$(FPU) -mfloat-abi=hard
CFLAGS += -mthumb -mthumb-interwork
CFLAGS += -ffunction-sections -fdata-sections
CFLAGS += -fno-builtin -fno-stack-protector
CFLAGS += -Wall -Wextra -Werror
CFLAGS += -std=c99
CFLAGS += -O2

# 어셈블러 플래그
ASFLAGS = -mcpu=$(MCU) -mfpu=$(FPU) -mfloat-abi=hard
ASFLAGS += -mthumb -mthumb-interwork

# 링커 플래그
LDFLAGS = -mcpu=$(MCU) -mfpu=$(FPU) -mfloat-abi=hard
LDFLAGS += -mthumb -mthumb-interwork
LDFLAGS += -T$(TARGET).ld
LDFLAGS += -Wl,--gc-sections
LDFLAGS += -Wl,--print-memory-usage
LDFLAGS += -nostartfiles

# 소스 파일들
C_SOURCES = main.c startup.c
ASM_SOURCES = 

# 오브젝트 파일들
OBJECTS = $(C_SOURCES:.c=.o) $(ASM_SOURCES:.s=.o)

# 기본 타겟
all: $(TARGET).elf $(TARGET).bin $(TARGET).hex

# ELF 파일 생성
$(TARGET).elf: $(OBJECTS)
	$(CC) $(LDFLAGS) -o $@ $^
	$(SIZE) $@

# BIN 파일 생성
$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

# HEX 파일 생성
$(TARGET).hex: $(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

# 오브젝트 파일 컴파일
%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

%.o: %.s
	$(AS) $(ASFLAGS) -o $@ $<

# 디스어셈블리 생성
disasm: $(TARGET).elf
	$(OBJDUMP) -d $< > $(TARGET).dis

# 정리
clean:
ifeq ($(OS),Windows_NT)
	$(RM) *.o *.elf *.bin *.hex *.dis
else
	$(RM) *.o *.elf *.bin *.hex *.dis
endif

# 플래시 (OpenOCD 사용)
flash: $(TARGET).bin
	openocd -f interface/stlink.cfg -f target/stm32f7x.cfg -c "program $< verify reset exit"

# 디버그 (OpenOCD + GDB)
debug: $(TARGET).elf
ifeq ($(OS),Windows_NT)
	start /B openocd -f interface/stlink.cfg -f target/stm32f7x.cfg -c "program $< verify reset"
	timeout /t 1 /nobreak >nul
	arm-none-eabi-gdb -ex "target remote localhost:3333" -ex "load" -ex "monitor reset halt" $<
else
	openocd -f interface/stlink.cfg -f target/stm32f7x.cfg -c "program $< verify reset" &
	sleep 1
	arm-none-eabi-gdb -ex "target remote localhost:3333" -ex "load" -ex "monitor reset halt" $<
endif

# 시리얼 모니터 (115200 baud)
monitor:
ifeq ($(OS),Windows_NT)
	@echo 시리얼 포트를 확인하고 연결하세요...
	@echo Windows: COM3, COM4, COM5 등
	@echo 터미널 프로그램에서 115200 baud로 연결
	@echo 예: PuTTY, Tera Term, HyperTerminal
else
	@echo 시리얼 포트를 확인하고 연결하세요...
	@echo Linux: /dev/ttyUSB0, /dev/ttyACM0
	@echo 터미널 프로그램에서 115200 baud로 연결
	@echo 예: screen /dev/ttyUSB0 115200
endif

# QEMU 실행 (OS별 스크립트 사용)
qemu:
ifeq ($(OS),Windows_NT)
	@echo Windows 환경에서 QEMU 실행...
	qemu_run.bat
else
	@echo Linux 환경에서 QEMU 실행...
	./qemu_run.sh
endif

# GDB 디버깅 (OS별 스크립트 사용)
gdb-debug:
ifeq ($(OS),Windows_NT)
	@echo Windows 환경에서 GDB 디버깅...
	gdb_debug.bat
else
	@echo Linux 환경에서 GDB 디버깅...
	./gdb_debug.sh
endif

# 도움말
help:
	@echo "사용 가능한 타겟:"
	@echo "  all       - 모든 파일 빌드"
	@echo "  clean     - 빌드 파일 정리"
	@echo "  flash     - 보드에 플래시"
	@echo "  debug     - GDB 디버깅 시작"
	@echo "  monitor   - 시리얼 모니터 정보"
	@echo "  disasm    - 디스어셈블리 생성"
	@echo "  qemu      - QEMU 시뮬레이션 실행"
	@echo "  gdb-debug - GDB 디버깅 실행"
ifeq ($(OS),Windows_NT)
	@echo ""
	@echo "Windows 전용:"
	@echo "  qemu_run.bat    - QEMU 실행 (배치 파일)"
	@echo "  gdb_debug.bat   - GDB 디버깅 (배치 파일)"
else
	@echo ""
	@echo "Linux 전용:"
	@echo "  ./qemu_run.sh   - QEMU 실행 (쉘 스크립트)"
	@echo "  ./gdb_debug.sh  - GDB 디버깅 (쉘 스크립트)"
endif

.PHONY: all clean flash debug monitor help disasm qemu gdb-debug
