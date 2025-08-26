#include <stdio.h>
#include <stdint.h>
#include <string.h>

// UART 관련 레지스터 정의 (STM32F7xx 기준)
#define UART_BASE           0x40011000
#define UART_SR             (*(volatile uint32_t*)(UART_BASE + 0x00))
#define UART_DR             (*(volatile uint32_t*)(UART_BASE + 0x04))
#define UART_BRR            (*(volatile uint32_t*)(UART_BASE + 0x08))
#define UART_CR1            (*(volatile uint32_t*)(UART_BASE + 0x0C))
#define UART_CR2            (*(volatile uint32_t*)(UART_BASE + 0x10))
#define UART_CR3            (*(volatile uint32_t*)(UART_BASE + 0x14))

// UART 상태 비트
#define UART_SR_TXE         (1 << 7)  // Transmit data register empty
#define UART_SR_TC          (1 << 6)  // Transmission complete
#define UART_SR_RXNE        (1 << 5)  // Read data register not empty

// UART 제어 비트
#define UART_CR1_UARTEN     (1 << 13) // UART enable
#define UART_CR1_TE         (1 << 3)  // Transmitter enable
#define UART_CR1_RE         (1 << 2)  // Receiver enable

// GPIO 관련 레지스터 (UART1 TX/RX 핀용)
#define GPIOA_BASE          0x40020000
#define GPIOA_MODER         (*(volatile uint32_t*)(GPIOA_BASE + 0x00))
#define GPIOA_OTYPER        (*(volatile uint32_t*)(GPIOA_BASE + 0x04))
#define GPIOA_OSPEEDR       (*(volatile uint32_t*)(GPIOA_BASE + 0x08))
#define GPIOA_PUPDR         (*(volatile uint32_t*)(GPIOA_BASE + 0x0C))
#define GPIOA_IDR           (*(volatile uint32_t*)(GPIOA_BASE + 0x10))
#define GPIOA_ODR           (*(volatile uint32_t*)(GPIOA_BASE + 0x14))
#define GPIOA_BSRR          (*(volatile uint32_t*)(GPIOA_BASE + 0x18))
#define GPIOA_LCKR          (*(volatile uint32_t*)(GPIOA_BASE + 0x1C))
#define GPIOA_AFRL          (*(volatile uint32_t*)(GPIOA_BASE + 0x20))
#define GPIOA_AFRH          (*(volatile uint32_t*)(GPIOA_BASE + 0x24))

// RCC (Reset and Clock Control) 레지스터
#define RCC_BASE            0x40023800
#define RCC_APB2ENR         (*(volatile uint32_t*)(RCC_BASE + 0x44))
#define RCC_AHB1ENR         (*(volatile uint32_t*)(RCC_BASE + 0x30))

// 클럭 활성화 비트
#define RCC_APB2ENR_USART1EN (1 << 4)  // USART1 clock enable
#define RCC_AHB1ENR_GPIOAEN  (1 << 0)  // GPIOA clock enable

// 시스템 클럭 설정
#define SYSTEM_CLOCK        216000000  // 216 MHz
#define UART_BAUDRATE       115200

// 딜레이 함수
void delay_ms(uint32_t ms) {
    volatile uint32_t i, j;
    for (i = 0; i < ms; i++) {
        for (j = 0; j < 216000; j++) {  // 216MHz에서 대략 1ms
            __asm("nop");
        }
    }
}

// UART 초기화
void uart_init(void) {
    // 1. GPIOA 클럭 활성화
    RCC_AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    
    // 2. USART1 클럭 활성화
    RCC_APB2ENR |= RCC_APB2ENR_USART1EN;
    
    // 3. GPIOA9 (TX)와 GPIOA10 (RX) 설정
    // PA9: AF7 (USART1_TX), PA10: AF7 (USART1_RX)
    GPIOA_MODER &= ~((3 << 18) | (3 << 20));  // Clear PA9, PA10
    GPIOA_MODER |= (2 << 18) | (2 << 20);     // Set as alternate function
    
    GPIOA_OSPEEDR |= (3 << 18) | (3 << 20);   // High speed
    
    GPIOA_PUPDR &= ~((3 << 18) | (3 << 20));  // No pull-up/pull-down
    
    // 4. Alternate function 설정 (AF7 for USART1)
    GPIOA_AFRH &= ~((0xF << 4) | (0xF << 8)); // Clear AF9, AF10
    GPIOA_AFRH |= (7 << 4) | (7 << 8);        // Set AF7 for PA9, PA10
    
    // 5. UART 설정
    UART_CR1 = 0;  // Disable UART first
    
    // Baud rate 설정
    uint32_t brr = SYSTEM_CLOCK / UART_BAUDRATE;
    UART_BRR = brr;
    
    // UART 활성화
    UART_CR1 = UART_CR1_UARTEN | UART_CR1_TE | UART_CR1_RE;
}

// UART 문자 전송
void uart_putchar(char c) {
    while (!(UART_SR & UART_SR_TXE));  // TXE 비트 대기
    UART_DR = c;
    while (!(UART_SR & UART_SR_TC));   // TC 비트 대기
}

// UART 문자열 전송
void uart_puts(const char* str) {
    while (*str) {
        uart_putchar(*str++);
    }
}

// UART 문자 수신
char uart_getchar(void) {
    while (!(UART_SR & UART_SR_RXNE));  // RXNE 비트 대기
    return (char)UART_DR;
}

// 메인 함수
int main(void) {
    // UART 초기화
    uart_init();
    
    // 시작 메시지
    uart_puts("\r\n");
    uart_puts("========================================\r\n");
    uart_puts("Cortex-M7 Hello World Example\r\n");
    uart_puts("STM32F7xx Series\r\n");
    uart_puts("UART Baud Rate: 115200\r\n");
    uart_puts("========================================\r\n");
    uart_puts("\r\n");
    
    uint32_t counter = 0;
    
    while (1) {
        uart_puts("Hello World from Cortex-M7! Counter: ");
        
        // 간단한 숫자 출력
        char num_str[16];
        int i = 0;
        uint32_t num = counter;
        
        if (num == 0) {
            uart_putchar('0');
        } else {
            // 숫자를 문자열로 변환
            while (num > 0) {
                num_str[i++] = '0' + (num % 10);
                num /= 10;
            }
            // 역순으로 출력
            while (i > 0) {
                uart_putchar(num_str[--i]);
            }
        }
        
        uart_puts("\r\n");
        uart_puts("Type any character to continue...\r\n");
        
        // 사용자 입력 대기
        char input = uart_getchar();
        uart_puts("You typed: ");
        uart_putchar(input);
        uart_puts("\r\n\r\n");
        
        counter++;
        delay_ms(1000);
    }
    
    return 0;
}
