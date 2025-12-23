import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import NodeManager from './NodeManager';

describe('NodeManager', () => {
  it('should render agents health', () => {
    render(<NodeManager />);
    expect(screen.getByText(/AGENTS_STATUS/i)).toBeInTheDocument();
    expect(screen.getByText(/Vision/i)).toBeInTheDocument();
    expect(screen.getByText(/Guardian/i)).toBeInTheDocument();
  });
});
