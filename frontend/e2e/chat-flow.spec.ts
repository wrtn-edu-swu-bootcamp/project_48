import { test, expect } from '@playwright/test';

test.describe('Chat Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/chat');
  });

  test('should display chat page correctly', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/AI 신입생 도우미/);
    
    // Check header
    await expect(page.getByRole('banner')).toBeVisible();
    
    // Check input area
    await expect(page.getByRole('textbox')).toBeVisible();
    await expect(page.getByRole('button', { name: /전송/i })).toBeVisible();
  });

  test('should display welcome message', async ({ page }) => {
    // Check for welcome message
    await expect(page.getByText(/안녕하세요/)).toBeVisible();
  });

  test('should display example questions', async ({ page }) => {
    // Check for example question buttons
    await expect(page.getByText(/수강신청은 언제 하나요/)).toBeVisible();
  });

  test('should send a message and receive response', async ({ page }) => {
    // Type a question
    const input = page.getByRole('textbox');
    await input.fill('수강신청은 언제 하나요?');
    
    // Click send button
    await page.getByRole('button', { name: /전송/i }).click();
    
    // Wait for user message to appear
    await expect(page.getByText('수강신청은 언제 하나요?')).toBeVisible();
    
    // Wait for bot response (with timeout)
    await expect(page.getByTestId('typing-indicator')).toBeVisible();
    
    // Check that response appears (may take a few seconds due to API)
    await expect(page.getByText(/학기/i).first()).toBeVisible({ timeout: 10000 });
  });

  test('should send message with Enter key', async ({ page }) => {
    // Type a question
    const input = page.getByRole('textbox');
    await input.fill('장학금 신청 방법이 궁금해요');
    
    // Press Enter
    await input.press('Enter');
    
    // Wait for user message to appear
    await expect(page.getByText('장학금 신청 방법이 궁금해요')).toBeVisible();
  });

  test('should not send empty message', async ({ page }) => {
    // Try to send without typing
    const sendButton = page.getByRole('button', { name: /전송/i });
    await sendButton.click();
    
    // No message should appear (only welcome message)
    const messages = page.locator('[data-role="user-message"]');
    await expect(messages).toHaveCount(0);
  });

  test('should disable input while loading', async ({ page }) => {
    // Send a message
    const input = page.getByRole('textbox');
    await input.fill('테스트 질문');
    await page.getByRole('button', { name: /전송/i }).click();
    
    // Input should be disabled during loading
    await expect(input).toBeDisabled();
    await expect(page.getByRole('button', { name: /전송/i })).toBeDisabled();
  });

  test('should click example question', async ({ page }) => {
    // Click on example question
    await page.getByText(/수강신청은 언제 하나요/).click();
    
    // Message should be sent
    await expect(page.getByText('수강신청은 언제 하나요?')).toBeVisible();
  });

  test('should display sources in bot message', async ({ page }) => {
    // Send a question that returns sources
    const input = page.getByRole('textbox');
    await input.fill('수강신청 일정 알려주세요');
    await page.getByRole('button', { name: /전송/i }).click();
    
    // Wait for response
    await expect(page.getByTestId('typing-indicator')).toBeVisible();
    await page.waitForTimeout(3000); // Wait for API response
    
    // Check for source citation
    await expect(page.getByText(/출처/i)).toBeVisible({ timeout: 10000 });
  });

  test('should handle multiple messages in sequence', async ({ page }) => {
    const input = page.getByRole('textbox');
    
    // Send first message
    await input.fill('첫 번째 질문');
    await input.press('Enter');
    await page.waitForTimeout(2000);
    
    // Send second message
    await input.fill('두 번째 질문');
    await input.press('Enter');
    
    // Both messages should be visible
    await expect(page.getByText('첫 번째 질문')).toBeVisible();
    await expect(page.getByText('두 번째 질문')).toBeVisible();
  });

  test('should scroll to bottom when new message arrives', async ({ page }) => {
    // Send multiple messages to create scroll
    const input = page.getByRole('textbox');
    
    for (let i = 0; i < 5; i++) {
      await input.fill(`질문 ${i + 1}`);
      await input.press('Enter');
      await page.waitForTimeout(500);
    }
    
    // Last message should be in viewport
    await expect(page.getByText('질문 5')).toBeInViewport();
  });
});
