const router = require('koa-router')()
const {getJson} = require('./q_driver.js')

router.get('/', async (ctx, next) => {
  await ctx.render('index', {
    title: 'Hello Koa 2!'
  })
})

router.get('/chatbot', async (ctx, next) => {
  ctx.body = {
    title: 'Chatbot for pcadblist!'
  }
})

// 获取neo4j数据的url
router.get('/neo4j', async (ctx, next) => {
  const params = ctx.request.query
  await getJson(params.query).then((res) => {
    ctx.body = res;
  }).catch(next);
})

module.exports = router
