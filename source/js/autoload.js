OML2D.loadOml2d({
	menus: {
		items: (defaultItems) =>{
			return [{
				id: 'home',
				icon: 'fa fa-house',
				title: '我的个人主页',
				onClick: () =>window.open('https://www.sinzmise.top/')
			},
			defaultItems[0], defaultItems[2], defaultItems[3]]
		}
	},
	mobileDisplay: false,
	models: [{
		"path": "https://files.blog.sinzmise.top/live2d/dujiaoshou_6/dujiaoshou_6.model3.json",
		"mobilePosition": [ - 10, 23],
		"mobileScale": 0.1,
		"mobileStageStyle": {
			"width": 180,
			"height": 166
		},
		"motionPreloadStrategy": "IDLE",
		"position": [ - 120, -30],
		"scale": 0.06,
		"stageStyle": {
			"width": 250,
			"height": 400
		}
	},
	{
		"path": "https://files.blog.sinzmise.top/live2d/dujiaoshou_4/dujiaoshou_4.model3.json",
		"scale": 0.06,
		"position": [ - 50, -25],
		"stageStyle": {
			"width": 250,
			"height": 300
		},
		"mobileScale": 0.08,
		"mobilePosition": [0, 0],
		"mobileStageStyle": {
			"width": 180
		}
	}],
	parentElement: document.body,
	primaryColor: "var(--theme-color)",
	sayHello: false,
	tips: {
		style: {
			"width": 230,
			"height": 120,
			"left": "calc(50% + 6px)",
			"top": "-100px"
		},
		mobileStyle: {
			"width": 180,
			"height": 80,
			"left": "calc(50% - 30px)",
			"top": "-100px"
		},
		idleTips: {
			interval: 15000,
			message: function() {
				return axios.get('https://v1.hitokoto.cn?c=i').then(function(response) {
					return response.data.hitokoto;
				}).
				catch(function(error) {
					console.error(error);
				});
			}
		}
	}
  });