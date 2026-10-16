import { describe, expect, test } from 'claude-code/testing'

import { fmtTokens, statusLabel } from './format'
import { makeUsage } from './usage-fixture'

describe('fmtTokens', () => {
  test('matches /context formatting', () => {
    expect(fmtTokens(0)).toBe('0')
    expect(fmtTokens(733)).toBe('733')
    expect(fmtTokens(9000)).toBe('9k')
    expect(fmtTokens(17700)).toBe('17.7k')
    expect(fmtTokens(72500)).toBe('72.5k')
    expect(fmtTokens(894500)).toBe('894.5k')
    expect(fmtTokens(1_000_000)).toBe('1M')
    expect(fmtTokens(1_500_000)).toBe('1.5M')
  })
})

describe('statusLabel', () => {
  test('is the percent, then tokens out of the window', () => {
    expect(statusLabel(makeUsage({ tokens: 72_605 }))).toBe('7% · 72.6k/1M')
    expect(statusLabel(makeUsage({ tokens: 244_000 }))).toBe('24% · 244k/1M')
  })

  test('uses the model window, whatever its size', () => {
    expect(statusLabel(makeUsage({ tokens: 50_000, window: 200_000 }))).toBe('25% · 50k/200k')
  })

  test('is undefined before the window has had a response', () => {
    expect(statusLabel(makeUsage())).toBeUndefined()
  })

  test('shows past 100% when over the window', () => {
    expect(statusLabel(makeUsage({ tokens: 1_100_000 }))).toBe('110% · 1.1M/1M')
  })
})
