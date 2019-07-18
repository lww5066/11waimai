//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        //已经初始化的categories
        categories: [],
        //分类点击切换视图id
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        banners: [],
        //添加分页功能的页数 默认为1
        page:1,
        // 后端传递给前端用来做终止请求的标识
        ismore:1,
        // 考虑到手机端网络不稳定 当上一次请求没有响应时不能发起下一次请求
        isloading:false

    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });

        that.setData({
            banners:
                //轮播假数据
                [
    //             {
    //                 "id": 1,
    //                 "pic_url": "/images/food.jpg"
    //             },
    //             {
    //                 "id": 2,
    //                 "pic_url": "/images/food.jpg"
    //             },
    //             {
    //                 "id": 3,
    //                 "pic_url": "/images/food.jpg"
    //             }
    //         ],
    //         categories: [
    //             {id: 0, name: "全部"},
    //             {id: 1, name: "川菜"},
    //             {id: 2, name: "东北菜"},
    //         ],
    //         //详情列表假数据
    //         activeCategoryId: 0,
	// 		goods: [
	// 		                {
	// 		                    "id": 1,
	// 		                    "name": "小鸡炖蘑菇-1",
	// 		                    "min_price": "15.00",
	// 		                    "price": "15.00",
	// 		                    "pic_url": "/images/food.jpg"
	// 		                },
	// 		                {
	// 		                    "id": 2,
	// 		                    "name": "小鸡炖蘑菇-1",
	// 		                    "min_price": "15.00",
	// 		                    "price": "15.00",
	// 		                    "pic_url": "/images/food.jpg"
	// 		                },
	// 		                {
	// 		                    "id": 3,
	// 		                    "name": "小鸡炖蘑菇-1",
	// 		                    "min_price": "15.00",
	// 		                    "price": "15.00",
	// 		                    "pic_url": "/images/food.jpg"
	// 		                },
	// 		                {
	// 		                    "id": 4,
	// 		                    "name": "小鸡炖蘑菇-1",
	// 		                    "min_price": "15.00",
	// 		                    "price": "15.00",
	// 		                    "pic_url": "/images/food.jpg"
	// 		                }
    //
			 ],
            // loadingMoreHidden: false
        });
        //调用轮播图与分类！！！！！！！
        this.getBannersAndCategory()
        //调用方法！！！！！！！
        this.getFoods()
    },
    // //(e)代表点击的视图
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
            // 'id':e.id,
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
	 toSearch:function( e ){
	        this.setData({
	            p:1,
	            goods:[],
	            loadingMoreHidden:true
	        });
	        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },
    //onReachBottom 页面上拉触底事件的处理函数
    onReachBottom:function(){
        console.log('滚动到底部要加载数据')
        //加载到底部再次调用方法获取数据!!!
        var that=this
        if (that.data.isloading==false){
            if (that.data.ismore!=0){
                //加参数语法记死了
                that.setData({
                    page:that.data.page+1
                })
                that.getFoods()
            }
        }

    },
    //点击下划线切换视图功能 添加监听事件
    // //(e)代表点击的视图
    // 打印e中的参数target有id表示分类id
    cateclick:function(e){
        var that=this
        console.log(e.target.id,'我是点击的监听事件 ')
        that.setData({
            activeCategoryId:e.target.id,
            //点击分类时应该清空之前的数据恢复原始页码 否则会出现缓存造成数据错误
            goods:[],
            page:1
        })
        // 点击分类的时候做筛选需要重新调用方法做查询！！！
        that.getFoods()
    },
    //构造请求传递后台的json数据做前端展示
    //返回轮播图与分类
    getBannersAndCategory:function () {
        //声明
        var that=this
        wx.request({
                        // url: 'http://127.0.0.1:5000/api/v1/food/search',
                        url: app.buildUrl('/v1/food/search'),
                        method: 'GET',
                        header: app.getRequestHeader(),
                        success(res) {
                            console.log(res.data)
                             if (res.data.code==-1){
                                app.alert({
                                    'content':res.data.msg
                                })
                                return
                            }
                            // if (res.data.code == 1) {
                                that.setData({
                                    banners:res.data.data.banners,
                                    categories:res.data.data.categories
                                })
                            }
                        // }
                    })
                },
    //返回所有商品
    getFoods:function () {
        //声明
        var that=this
        that.setData({
            'isloading':true
        })
            wx.request({
                        // url: 'http://127.0.0.1:5000/api/v1/food/all',
                        url: app.buildUrl('/v1/food/all'),
                        method: 'GET',
                        header: app.getRequestHeader(),
                        //获取点击分类id 分页页码
                        data:{
                            'cid':that.data.activeCategoryId,
                            'page':that.data.page
                        },
                        // ?cid=1传递分类id作为查询条件 以参数的形式拼接到url后作为请求url
                        //Request URL: http://127.0.0.1:5000/api/v1/food/all?cid=1
                        success(res) {
                            console.log(res.data)
                             if (res.data.code==-1){
                                app.alert({
                                    'content':res.data.msg
                                })
                                return
                            }
                            // if (res.data.code == 1) {
                                //提取后台返回的JSON串中的数据作展示
                                that.setData({
                                    // 'goods':res.data.data.goods,
                                    'goods':that.data.goods.concat(res.data.data.goods),
                                    //后端传递给前端用来做终止请求的标识
                                    //res表示？？？？
                                    'ismore':res.data.data.ismore,
                                    'isloading':false
                                })
                                //当没有数据返回时 显示数据加载完毕的提示
                                if (that.data.ismore==0){
                                    that.setData({
                                        loadingMoreHidden:false
                                    })
                                }
                            }
                        // }
                    })
                }
});

