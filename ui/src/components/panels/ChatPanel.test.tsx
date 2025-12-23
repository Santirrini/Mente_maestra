import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ChatPanel from './ChatPanel';

describe('ChatPanel', () => {
  it('should render chat title and input', () => {
    render(<ChatPanel />);
    expect(screen.getByText(/SYNPSE_CHAT/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enviar comando.../i)).toBeInTheDocument();
  });
});
