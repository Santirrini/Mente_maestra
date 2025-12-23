import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('Main Layout', () => {
  it('should render the three main panels', () => {
    render(<App />);
    expect(screen.getByTestId('chat-panel')).toBeInTheDocument();
    expect(screen.getByTestId('graph-panel')).toBeInTheDocument();
    expect(screen.getByTestId('log-panel')).toBeInTheDocument();
  });
});
