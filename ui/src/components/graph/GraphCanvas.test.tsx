import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import GraphCanvas from './GraphCanvas';

describe('GraphCanvas', () => {
  it('should render the graph canvas container', () => {
    render(<GraphCanvas />);
    expect(screen.getByTestId('react-flow-wrapper')).toBeInTheDocument();
  });
});