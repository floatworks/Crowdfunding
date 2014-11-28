var myScroll,
	pullDownEl, pullDownOffset,
	pullUpEl, pullUpOffset,
	generatedCount = 0;

/**
 * 下拉刷新 （自定义实现此方法）
 * myScroll.refresh();		// 数据加载完成后，调用界面更新方法
 */
function pullDownAction() {
		setTimeout(function() {
			location.reload(true);

			/*var content = "";
			for (var i = 1; i < 3; i++) {
				content = content + "<li>";
				content = content + "<a href=\"index2.html\">";
				content = content + "<img src=\"images/album-bb.jpg\" />";
				content = content + "<h2>";
				content = content + "下拉新增内容<br/>" + new Date();
				content = content + "</h2>";
				content = content + "<p>";
				content = content + "Broken Bells";
				content = content + "</p>";
				content = content + "</a>";
				content = content + "</li>";
			}
			$("#thelist").prepend(content).listview('refresh');



			myScroll.refresh(); */ //数据加载完成后，调用界面更新方法   Remember to refresh when contents are loaded (ie: on ajax completion)
		}, 1000);
}
		/**
		 * 滚动翻页 （自定义实现此方法）
		 * myScroll.refresh();		// 数据加载完成后，调用界面更新方法
		 */
		function pullUpAction() {
			setTimeout(function() { // <-- Simulate network congestion, remove setTimeout from production!
				/*		
				var el, li, i;
				el = document.getElementById('thelist');

				for (i=0; i<3; i++) {
					li = document.createElement('li');
					li.innerText = 'Generated row ' + (++generatedCount);
					el.appendChild(li, el.childNodes[0]);
				}
				*/
				generatedCount += 1;
				$.ajax({
					url: '/w/prolist/' + generatedCount,
					type: 'GET',
					dataType: 'json',
					success: function(result) {
						if(result.status == 1){
							var content = "";
							projects = result.projects;
							for (var index in projects){
								if(projects[index].type == 'stock'){
									content += "<li data-icon='false'>";
									content += "<a href='#pro_detail'>";
									content += "<img src='/media/"+projects[index].image+"'/>";
									content += "<h3>"+projects[index].title+"</h3>";
									if(projects[index].progress > 50)
										content += "<p class='progressbar more' data='"+projects[index].progress+"'>";
									else
										content += "<p class='progressbar less' data='"+projects[index].progress+"'>";
									content += "<span class='progress'> <b class='bar' style='width: "+projects[index].progress+"%;'></b></span><span class='num'> "+projects[index].progress+"%</span></p>";
									content += "<p class='cbrief'>";
									content += "<span class='ui-alt-icon ui-icon-location ui-btn-icon-left'>"+projects[index].province+"</span>"
									content += "<span class='hl1'>"+projects[index].industry+"</span>"
									content += "<span class='hl2'>"+projects[index].com_type+"</span></p>"
									content += "<p class='cpopular'><span>";
									content += "热度 <em class='hl1'>"+projects[index].view_count+"</em></span>";
									content += "/ ";
									content += "<span>关注 <em class='hl1'>"+projects[index].like_count+"</em></span>";
									content += "/ ";
									content += "<span>认购 <em class='hl1'>"+projects[index].invest_count+"</em></span></p>";
									content += "<p class='ui-li-aside'>"+projects[index].pro_type+"</p></a>";
									content += "<p class='ui-li-bottom'><span>当前融资:<em>￥"+projects[index].current_price+"</em></span>";
									content += "<span>融资总额:<em>￥"+projects[index].total_price+"</em></span>";
									content += "<span>认购起点:<em>￥"+projects[index].min_price+"</em></span></p></li>";
								}else if(projects[index].type == 'bond'){
									content += "<li data-icon='false'>";
									content += "<a href='#pro_detail'>";
									content += "<img src='/media/"+projects[index].image+"'/>";
									content += "<h3>"+projects[index].title+"</h3>";
									if(projects[index].progress > 50)
										content += "<p class='progressbar more' data='"+projects[index].progress+"'>";
									else
										content += "<p class='progressbar less' data='"+projects[index].progress+"'>";
									content += "<span class='progress'> <b class='bar' style='width: "+projects[index].progress+"%;'></b></span><span class='num'> "+projects[index].progress+"%</span></p>";
									content += "<p>"+projects[index].com_name+"</p>";
									content += "<p>"+projects[index].brief+"</p>";
									content += "<p class='ui-li-aside'>"+projects[index].pro_type+"</p></a>";
									content += "<p class='ui-li-bottom'><span>年化利率:<em class='hl1'>"+projects[index].scale+"%</em></span>";
									content += "<span>融资总额:<em class='hl1'>￥"+projects[index].current_price+"</em></span>";
									content += "<span>授信额度:<em class='hl1'>￥"+projects[index].min_price+"</em></span></p></li>"
								}
							}

							$("#thelist").append(content).listview('refresh');
							myScroll.refresh(); // 数据加载完成后，调用界面更新方法 Remember to refresh when contents are loaded (ie: on ajax completion)
						}else if(result.status == 0){
							myScroll.refresh();
							pullUpEl = document.getElementById('pullUp');
							pullUpEl.querySelector('.pullUpLabel').innerHTML = '没有更多数据了';
						}
					},
					error: function() {
					}
				});

				// var content = "";
				// for (var i = 1; i < 3; i++) {
				// 	content = content + "<li>";
				// 	content = content + "<a href=\"#\">";
				// 	content = content + "<img src=\"images/album-bb.jpg\" />";
				// 	content = content + "<h2>";
				// 	content = content + "下拉新增内容<br/>" + new Date();
				// 	content = content + "</h2>";
				// 	content = content + "<p>";
				// 	content = content + "Broken Bells";
				// 	content = content + "</p>";
				// 	content = content + "</a>";
				// 	content = content + "</li>";
				// }
				// $("#thelist").append(content).listview('refresh');

				
			}, 1000); // <-- Simulate network congestion, remove setTimeout from production!
		}

		/**
		 * 初始化iScroll控件
		 */
		function loaded() {
			//清除所占的内存空间
			if (myScroll != null) {
				myScroll.destroy();
			}

			pullDownEl = document.getElementById('pullDown');
			pullDownOffset = pullDownEl.offsetHeight;
			pullUpEl = document.getElementById('pullUp');
			pullUpOffset = pullUpEl.offsetHeight;

			myScroll = new iScroll('wrapper', {
				useTransition: true, //默认为true
				//useTransition: false, 
				topOffset: pullDownOffset,
				onRefresh: function() {
					if (pullDownEl.className.match('loading')) {
						pullDownEl.className = '';
						pullDownEl.querySelector('.pullDownLabel').innerHTML = '下拉刷新...';
					} else if (pullUpEl.className.match('loading')) {
						pullUpEl.className = '';
						pullUpEl.querySelector('.pullUpLabel').innerHTML = '上拉加载更多...';
					}
				},
				onScrollMove: function() {
					if (this.y > 5 && !pullDownEl.className.match('flip')) {
						pullDownEl.className = 'flip';
						pullDownEl.querySelector('.pullDownLabel').innerHTML = '松开更新...';
						this.minScrollY = 0;
					} else if (this.y < 5 && pullDownEl.className.match('flip')) {
						pullDownEl.className = '';
						pullDownEl.querySelector('.pullDownLabel').innerHTML = '下拉刷新...';
						this.minScrollY = -pullDownOffset;
					} else if (this.y < (this.maxScrollY - 5) && !pullUpEl.className.match('flip')) {
						pullUpEl.className = 'flip';
						pullUpEl.querySelector('.pullUpLabel').innerHTML = '松开更新...';
						this.maxScrollY = this.maxScrollY;
					} else if (this.y > (this.maxScrollY + 5) && pullUpEl.className.match('flip')) {
						pullUpEl.className = '';
						pullUpEl.querySelector('.pullUpLabel').innerHTML = '上拉加载更多...';
						this.maxScrollY = pullUpOffset;
					}
				},
				onScrollEnd: function() {
					if (pullDownEl.className.match('flip')) {
						pullDownEl.className = 'loading';
						pullDownEl.querySelector('.pullDownLabel').innerHTML = '正在加载...';
						pullDownAction(); // Execute custom function (ajax call?)
					} else if (pullUpEl.className.match('flip')) {
						pullUpEl.className = 'loading';
						pullUpEl.querySelector('.pullUpLabel').innerHTML = '正在加载...';
						pullUpAction(); // Execute custom function (ajax call?)
					}
				}
			});

			document.getElementById('wrapper').style.left = '0';
		}

		//初始化绑定iScroll控件 
		//document.addEventListener('touchmove', function(e) {
		//	e.preventDefault();
		//}, false);

		//document.addEventListener('DOMContentLoaded', function () { setTimeout(loaded, 200); }, false);
		document.addEventListener('DOMContentLoaded', loaded, false);


$(document).ready(function () {
	$("#t_itemsList").bind("click",function(){
		$("#itemsList").show();
		$("#itemsRecommend").hide();
	});
	$("#t_itemsRecommend").bind("click",function(){
		$("#itemsRecommend").show();
		$("#itemsList").hide();
	});
});
