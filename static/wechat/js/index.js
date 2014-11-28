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



		myScroll.refresh(); *///数据加载完成后，调用界面更新方法   Remember to refresh when contents are loaded (ie: on ajax completion)
	}, 1000); 

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

		var content = "";
		for (var i = 1; i < 3; i++) {
			content = content + "<li>";
			content = content + "<a href=\"#\">";
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
		$("#thelist").append(content).listview('refresh');

		myScroll.refresh(); // 数据加载完成后，调用界面更新方法 Remember to refresh when contents are loaded (ie: on ajax completion)
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
document.addEventListener('touchmove', function(e) {
	e.preventDefault();
}, false);

//document.addEventListener('DOMContentLoaded', function () { setTimeout(loaded, 200); }, false);
document.addEventListener('DOMContentLoaded', loaded, false);