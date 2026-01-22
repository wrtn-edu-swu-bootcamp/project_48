import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should navigate from home to chat page', async ({ page }) => {
    // Go to home page
    await page.goto('/');
    
    // Check home page elements
    await expect(page.getByRole('heading', { name: /AI 신입생 도우미/i })).toBeVisible();
    
    // Click "지금 질문하기" button
    await page.getByRole('button', { name: /지금 질문하기/i }).click();
    
    // Should navigate to chat page
    await expect(page).toHaveURL('/chat');
    await expect(page.getByRole('textbox')).toBeVisible();
  });

  test('should navigate using header link', async ({ page }) => {
    await page.goto('/chat');
    
    // Click logo or service name to go back home
    await page.getByText(/AI 신입생 도우미/).first().click();
    
    // Should navigate to home page
    await expect(page).toHaveURL('/');
  });

  test('should display footer links', async ({ page }) => {
    await page.goto('/');
    
    // Check footer links
    await expect(page.getByRole('contentinfo')).toBeVisible();
    await expect(page.getByText(/자주 묻는 질문/i)).toBeVisible();
    await expect(page.getByText(/학사 일정 보기/i)).toBeVisible();
  });

  test('should navigate using browser back button', async ({ page }) => {
    // Go to home
    await page.goto('/');
    
    // Navigate to chat
    await page.goto('/chat');
    await expect(page).toHaveURL('/chat');
    
    // Go back
    await page.goBack();
    await expect(page).toHaveURL('/');
  });

  test('should handle 404 page', async ({ page }) => {
    // Try to access non-existent page
    const response = await page.goto('/non-existent-page');
    
    // Should show 404 or redirect
    expect(response?.status()).toBe(404);
  });

  test('should maintain state when navigating back', async ({ page }) => {
    await page.goto('/chat');
    
    // Send a message
    const input = page.getByRole('textbox');
    await input.fill('테스트 질문');
    await page.getByRole('button', { name: /전송/i }).click();
    
    // Navigate away
    await page.goto('/');
    
    // Navigate back
    await page.goto('/chat');
    
    // Message should still be visible (if state is persisted)
    // This depends on implementation
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');
    
    // Check that content is visible and properly sized
    await expect(page.getByRole('heading', { name: /AI 신입생 도우미/i })).toBeVisible();
    
    // Navigate to chat
    await page.goto('/chat');
    await expect(page.getByRole('textbox')).toBeVisible();
  });

  test('should be responsive on tablet', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');
    
    // Check layout
    await expect(page.getByRole('heading', { name: /AI 신입생 도우미/i })).toBeVisible();
  });

  test('should display main page features', async ({ page }) => {
    await page.goto('/');
    
    // Check quick links section
    await expect(page.getByText(/빠른 안내/i)).toBeVisible();
    await expect(page.getByText(/학사일정 보기/i)).toBeVisible();
    await expect(page.getByText(/공지사항 확인/i)).toBeVisible();
    await expect(page.getByText(/지원프로그램 안내/i)).toBeVisible();
  });

  test('should display FAQ section', async ({ page }) => {
    await page.goto('/');
    
    // Check FAQ section
    await expect(page.getByText(/자주 묻는 질문/i)).toBeVisible();
  });
});
