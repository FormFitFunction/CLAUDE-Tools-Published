import type { EngineInterface, Register } from 'claude-code'

import { statusLabel } from './format'

// No breakdown is requested, so a refresh is free: `$.session.usage()` with no arguments only reads the status line's figures.
const refresh = async ($: EngineInterface) => {
  try {
    $.ui.status(statusLabel(await $.session.usage()))
  } catch {
    // Keep the last reading; the next event tries again.
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await refresh($)

    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    await refresh($)

    return next(e)
  })

  on('session.compact', async ($, e, next) => {
    const result = await next(e)
    await refresh($)

    return result
  }).catch(($, e, next) => next(e))
}
