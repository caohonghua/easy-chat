import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import MarkdownIt from 'markdown-it'
import mdHighlightjs from 'markdown-it-highlightjs'
import 'highlight.js/styles/github.css'

const app = createApp(App)

app.use(router)


// 定义全局函数 - mdRender
app.config.globalProperties.$mdRender = function(mdContent) {
    const md = new MarkdownIt()
    md.use(mdHighlightjs)
    return md.render(mdContent)
}

app.mount('#app')

