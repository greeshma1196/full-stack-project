import { render, screen } from '@testing-library/react';
import WebScrapper from './WebScrapper';

test('renders learn react link', () => {
  render(<WebScrapper />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
