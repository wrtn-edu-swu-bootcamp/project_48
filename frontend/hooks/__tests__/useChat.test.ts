import { renderHook, act, waitFor } from '@testing-library/react'
import useChat from '../useChat'
import * as chatAPI from '@/lib/chatAPI'

// Mock the chatAPI module
jest.mock('@/lib/chatAPI')

describe('useChat', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('should initialize with empty messages', () => {
    const { result } = renderHook(() => useChat())
    
    expect(result.current.messages).toEqual([])
    expect(result.current.isLoading).toBe(false)
    expect(result.current.error).toBeNull()
  })

  it('should send message and update messages', async () => {
    const mockResponse = {
      answer: '1학기 수강신청은 3월 1일부터 3월 5일까지입니다.',
      sources: [
        { title: '2025학년도 학사일정', source_type: 'academic_schedule' },
      ],
    }
    
    ;(chatAPI.sendMessage as jest.Mock).mockResolvedValue(mockResponse)
    
    const { result } = renderHook(() => useChat())
    
    await act(async () => {
      await result.current.sendMessage('수강신청은 언제 하나요?')
    })
    
    expect(result.current.messages).toHaveLength(2)
    expect(result.current.messages[0].role).toBe('user')
    expect(result.current.messages[0].content).toBe('수강신청은 언제 하나요?')
    expect(result.current.messages[1].role).toBe('assistant')
    expect(result.current.messages[1].content).toContain('3월 1일')
  })

  it('should set loading state during API call', async () => {
    let resolvePromise: any
    const promise = new Promise((resolve) => {
      resolvePromise = resolve
    })
    
    ;(chatAPI.sendMessage as jest.Mock).mockReturnValue(promise)
    
    const { result } = renderHook(() => useChat())
    
    act(() => {
      result.current.sendMessage('테스트 질문')
    })
    
    expect(result.current.isLoading).toBe(true)
    
    await act(async () => {
      resolvePromise({ answer: '답변', sources: [] })
      await promise
    })
    
    expect(result.current.isLoading).toBe(false)
  })

  it('should handle API errors', async () => {
    const mockError = new Error('API Error')
    ;(chatAPI.sendMessage as jest.Mock).mockRejectedValue(mockError)
    
    const { result } = renderHook(() => useChat())
    
    await act(async () => {
      await result.current.sendMessage('테스트 질문')
    })
    
    expect(result.current.error).toBeTruthy()
    expect(result.current.isLoading).toBe(false)
  })

  it('should not send empty messages', async () => {
    const { result } = renderHook(() => useChat())
    
    await act(async () => {
      await result.current.sendMessage('')
    })
    
    expect(chatAPI.sendMessage).not.toHaveBeenCalled()
    expect(result.current.messages).toHaveLength(0)
  })

  it('should clear messages', () => {
    const { result } = renderHook(() => useChat())
    
    act(() => {
      result.current.sendMessage('테스트 질문')
    })
    
    act(() => {
      result.current.clearMessages()
    })
    
    expect(result.current.messages).toHaveLength(0)
  })

  it('should handle multiple messages in sequence', async () => {
    const mockResponse1 = { answer: '답변 1', sources: [] }
    const mockResponse2 = { answer: '답변 2', sources: [] }
    
    ;(chatAPI.sendMessage as jest.Mock)
      .mockResolvedValueOnce(mockResponse1)
      .mockResolvedValueOnce(mockResponse2)
    
    const { result } = renderHook(() => useChat())
    
    await act(async () => {
      await result.current.sendMessage('질문 1')
    })
    
    await act(async () => {
      await result.current.sendMessage('질문 2')
    })
    
    expect(result.current.messages).toHaveLength(4)
    expect(chatAPI.sendMessage).toHaveBeenCalledTimes(2)
  })
})
