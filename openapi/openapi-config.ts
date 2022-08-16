import type { ConfigFile } from '@rtk-query/codegen-openapi'

// https://redux-toolkit.js.org/rtk-query/usage/code-generation

const config: ConfigFile = {
  schemaFile: './build/merged.yaml',
  apiFile: '../frontend/src/store/emptyApi.ts',
  hooks: true,
  outputFiles: {
    '../frontend/src/store/trendApi.ts': {
      filterEndpoints: [/trend/i],
    },
    '../frontend/src/store/nodeApi.ts': {
      filterEndpoints: [/node/i],
    },
    '../frontend/src/store/linkApi.ts': {
      filterEndpoints: [/link/i],
    },
    '../frontend/src/store/pipelineApi.ts': {
        filterEndpoints: [/pipeline/i],
    },    
    '../frontend/src/store/eventApi.ts': {
        filterEndpoints: [/event/i],
    },
    '../frontend/src/store/authApi.ts': {
        filterEndpoints: [/auth/i],
    },
  }
}

export default config