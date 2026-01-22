import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import InputArea from '../InputArea'

describe('InputArea', () => {
  const mockOnSend = jest.fn()

  beforeEach(() => {
    mockOnSend.mockClear()
  })

  it('should render input field and send button', () => {
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    expect(screen.getByRole('textbox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /전송/i })).toBeInTheDocument()
  })

  it('should update input value when typing', async () => {
    const user = userEvent.setup()
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    const input = screen.getByRole('textbox')
    await user.type(input, '수강신청은 언제 하나요?')
    
    expect(input).toHaveValue('수강신청은 언제 하나요?')
  })

  it('should call onSend when send button is clicked', async () => {
    const user = userEvent.setup()
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    const input = screen.getByRole('textbox')
    const sendButton = screen.getByRole('button', { name: /전송/i })
    
    await user.type(input, '수강신청은 언제 하나요?')
    await user.click(sendButton)
    
    expect(mockOnSend).toHaveBeenCalledWith('수강신청은 언제 하나요?')
  })

  it('should call onSend when Enter key is pressed', async () => {
    const user = userEvent.setup()
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    const input = screen.getByRole('textbox')
    await user.type(input, '수강신청은 언제 하나요?{Enter}')
    
    expect(mockOnSend).toHaveBeenCalledWith('수강신청은 언제 하나요?')
  })

  it('should clear input after sending', async () => {
    const user = userEvent.setup()
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    const input = screen.getByRole('textbox')
    await user.type(input, '테스트 메시지')
    await user.click(screen.getByRole('button', { name: /전송/i }))
    
    expect(input).toHaveValue('')
  })

  it('should not send empty messages', async () => {
    const user = userEvent.setup()
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    const sendButton = screen.getByRole('button', { name: /전송/i })
    await user.click(sendButton)
    
    expect(mockOnSend).not.toHaveBeenCalled()
  })

  it('should disable input and button when loading', () => {
    render(<InputArea onSend={mockOnSend} isLoading={true} />)
    
    expect(screen.getByRole('textbox')).toBeDisabled()
    expect(screen.getByRole('button', { name: /전송/i })).toBeDisabled()
  })

  it('should have proper placeholder text', () => {
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    expect(screen.getByPlaceholderText(/궁금한 것을 물어보세요/i)).toBeInTheDocument()
  })

  it('should support Shift+Enter for newline', async () => {
    const user = userEvent.setup()
    render(<InputArea onSend={mockOnSend} isLoading={false} />)
    
    const input = screen.getByRole('textbox')
    await user.type(input, '첫 줄{Shift>}{Enter}{/Shift}두 번째 줄')
    
    // Should not have called onSend
    expect(mockOnSend).not.toHaveBeenCalled()
  })
})
