import type { SessionUsage } from 'claude-code'

const tenth = (n: number) => String(Math.round(n * 10) / 10)

/** `/context` formatting: 733, 9k, 17.7k, 894.5k, 1M. */
export const fmtTokens = (tokens: number): string => {
  if (tokens >= 1_000_000) return `${tenth(tokens / 1_000_000)}M`
  if (tokens >= 1000) return `${tenth(tokens / 1000)}k`

  return String(Math.round(tokens))
}

/** The status line text, `7% · 72.6k/1M`; undefined until the window has had a response. */
export const statusLabel = ({ context }: SessionUsage): string | undefined => {
  if (context.tokens === undefined) return undefined

  return `${Math.round((context.tokens / context.window) * 100)}% · ${fmtTokens(context.tokens)}/${fmtTokens(context.window)}`
}
