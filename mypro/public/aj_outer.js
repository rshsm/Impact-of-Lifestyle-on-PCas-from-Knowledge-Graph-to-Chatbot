//定义name变量制作图标
var names = ['Lifestyle', 'Paper', 'Nation', 'PCA_Cancer', 'Unit', 'FirClass', 'SecClass', 'ThrClass', 'Baseline', 'Outcome', 'Gene'];
var colors = ['#006BB0', '#EFA90D', '#800080', '#DC2F1F', '#795749', '#cfaca5', '#3894a6', '#a9e5bd', '#059341', '#a876d9', '#B93A85'];


//背景颜色设置 补充CSS样式设置字体布局
for (var i=0; i < names.length; i++) {
	$('#indicator').append("<div><span style='background-color:" + colors[i] + "'></span>" + names[i] + "</div>");
}

// 图数据
let nodes = []
let links = []	 // 存放节点和关系
let nodeSet = [] // 存放去重后nodes的id

var graph = data
console.log(graph[0].p)

for (let item of graph) {
	// console.log(item.p.start instanceof Array)
	// console.log(item.p)
	// 重新更改data格式
	if(nodeSet.indexOf(item.p.start.identity.low) == -1){
		nodeSet.push(item.p.start.identity.low)
		nodes.push({
			id: item.p.start.identity.low,
			label: item.p.start.labels[0],
			properties: item.p.start.properties
		})
	}
	if(nodeSet.indexOf(item.p.end.identity.low) == -1){
		nodeSet.push(item.p.end.identity.low)
		nodes.push({
			id: item.p.end.identity.low,
			label: item.p.end.labels[0],
			properties: item.p.end.properties
		})
	}
	links.push({
		source: item.p.segments[0].relationship.start.low,
		target: item.p.segments[0].relationship.end.low,
		type: item.p.segments[0].relationship.type,
		properties: item.p.segments[0].relationship.properties
	})
}

//处理三种类
/* for(var i=0;i<nodes.length;i++){
	if(nodes[i].label == 'FirClass' || nodes[i].label == 'SecClass' || nodes[i].label == 'ThrClass'){
		nodes[i].properties.name = ' '+nodes[i].properties.name
	}
} */

console.log(nodes)
console.log(links)
//
if(links.length > 100 && links.length <= 500){
	$("#svgouter").attr('style', 'width:800px;height:550px;margin-bottom:10px;text-align:center;left:180px;position:relative;border: 2px solid lightgrey; overflow: scroll;');
	$("#svg1").attr('width', '1000');
	$("#svg1").attr('height', '800');
}
if(links.length > 500 && links.length <= 1000){
	$("#svgouter").attr('style', 'width:800px;height:550px;margin-bottom:10px;text-align:center;left:180px;position:relative;border: 2px solid lightgrey; overflow: scroll;');
	$("#svg1").attr('width', '1100');
	$("#svg1").attr('height', '1200');
}
if(links.length > 1000){
	$("#svgouter").attr('style', 'width:800px;height:550px;margin-bottom:10px;text-align:center;left:180px;position:relative;border: 2px solid lightgrey; overflow: scroll;');
	$("#svg1").attr('width', '1400');
	$("#svg1").attr('height', '1600');
}


//标题显示lifestyle的名字
function title_dis(testlist){
	for(var i=0;i<testlist.length;i++)
	{
		if (testlist[i].label == 'Lifestyle')
		{
			lfst_title = testlist[i].properties.name;
			break;
		}
	}
	return lfst_title;
}
//显示标题lfst, 节点及关系总数
document.getElementById("lfst").innerHTML="lifestyle_name: \" "+title_dis(nodes)+" \" ";
document.getElementById('ents_len').innerText=nodes.length;
document.getElementById('links_len').innerText=links.length;

//定义svg变量将布局svg1选出来
var svg = d3.select("#svg1");
var width = svg.attr("width");
var height = svg.attr("height");
/* svg.call(d3.zoom().on("zoom", 
			function(){svg.attr("transform", d3.event.transform)
			})).append("g"); */


//利用d3.forceSimulation()定义关系图 包括设置边link、排斥电荷charge、关系图中心点
var simulation = d3.forceSimulation()
		.force("link", d3.forceLink().id(d => {
			// console.log(d)
			return d.id
		}))
		.force("charge", d3.forceManyBody())
		.force("center", d3.forceCenter(width / 2, height / 2))
		.force("collision", d3.forceCollide(18)) // 碰撞检测
//D3映射数据至HTML中
//g用于绘制所有边,selectALL选中所有的line,并绑定数据data(graph.links),enter().append("line")添加元素
//数据驱动文档,设置边的粗细
var link = svg.append("g").attr("class","links").selectAll("line").data(links).enter()
.append("line").attr("stroke-width", function(d) {
	// 每次访问links的一项数据
	return 1.5 //所有线宽度均为2
});

//添加所有的点
//selectAll("circle")选中所有的圆并绑定数据,圆的直径为d.size
//再定义圆的填充色,同样数据驱动样式,圆没有描边,圆的名字为d.id
//call()函数：拖动函数,当拖动开始绑定dragstarted函数，拖动进行和拖动结束也绑定函数
var node = svg.append("g").attr("class", "nodes").selectAll("circle").data(nodes).enter()
.append("circle").attr("r", function(d) {
	// 每次访问nodes的一项数据
	// console.log(d)
	let size = 14
	switch(d.label){
		case 'Lifestyle': break;
		case 'Paper': size = 13;break;
		case 'Nation': size = 12;break;
		case 'PCA_Cancer': size=11;break;
		case 'Unit': size=10;break;
		case 'FirClass': size=9;break;
		case 'SecClass': size=8;break;
		case 'ThrClass': size=7;break;
		case 'Baseline': size=6;break;
		case 'Outcome': size=5;break;
		case 'Gene': size=4;break;
	}
	return size
}).attr("fill", function(d) {
	let index = 0
	switch(d.label){
		case 'Lifestyle': break;
		case 'Paper': index = 1;break;
		case 'Nation': index = 2;break;
		case 'PCA_Cancer': index=3;break;
		case 'Unit': index=4;break;
		case 'FirClass': index=5;break;
		case 'SecClass': index=6;break;
		case 'ThrClass': index=7;break;
		case 'Baseline': index=8;break;
		case 'Outcome': index=9;break;
		case 'Gene': index=10;break;
	}
	return colors[index]
}).attr("stroke", "none").attr("name", function(d) {
	return d.properties.name;
}).attr("id", d => d.id)
.call(d3.drag()
	.on("start", dragstarted)
	.on("drag", dragged)
	.on("end", dragended)
);

//显示所有的文本
//设置大小、填充颜色、名字、text()设置文本
//attr("text-anchor", "middle")设置文本居中
var text = svg.append("g").attr("class", "texts").selectAll("text").data(nodes).enter()
.append("text").attr("font-size", function(d) {
		return 12;
	}).attr("fill", function(d) {
			let index = 0
			switch(d.label){
				case 'Lifestyle': break;
				case 'Paper': index = 1;break;
				case 'Nation': index = 2;break;
				case 'PCA_Cancer': index=3;break;
				case 'Unit': index=4;break;
				case 'FirClass': index=5;break;
				case 'SecClass': index=6;break;
				case 'ThrClass': index=7;break;
				case 'Baseline': index=8;break;
				case 'Outcome': index=9;break;
				case 'Gene': index=10;break;
			}
			return colors[index];
	}).attr('name', function(d) {
		return d.properties.name;
	}).attr("text-anchor", "middle").text(function(d) {
		return d.properties.name;
	})
		
//圆增加title
node.append("title").text(d => d.properties.name)
//link.append("title").text('relation_type:')

//simulation中ticked数据初始化并生成图形
simulation.nodes(nodes).on("tick", ticked);
	
simulation.force("link")
		.links(links)
		.distance(d => {//每一边的长度
			let distance = 8
			switch(d.source.label){
				case 'Lifestyle': distance += 85;break;
				case 'Paper': distance += 77;break;
				case 'Nation': distance += 69;break;
				case 'PCA_Cancer': distance += 61;break;
				case 'Unit': distance += 53;break;
				case 'FirClass': distance += 45;break;
				case 'SecClass': distance += 37;break;
				case 'ThrClass': distance += 29;break;
				case 'Baseline': distance += 21;break;
				case 'Outcome': distance += 13;break;
				case 'Gene': distance += 5;break;
			}
			switch(d.target.label){
				case 'Lifestyle': distance += 85;break;
				case 'Paper': distance += 77;break;
				case 'Nation': distance += 69;break;
				case 'PCA_Cancer': distance += 61;break;
				case 'Unit': distance += 53;break;
				case 'FirClass': distance += 45;break;
				case 'SecClass': distance += 37;break;
				case 'ThrClass': distance += 29;break;
				case 'Baseline': distance += 21;break;
				case 'Outcome': distance += 13;break;
				case 'Gene': distance += 5;break;
			}
			return distance
		});
	
//ticked()函数确定link线的起始点x、y坐标 node确定中心点 文本通过translate平移变化
function ticked() {
		link
				.attr("x1", function(d) {
					return d.source.x;
				})
				.attr("y1", function(d) {
					return d.source.y;
				})
				.attr("x2", function(d) {
					return d.target.x;
				})
				.attr("y2", function(d) {
					return d.target.y;
				});

		node
				.attr("cx", function(d) {
						return d.x;
				})
				.attr("cy", function(d) {
						return d.y;
				});

		text.attr('transform', function(d) {
			var size = 14
			switch(d.label){
				case 'Lifestyle': break;
				case 'Paper': size = 13;break;
				case 'Nation': size = 12;break;
				case 'PCA_Cancer': size=11;break;
				case 'Unit': size=10;break;
				case 'FirClass': size=9;break;
				case 'SecClass': size=8;break;
				case 'ThrClass': size=7;break;
				case 'Baseline': size=6;break;
				case 'Outcome': size=5;break;
				case 'Gene': size=4;break;
			}
			return 'translate(' + (d.x - size / 2) + ',' + (d.y + size / 2) + ')';
		});
}

//拖动函数代码
var dragging = false;
//开始拖动并更新相应的点
function dragstarted(d) {
	if (!d3.event.active) simulation.alphaTarget(0.3).restart();
	d.fx = d.x;
	d.fy = d.y;
	//dragging = true;
}
//拖动进行中
function dragged(d) {
	d.fx = d3.event.x;
	d.fy = d3.event.y;
}
//拖动结束
function dragended(d) {
	if (!d3.event.active) simulation.alphaTarget(0);
	d.fx = null;
	d.fy = null;
	//dragging = false;
}

svgToCanvas = function (){
	saveSvgAsPng(document.getElementById("svg1"), "plot.png", {scale: 1, backgroundColor: '#9dadc1'});
};

//span点击事件
//$('.texts text').show();
$('.nodes circle').show();
// $('#mode span').click(function(event) {
	 // //span都设置为不激活状态
	 // $('#mode span').removeClass('active');
	 // //点击的span被激活
	 // $(this).addClass('active');
	 // //text隐藏 nodes显示
	 // if ($(this).text() == 'nodes') {
			 // $('.texts text').show();
			 // $('.nodes circle').show();
	 // } else {
			 // $('.texts text').show();
			 // $('.nodes circle').hide();
	 // }
// });
//设置鼠标选中节点显示，并循环设置与选中节点相关联的节点显示
//为svg1父元素下的.nodes circle元素绑定鼠标进入事件
$('#svg1').on('mouseenter', '.nodes circle', function(event) {
	// console.log(event)
	//通过变量dragging保证拖动鼠标时，其状态不受影响，从而改变图形
	//鼠标没有拖动才能处理事件
	if(!dragging) {
		//获取被选中元素的名字
		var id = $(this).attr("id");
		var name = $(this).attr("name");
		//设置#info h4样式的颜色为该节点的颜色，文本为该节点name
		//$(this).attr('fill')表示当前悬浮圆的填充色
		for(let item of nodes){
			if(item.id == id){
				$('#info h4').css('color', $(this).attr('fill')).text(item.label+': '+name);
			}
		}
		
		//每次点击添加属性前把上次显示的信息去除，否则会不断叠加
		$('#info p').remove();
		//遍历查找id对应的属性
		for(let item of nodes){
			if(item.id == id){
				for(var key in item.properties)
				//显示值及其字段名字
					$('#info').append('<p><span>' + key + '</span>' + item.properties[key] + '</p>');
			}
		}
		//选择#svg1 .nodes中所有的circle，再增加个class
		d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d) {
			//数据的id是否等于name,返回空
			if(d.properties.name == name) {
				return '';
			} 
			//当前节点返回空，否则其他节点循环判断是否被隐藏起来(CSS设置隐藏)
			else {
				//links链接的起始节点进行判断,如果其id等于name则显示这类节点
				//注意: graph=data
				for (var i = 0; i < links.length; i++) {
					//如果links的起点等于name，并且终点等于正在处理的则显示
					if (links[i]['source'].properties.name == name && links[i]['target'].id == d.id) {
							return '';
					}
					if (links[i]['target'].properties.name == name && links[i]['source'].id == d.id) {
							return '';
					}
				}
				return "inactive"; //前面CSS定义 .nodes circle.inactive
			}
		});
		//处理相邻的边line是否隐藏 注意 || 
		d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
				if (d.source.properties.name == name || d.target.properties.name == name) {
						return '';
				} else {
						return 'inactive';
				}
		});
	}
});
//鼠标移开还原原图，显示所有隐藏的点及边
$('#svg1').on('mouseleave', '.nodes circle', function(event) {
	d3.select('#svg1 .nodes').selectAll('circle').attr('class', '');
	d3.select('#svg1 .links').selectAll('line').attr('class', '');
});
//鼠标进入文本显示相邻节点及边
$('#svg1').on('mouseenter', '.texts text', function(event) {
	if (!dragging) {
		var name = $(this).attr('name');
		var id = $(this).attr('id');
		//var tag = $(this).attr('label');
		$('#info h4').css('color', $(this).attr('fill')).text(name);
		$('#info p').remove();
		//遍历查找id对应的属性
		for(let item of nodes){
			if(item.id == id){
				for(var key in item.properties){
					//显示值及其字段名字
					$('#info').append('<p><span>' + key + '</span>' + item.properties[key] + '</p>');
				}
			}
		}
		
		
		d3.select('#svg1 .texts').selectAll('text').attr('class', function(d) {
			if (d.properties.name == name) {
				return '';
			}

			for (var i = 0; i < links.length; i++) {
				if (links[i]['source'].properties.name == name && links[i]['target'].id == d.id) {
					return '';
				}
				if (links[i]['target'].properties.name == name && links[i]['source'].id == d.id) {
					return '';
				}
			}
			return 'inactive';
		});
		d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
			if (d.source.properties.name == name || d.target.properties.name == name) {
				return '';
			} else {
				return 'inactive';
			}
		});
	}
});
//鼠标移除文本还原相应节点及边
$('#svg1').on('mouseleave', '.texts text', function(event) {
	if (!dragging) {
		d3.select('#svg1 .texts').selectAll('text').attr('class', '');
		d3.select('#svg1 .links').selectAll('line').attr('class', '');
	}
});

//搜索框中输入内容则响应该事件
//keyup按键敲击响应event
$('#search input').keyup(function(event) {
	//如果Input值是空的显示所有的圆和线(没有进行筛选)
	if ($(this).val() == '') {
		d3.select('#svg1 .texts').selectAll('text').attr('class', '');
		d3.select('#svg1 .nodes').selectAll('circle').attr('class', '');
		d3.select('#svg1 .links').selectAll('line').attr('class', '');
	}
	//否则判断判断三个元素是否等于name值，等于则显示该值
	else {
		var name = $(this).val();
		//搜索所有的节点
		d3.select('#svg1 .nodes').selectAll('circle').attr('class', function(d) {
						//输入节点id的小写等于name则显示，否则隐藏
			if (d.properties.name.indexOf(name) >= 0) {
				return '';
			} else {
				//优化：与该搜索节点相关联的节点均显示
				//links链接的起始节点进行判断,如果其id等于name则显示这类节点
							//注意: graph=data
							for (var i = 0; i < links.length; i++) {
								//如果links的起点等于name，并且终点等于正在处理的则显示
								if ((links[i]['source'].properties.name.indexOf(name) >= 0) && 
									(links[i]['target'].id == d.id)) {
										return '';
								}
								//如果links的终点等于name，并且起点等于正在处理的则显示
								if ((links[i]['target'].properties.name.indexOf(name) >= 0) && 
									(links[i]['source'].id == d.id)) {
										return '';
								}
							}
							return 'inactive'; //隐藏
			}
		});
		//搜索texts
		d3.select('#svg1 .texts').selectAll('text').attr('class', function(d) {
					if (d.properties.name.indexOf(name) >= 0) {
							return '';
					} else {
								//优化：与该搜索节点相关联的节点均显示
								//links链接的起始节点进行判断,如果其id等于name则显示这类节点
								//注意: graph=data
								for (var i = 0; i < links.length; i++) {
										//如果links的起点等于name，并且终点等于正在处理的则显示
					if ((links[i]['source'].properties.name.indexOf(name) >= 0) && 
						(links[i]['target'].id == d.id)) {
						return '';
					}
					//如果links的终点等于name，并且起点等于正在处理的则显示
					if ((links[i]['target'].properties.name.indexOf(name) >= 0) && 
						(links[i]['source'].id == d.id)) {
						return '';
					}
				}
				return 'inactive';
			}
		});
		//搜索links
		//显示相的邻边 注意 || 
		//name=$(this).val()：名字为键盘输入的内容
		d3.select("#svg1 .links").selectAll('line').attr('class', function(d) {
			if ((d.source.properties.name.indexOf(name) >= 0) || 
				(d.target.properties.name.indexOf(name) >= 0) 
				) {
				return '';
			} else {
				return 'inactive'; //隐藏
			}
		});
	}
});