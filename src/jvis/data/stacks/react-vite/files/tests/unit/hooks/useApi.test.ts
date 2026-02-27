import { describe, it, expect } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useApi } from '../../../src/hooks/useApi';

describe('useApi', () => {
  it('should start with initial state', () => {
    const { result } = renderHook(() => useApi<string>());
    expect(result.current.data).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('should set data on success', async () => {
    const { result } = renderHook(() => useApi<string>());

    await act(async () => {
      await result.current.execute(() => Promise.resolve('hello'));
    });

    expect(result.current.data).toBe('hello');
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('should set error on failure', async () => {
    const { result } = renderHook(() => useApi<string>());

    await act(async () => {
      try {
        await result.current.execute(() => Promise.reject(new Error('fail')));
      } catch {
        // expected
      }
    });

    expect(result.current.data).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe('fail');
  });
});
