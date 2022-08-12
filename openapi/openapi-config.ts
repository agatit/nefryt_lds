import type { ConfigFile } from '@rtk-query/codegen-openapi'

// https://redux-toolkit.js.org/rtk-query/usage/code-generation

const config: ConfigFile = {
  schemaFile: './build/merged.yaml',
  apiFile: '../frontend.test/src/store/emptyApi.ts',
  outputFiles: {
    '../frontend.test/src/store/trend.ts': {
      filterEndpoints: [/trend/i],
    },
    '../frontend.test/src/store/node.ts': {
      filterEndpoints: [/node/i],
    },
    '../frontend.test/src/store/link.ts': {
      filterEndpoints: [/link/i],
    },
    '../frontend.test/src/store/pipeline.ts': {
        filterEndpoints: [/pipeline/i],
    },    
    '../frontend.test/src/store/event.ts': {
        filterEndpoints: [/event/i],
    },
    '../frontend.test/src/store/auth.ts': {
        filterEndpoints: [/auth/i],
    },
  }
}

export default config