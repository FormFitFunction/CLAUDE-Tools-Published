import { describe, expect, test } from 'claude-code/testing'

import { makeUsage } from './usage-fixture'
import type { FixtureOptions } from './usage-fixture'

type Hook = (event: string, fn: (...a: never[]) => unknown) => void

const START = { source: 'startup', cwd: '/x', surface: 'desktop', isInteractive: true }
const DONE = { answer: 'done' }
const MESSAGE = { role: 'user', text: 'hi', toolUses: [] }

type Engine = {
  turn: { complete: (e: never) => Promise<unknown> }
  session: { start: (e: never) => Promise<unknown>; compact: (e: never) => Promise<unknown> }
}

// What the engine answers beneath the plugin: usage, the status line, and the events the plugin passes on.
const engine = (on: unknown, usage: (args: unknown) => unknown) => {
  const hook = on as Hook
  const statuses: (string | undefined)[] = []
  const asked: unknown[] = []
  hook('session.usage', ((_$: never, args: unknown) => {
    asked.push(args)

    return { value: usage(args) }
  }) as never)
  hook('ui.status', ((_$: never, e: { text: string | undefined }) => {
    statuses.push(e.text)

    return { value: undefined }
  }) as never)
  hook('turn.complete', () => ({ text: 'done' }) as never)
  hook('session.start', ((_$: never, e: { cwd: string }) => ({ cwd: e.cwd })) as never)
  hook('session.compact', ((_$: never, e: { messages: unknown[] }) => ({ messages: e.messages })) as never)

  return { statuses, asked }
}

describe('status line', () => {
  test('is set when the session starts', async ($, on) => {
    const { statuses } = engine(on, () => makeUsage({ tokens: 72_605 }))

    await ($ as Engine).session.start(START as never)

    expect(statuses.at(-1)).toBe('7% · 72.6k/1M')
  })

  test('updates when a turn completes', async ($, on) => {
    let current: FixtureOptions = { tokens: 72_605 }
    const { statuses } = engine(on, () => makeUsage(current))

    await ($ as Engine).turn.complete(DONE as never)
    expect(statuses.at(-1)).toBe('7% · 72.6k/1M')
    current = { tokens: 300_000 }
    await ($ as Engine).turn.complete(DONE as never)
    expect(statuses.at(-1)).toBe('30% · 300k/1M')
  })

  test('updates after compaction', async ($, on) => {
    let current: FixtureOptions = { tokens: 800_000 }
    const { statuses } = engine(on, () => makeUsage(current))

    await ($ as Engine).turn.complete(DONE as never)
    current = { tokens: 60_000 }
    await ($ as Engine).session.compact({ messages: [MESSAGE] } as never)

    expect(statuses.at(-1)).toBe('6% · 60k/1M')
  })

  test('clears the line while there is nothing to show yet', async ($, on) => {
    const { statuses } = engine(on, () => makeUsage())

    await ($ as Engine).session.start(START as never)

    expect(statuses).toEqual([undefined])
  })

  test('keeps the last reading when usage cannot be read', async ($, on) => {
    let isBroken = false
    const { statuses } = engine(on, () => {
      if (isBroken) throw new Error('no session')

      return makeUsage({ tokens: 72_605 })
    })

    await ($ as Engine).turn.complete(DONE as never)
    isBroken = true
    await ($ as Engine).turn.complete(DONE as never)

    expect(statuses).toEqual(['7% · 72.6k/1M'])
  })

  test('never asks for the breakdown, so a refresh is free', async ($, on) => {
    const { asked } = engine(on, () => makeUsage({ tokens: 72_605 }))

    await ($ as Engine).session.start(START as never)
    await ($ as Engine).turn.complete(DONE as never)

    expect(asked.length).toBeGreaterThan(0)
    expect(asked.every(args => (args as { breakdown?: unknown } | undefined)?.breakdown === undefined)).toBe(true)
  })
})
