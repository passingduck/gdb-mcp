/* STM32F7xx 링커 스크립트 */
MEMORY
{
    FLASH (rx)      : ORIGIN = 0x08000000, LENGTH = 1024K
    RAM (xrw)       : ORIGIN = 0x20000000, LENGTH = 320K
    CCMRAM (rw)     : ORIGIN = 0x10000000, LENGTH = 64K
}

/* 스택 크기 설정 */
_stack_size = 0x4000;

/* 섹션 정의 */
SECTIONS
{
    /* 벡터 테이블과 코드 */
    .text :
    {
        KEEP(*(.isr_vector))
        *(.text*)
        *(.rodata*)
        . = ALIGN(4);
    } >FLASH

    /* 초기화된 데이터 */
    .data : 
    {
        _sdata = .;
        *(.data*)
        . = ALIGN(4);
        _edata = .;
    } >RAM AT> FLASH

    /* 초기화되지 않은 데이터 */
    .bss :
    {
        _sbss = .;
        *(.bss*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = .;
    } >RAM

    /* 스택 */
    .stack :
    {
        . = ALIGN(8);
        . = . + _stack_size;
        . = ALIGN(8);
        _estack = .;
    } >RAM

    /* CCM RAM */
    .ccmram :
    {
        *(.ccmram*)
    } >CCMRAM

    /* 디버그 정보 제거 */
    /DISCARD/ :
    {
        libc.a ( * )
        libm.a ( * )
        libgcc.a ( * )
    }
}
