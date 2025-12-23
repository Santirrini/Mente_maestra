import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import LogPanel from './LogPanel';

describe('LogPanel', () => {
  it('should render blackboard title', () => {
    render(<LogPanel />);
    expect(screen.getByText(/BLACKBOARD_LOGS/i)).toBeInTheDocument();
  });
});
