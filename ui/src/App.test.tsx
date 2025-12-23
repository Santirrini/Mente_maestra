import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('Dashboard Layout', () => {
  it('should render the core dashboard components', () => {
    render(<App />);
    expect(screen.getByTestId('chat-panel')).toBeInTheDocument();
    expect(screen.getByTestId('blackboard-view')).toBeInTheDocument();
    expect(screen.getByTestId('state-machine-view')).toBeInTheDocument();
    expect(screen.getByTestId('governance-module')).toBeInTheDocument();
  });
});
