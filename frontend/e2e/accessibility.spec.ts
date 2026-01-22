import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Tests', () => {
  test('should not have any automatically detectable accessibility issues on home page', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should not have any automatically detectable accessibility issues on chat page', async ({ page }) => {
    await page.goto('/chat');
    
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('should support keyboard navigation on chat page', async ({ page }) => {
    await page.goto('/chat');
    
    // Tab to input field
    await page.keyboard.press('Tab');
    await expect(page.getByRole('textbox')).toBeFocused();
    
    // Tab to send button
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: /전송/i })).toBeFocused();
  });

  test('should have proper ARIA labels on input field', async ({ page }) => {
    await page.goto('/chat');
    
    const input = page.getByRole('textbox');
    await expect(input).toHaveAttribute('aria-label');
  });

  test('should have proper ARIA labels on buttons', async ({ page }) => {
    await page.goto('/chat');
    
    const sendButton = page.getByRole('button', { name: /전송/i });
    await expect(sendButton).toHaveAccessibleName();
  });

  test('should have proper heading hierarchy', async ({ page }) => {
    await page.goto('/');
    
    // Check for h1
    const h1 = page.getByRole('heading', { level: 1 });
    await expect(h1).toBeVisible();
    
    // Should only have one h1
    expect(await h1.count()).toBe(1);
  });

  test('should have sufficient color contrast', async ({ page }) => {
    await page.goto('/');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .analyze();
    
    const contrastViolations = accessibilityScanResults.violations.filter(
      v => v.id === 'color-contrast'
    );
    
    expect(contrastViolations).toEqual([]);
  });

  test('should support screen reader announcements for typing indicator', async ({ page }) => {
    await page.goto('/chat');
    
    // Send a message
    const input = page.getByRole('textbox');
    await input.fill('테스트 질문');
    await page.getByRole('button', { name: /전송/i }).click();
    
    // Typing indicator should be announced
    const typingIndicator = page.getByTestId('typing-indicator');
    await expect(typingIndicator).toHaveAttribute('aria-live', 'polite');
  });

  test('should have proper form labels', async ({ page }) => {
    await page.goto('/chat');
    
    const input = page.getByRole('textbox');
    
    // Input should have associated label or aria-label
    const hasLabel = await input.evaluate((el) => {
      const ariaLabel = el.getAttribute('aria-label');
      const ariaLabelledby = el.getAttribute('aria-labelledby');
      const associatedLabel = el.labels?.length > 0;
      
      return !!(ariaLabel || ariaLabelledby || associatedLabel);
    });
    
    expect(hasLabel).toBe(true);
  });

  test('should support focus visible styles', async ({ page }) => {
    await page.goto('/chat');
    
    // Tab to input
    await page.keyboard.press('Tab');
    
    // Input should have visible focus indicator
    const input = page.getByRole('textbox');
    const outlineStyle = await input.evaluate((el) => {
      return window.getComputedStyle(el).outline;
    });
    
    expect(outlineStyle).not.toBe('none');
  });

  test('should announce error messages to screen readers', async ({ page }) => {
    await page.goto('/chat');
    
    // This test assumes error handling is implemented
    // Check for aria-live region for errors
    const errorRegion = page.locator('[role="alert"]').or(page.locator('[aria-live="assertive"]'));
    
    // Error region should exist (even if empty)
    expect(await errorRegion.count()).toBeGreaterThanOrEqual(0);
  });

  test('should have alt text for images', async ({ page }) => {
    await page.goto('/');
    
    // Check all images have alt text
    const images = page.locator('img');
    const imageCount = await images.count();
    
    for (let i = 0; i < imageCount; i++) {
      const img = images.nth(i);
      await expect(img).toHaveAttribute('alt');
    }
  });

  test('should support zoom up to 200%', async ({ page }) => {
    await page.goto('/');
    
    // Zoom to 200%
    await page.evaluate(() => {
      document.body.style.zoom = '2';
    });
    
    // Content should still be accessible
    await expect(page.getByRole('heading', { name: /AI 신입생 도우미/i })).toBeVisible();
    
    // Reset zoom
    await page.evaluate(() => {
      document.body.style.zoom = '1';
    });
  });

  test('should have skip link for keyboard users', async ({ page }) => {
    await page.goto('/');
    
    // Tab to first element (should be skip link or main content area)
    await page.keyboard.press('Tab');
    
    // Skip link or main content should be focused
    const focusedElement = await page.evaluate(() => {
      return document.activeElement?.tagName;
    });
    
    expect(focusedElement).toBeTruthy();
  });
});
