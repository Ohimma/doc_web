// 1. 引入required模块
const http = require('http')

const hostname = '127.0.0.1'
const port = 3000

// 2. 创建 http 服务器
// 3. 定义 请求与响应
const server = http.createServer((req, res) => {
  res.statusCode = 200
  res.setHeader('Content-Type', 'text/plain')
  res.end('Hello world\n')
})

// 4. 监听启动
server.listen(port, hostname, () => {
  console.log(`服务器运行在 http://${hostname}:${port}/`)
})
