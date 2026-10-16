import type { SessionUsage } from 'claude-code'

export type FixtureOptions = {
  /** Input tokens of the last response; leave out for a window with no response yet. */
  tokens?: number
  window?: number
}

export const makeUsage = (options: FixtureOptions = {}): SessionUsage =>
  ({
    startedAt: 0,
    context: { window: options.window ?? 1_000_000, ...(options.tokens === undefined ? {} : { tokens: options.tokens }) },
    rateLimits: [],
  }) as unknown as SessionUsage
