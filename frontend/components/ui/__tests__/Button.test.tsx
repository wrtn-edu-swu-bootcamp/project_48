import { render, screen, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Button from '../Button'

describe('Button', () => {
  it('should render button with text', () => {
    render(<Button>Click me</Button>)
    
    expect(screen.getByRole('button', { name: 'Click me' })).toBeInTheDocument()
  })

  it('should call onClick when clicked', async () => {
    const user = userEvent.setup()
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    await user.click(screen.getByRole('button'))
    
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('should not call onClick when disabled', async () => {
    const user = userEvent.setup()
    const handleClick = jest.fn()
    render(<Button onClick={handleClick} disabled>Click me</Button>)
    
    await user.click(screen.getByRole('button'))
    
    expect(handleClick).not.toHaveBeenCalled()
  })

  it('should apply primary variant styles', () => {
    const { container } = render(<Button variant="primary">Primary</Button>)
    
    const button = container.querySelector('button')
    expect(button).toHaveClass('bg-burgundy')
  })

  it('should apply secondary variant styles', () => {
    const { container } = render(<Button variant="secondary">Secondary</Button>)
    
    const button = container.querySelector('button')
    expect(button).toHaveClass('border-burgundy')
  })

  it('should apply different sizes', () => {
    const { container: smallContainer } = render(<Button size="small">Small</Button>)
    const { container: largeContainer } = render(<Button size="large">Large</Button>)
    
    const smallButton = smallContainer.querySelector('button')
    const largeButton = largeContainer.querySelector('button')
    
    expect(smallButton).toHaveClass('h-9')
    expect(largeButton).toHaveClass('h-13')
  })

  it('should be keyboard accessible', async () => {
    const user = userEvent.setup()
    const handleClick = jest.fn()
    render(<Button onClick={handleClick}>Button</Button>)
    
    const button = screen.getByRole('button')
    button.focus()
    
    expect(button).toHaveFocus()
    
    await user.keyboard('{Enter}')
    expect(handleClick).toHaveBeenCalled()
  })

  it('should display loading state', () => {
    render(<Button isLoading>Loading</Button>)
    
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument()
  })

  it('should support fullWidth prop', () => {
    const { container } = render(<Button fullWidth>Full Width</Button>)
    
    const button = container.querySelector('button')
    expect(button).toHaveClass('w-full')
  })
})
