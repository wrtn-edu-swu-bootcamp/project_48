import { render, screen } from '@testing-library/react'
import UserMessage from '../UserMessage'

describe('UserMessage', () => {
  const mockMessage = {
    content: '수강신청은 언제 하나요?',
    timestamp: new Date('2025-01-22T10:00:00'),
  }

  it('should render user message content', () => {
    render(<UserMessage message={mockMessage.content} timestamp={mockMessage.timestamp} />)
    
    expect(screen.getByText('수강신청은 언제 하나요?')).toBeInTheDocument()
  })

  it('should display timestamp', () => {
    render(<UserMessage message={mockMessage.content} timestamp={mockMessage.timestamp} />)
    
    // Check for time display (format may vary)
    expect(screen.getByText(/10:00/)).toBeInTheDocument()
  })

  it('should have correct styling classes', () => {
    const { container } = render(
      <UserMessage message={mockMessage.content} timestamp={mockMessage.timestamp} />
    )
    
    // Check for user message specific classes
    const messageElement = container.querySelector('.user-message')
    expect(messageElement).toBeInTheDocument()
  })

  it('should align to the right', () => {
    const { container } = render(
      <UserMessage message={mockMessage.content} timestamp={mockMessage.timestamp} />
    )
    
    const wrapper = container.firstChild
    expect(wrapper).toHaveClass('flex', 'justify-end')
  })

  it('should handle long messages', () => {
    const longMessage = '이것은 매우 긴 메시지입니다. '.repeat(50)
    render(<UserMessage message={longMessage} timestamp={mockMessage.timestamp} />)
    
    expect(screen.getByText(longMessage)).toBeInTheDocument()
  })

  it('should handle messages with newlines', () => {
    const multilineMessage = '첫 번째 줄\n두 번째 줄\n세 번째 줄'
    render(<UserMessage message={multilineMessage} timestamp={mockMessage.timestamp} />)
    
    expect(screen.getByText(/첫 번째 줄/)).toBeInTheDocument()
  })
})
