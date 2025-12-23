import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ChatPanel from './ChatPanel';

describe('ChatPanel', () => {
  it('should render terminal title and input', () => {
    render(<ChatPanel />);
    expect(screen.getByText(/Input Terminal/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Escriba un comando.../i)).toBeInTheDocument();
  });
});
