import { render, screen } from '@testing-library/react'
import BotMessage from '../BotMessage'

describe('BotMessage', () => {
  const mockMessage = {
    content: '1학기 수강신청은 3월 1일부터 3월 5일까지입니다.',
    timestamp: new Date('2025-01-22T10:00:05'),
    sources: [
      {
        title: '2025학년도 학사일정',
        source_type: 'academic_schedule',
      },
    ],
  }

  it('should render bot message content', () => {
    render(
      <BotMessage
        message={mockMessage.content}
        timestamp={mockMessage.timestamp}
        sources={mockMessage.sources}
      />
    )
    
    expect(screen.getByText(/1학기 수강신청은 3월 1일부터/)).toBeInTheDocument()
  })

  it('should display sources', () => {
    render(
      <BotMessage
        message={mockMessage.content}
        timestamp={mockMessage.timestamp}
        sources={mockMessage.sources}
      />
    )
    
    expect(screen.getByText('2025학년도 학사일정')).toBeInTheDocument()
  })

  it('should display bot avatar', () => {
    render(
      <BotMessage
        message={mockMessage.content}
        timestamp={mockMessage.timestamp}
        sources={mockMessage.sources}
      />
    )
    
    const avatar = screen.getByTestId('bot-avatar')
    expect(avatar).toBeInTheDocument()
  })

  it('should render without sources', () => {
    render(
      <BotMessage
        message={mockMessage.content}
        timestamp={mockMessage.timestamp}
      />
    )
    
    expect(screen.getByText(/1학기 수강신청은 3월 1일부터/)).toBeInTheDocument()
    expect(screen.queryByText('출처')).not.toBeInTheDocument()
  })

  it('should handle markdown content', () => {
    const markdownMessage = '# 제목\n\n**굵은 글씨**\n\n- 항목 1\n- 항목 2'
    render(
      <BotMessage
        message={markdownMessage}
        timestamp={mockMessage.timestamp}
      />
    )
    
    expect(screen.getByText('제목')).toBeInTheDocument()
  })

  it('should display timestamp', () => {
    render(
      <BotMessage
        message={mockMessage.content}
        timestamp={mockMessage.timestamp}
        sources={mockMessage.sources}
      />
    )
    
    expect(screen.getByText(/10:00/)).toBeInTheDocument()
  })

  it('should align to the left', () => {
    const { container } = render(
      <BotMessage
        message={mockMessage.content}
        timestamp={mockMessage.timestamp}
        sources={mockMessage.sources}
      />
    )
    
    const wrapper = container.firstChild
    expect(wrapper).toHaveClass('flex', 'justify-start')
  })

  it('should display multiple sources', () => {
    const multipleSources = [
      { title: '출처 1', source_type: 'academic_schedule' },
      { title: '출처 2', source_type: 'notice' },
      { title: '출처 3', source_type: 'support_program' },
    ]
    
    render(
      <BotMessage
        message={mockMessage.content}
        timestamp={mockMessage.timestamp}
        sources={multipleSources}
      />
    )
    
    expect(screen.getByText('출처 1')).toBeInTheDocument()
    expect(screen.getByText('출처 2')).toBeInTheDocument()
    expect(screen.getByText('출처 3')).toBeInTheDocument()
  })
})
