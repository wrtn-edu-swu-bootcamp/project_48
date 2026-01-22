import { render, screen } from '@testing-library/react'
import TypingIndicator from '../TypingIndicator'

describe('TypingIndicator', () => {
  it('should render typing indicator', () => {
    render(<TypingIndicator />)
    
    const indicator = screen.getByTestId('typing-indicator')
    expect(indicator).toBeInTheDocument()
  })

  it('should display three dots', () => {
    const { container } = render(<TypingIndicator />)
    
    const dots = container.querySelectorAll('.dot')
    expect(dots).toHaveLength(3)
  })

  it('should have bot avatar', () => {
    render(<TypingIndicator />)
    
    const avatar = screen.getByTestId('bot-avatar')
    expect(avatar).toBeInTheDocument()
  })

  it('should have animation classes', () => {
    const { container } = render(<TypingIndicator />)
    
    const dots = container.querySelectorAll('.dot')
    dots.forEach((dot) => {
      expect(dot).toHaveClass('animate-pulse')
    })
  })

  it('should be accessible', () => {
    render(<TypingIndicator />)
    
    const indicator = screen.getByTestId('typing-indicator')
    expect(indicator).toHaveAttribute('aria-live', 'polite')
    expect(indicator).toHaveAttribute('aria-label', expect.stringContaining('답변'))
  })
})
