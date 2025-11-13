const { deepMerge } = require('hexo-util')
const path = require('path')

// Cache default config to avoid repeated file reads
let cachedDefaultConfig = null

/**
 * Check Hexo version and configuration
 */
function checkHexoEnvironment (hexo) {
  const { version, log, locals } = hexo

  const [major, minor] = version.split('.').map(Number)
  const requiredMajor = 5
  const requiredMinor = 3

  if (major < requiredMajor || (major === requiredMajor && minor < requiredMinor)) {
    log.error('Please update Hexo to V5.3.0 or higher!')
    log.error('請把 Hexo 升級到 V5.3.0 或更高的版本！')
    process.exit(-1)
  }

  // Check for deprecated configuration file
  if (locals.get) {
    const data = locals.get('data')
    if (data && data.butterfly) {
      log.error("'butterfly.yml' is deprecated. Please use '_config.butterfly.yml'")
      log.error("'butterfly.yml' 已經棄用，請使用 '_config.butterfly.yml'")
      process.exit(-1)
    }
  }
}
