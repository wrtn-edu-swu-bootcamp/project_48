import { render, screen } from '@testing-library/react'
import ChatArea from '../ChatArea'

describe('ChatArea', () => {
  const mockMessages = [
    {
      id: '1',
      role: 'user' as const,
      content: '수강신청은 언제 하나요?',
      timestamp: new Date('2025-01-22T10:00:00'),
    },
    {
      id: '2',
      role: 'assistant' as const,
      content: '1학기 수강신청은 3월 1일부터 3월 5일까지입니다.',
      timestamp: new Date('2025-01-22T10:00:05'),
      sources: [
        {
          title: '2025학년도 학사일정',
          source_type: 'academic_schedule',
        },
      ],
    },
  ]

  it('should render without crashing', () => {
    render(<ChatArea messages={[]} isLoading={false} />)
    expect(screen.getByRole('log')).toBeInTheDocument()
  })

  it('should display user and bot messages', () => {
    render(<ChatArea messages={mockMessages} isLoading={false} />)
    
    expect(screen.getByText('수강신청은 언제 하나요?')).toBeInTheDocument()
    expect(screen.getByText(/1학기 수강신청은 3월 1일부터/)).toBeInTheDocument()
  })

  it('should show typing indicator when loading', () => {
    render(<ChatArea messages={mockMessages} isLoading={true} />)
    
    expect(screen.getByTestId('typing-indicator')).toBeInTheDocument()
  })

  it('should display welcome message when no messages', () => {
    render(<ChatArea messages={[]} isLoading={false} />)
    
    expect(screen.getByText(/안녕하세요/)).toBeInTheDocument()
  })

  it('should display sources for bot messages', () => {
    render(<ChatArea messages={mockMessages} isLoading={false} />)
    
    expect(screen.getByText('2025학년도 학사일정')).toBeInTheDocument()
  })

  it('should apply correct ARIA attributes', () => {
    render(<ChatArea messages={mockMessages} isLoading={false} />)
    
    const chatLog = screen.getByRole('log')
    expect(chatLog).toHaveAttribute('aria-label', expect.stringContaining('대화'))
  })
})
