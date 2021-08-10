// neo4j-driver.js
const neo4j = require('neo4j-driver')
const db = 'bolt://localhost:7687' // http://localhost:7474 bolt://localhost:7687
const dbuser = 'neo4j'
const dbpassword = 'rdxsdzxgc'
// 连接数据库
const driver = neo4j.driver(db, neo4j.auth.basic(dbuser, dbpassword),{
  maxTransactionRetryTime: 30000
})

// 具体示例，这里的例子是查询某个node的关系网络
const getJson =  async (query) => {
  return new Promise((resolve, reject) => {
    // 连接数据库
    const driver = neo4j.driver(db, neo4j.auth.basic(dbuser, dbpassword),{
      maxTransactionRetryTime: 30000
    })
    // 启动根查询
	if(query.includes('>=')){
		query = query.replace('>=','≥');
	}
	if(query.includes('<=')){
		query = query.replace('<=','≤');
	}
	if(query.includes('alpha-')){
		query = query.replace('alpha-','α-');
	}
	if(query.includes('beta-')){
		query = query.replace('beta-','β-');
	}
	if(query.includes('omega-')){
		query = query.replace('omega-','ω-');
	}
	if(query.includes('mu_g')){
		query = query.replace('mu_g','μg');
	}
	if(query.includes('*')){
		query = query.replace('*','×');
	}
    const cql_root = `MATCH (n:Lifestyle) where n.name='${query}'RETURN n LIMIT 1`
    let cql_name = ''
    let json = {} // 最终结果集
    const session1 = driver.session()
    // const root = await session.run(statement, params)
    session1.run(cql_root).subscribe({
      onKeys: keys => {
        console.log(keys)
      },
      onNext: record => {
        console.log(record.get('n').properties.name)
        cql_name = record.get('n').properties.name // 拿到查询结果
      },
      onCompleted: () => {
        session1.close() // returns a Promise
        // 下一个查询语句
        //const statement = `MATCH p=(n:Lifestyle{name: '${cql_name }'})-[]-() RETURN p`
		const statement = `MATCH p=(n:Lifestyle{name: '${cql_name}'})-[]-()-[:outcomes_of_pcatype]-(s) WHERE s.index_name = n.name WITH n,p MATCH q=(n)-[:baselines_of_lfst|first_class|second_class|third_class|nations_of_lfst|units_of_lfst|related_papers]-() RETURN p,q`
        // 根据结果查询关联企业
        const session2 = driver.session()
        // const result = await session.run(statement, params)
        // const result = await session2.run(statement)
        session2.run(statement).then(result => { // 异步处理
          console.log(result)
          // 此处可自行拓展
          // 可以把结果加到最终结果集中，也可以通过forEach遍历处理后再加进去
          json.data = result.records
        }).catch(error => {
          console.log(error)
        })
        .then(() => {
          session2.close()
          driver.close()
          resolve(json) // 在这里返回json数据集
        })
      },
      onError: error => {
        console.log(error)
      }
    })
  })
}

module.exports = {
  getJson
}