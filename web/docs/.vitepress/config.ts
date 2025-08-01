import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Auto Doc Server',
  description: '自动为Python项目生成美观的文档',
  lang: 'zh-CN',
  
  themeConfig: {
    siteTitle: 'Auto Doc Server',
    nav: [
      { text: '首页', link: '/' },
      { text: '生成的文档', link: '/generated/' },
      { text: 'GitHub', link: 'https://github.com/your-repo' }
    ],
    
    sidebar: {
      '/generated/': [
        {
          text: '生成的文档',
          items: [
            { text: '文档首页', link: '/generated/' },
            { text: '项目概览', link: '/generated/overview' },
            { text: '示例模块', link: '/generated/example_module' },
          ]
        }
      ]
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/your-repo' },
    ],
    
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2024 Auto Doc Server'
    },
    
    search: {
      provider: 'local'
    }
  },
  
  markdown: {
    theme: 'material-theme-palenight',
    lineNumbers: true,
    toc: {
      level: [1, 2, 3]
    }
  },
  
  vite: {
    server: {
      port: 3000,
      host: 'localhost'
    }
  }
}) 