import React from 'react';
import { render } from '@testing-library/react';
import { ExampleComponent } from './ExampleComponent';
import { TestApiProvider } from '@backstage/test-utils';

describe('ExampleComponent', () => {
  it('should render without crashing', () => {
    const rendered = render(
      <TestApiProvider apis={[]}>
        <ExampleComponent />
      </TestApiProvider>
    );
    expect(rendered.getByText('Mi Primer Componente')).toBeInTheDocument();
  });

  it('should display welcome message', () => {
    const rendered = render(
      <TestApiProvider apis={[]}>
        <ExampleComponent />
      </TestApiProvider>
    );
    expect(rendered.getByText(/primer componente personalizado/i)).toBeInTheDocument();
  });

  it('should display all feature cards', () => {
    const rendered = render(
      <TestApiProvider apis={[]}>
        <ExampleComponent />
      </TestApiProvider>
    );
    expect(rendered.getByText('🎨 Personalización')).toBeInTheDocument();
    expect(rendered.getByText('🔌 Integración')).toBeInTheDocument();
    expect(rendered.getByText('📊 Datos')).toBeInTheDocument();
    expect(rendered.getByText('🚀 Próximos Pasos')).toBeInTheDocument();
  });
});
