//获取应用实例
var app = getApp();

Page({
    data: {
        // 声明ids
        ids:[],
        goods_list:[],
        address_id:0,
        note:'',
        // goods_list: [
        //     {
        //         id:22,
        //         name: "小鸡炖蘑菇",
        //         price: "85.00",
        //         pic_url: "/images/food.jpg",
        //         number: 1,
        //     },
        //     {
        //         id:22,
        //         name: "小鸡炖蘑菇",
        //         price: "85.00",
        //         pic_url: "/images/food.jpg",
        //         number: 1,
        //     }
        // ],
        // default_address: {
        //     name: "编程浪子",
        //     mobile: "12345678901",
        //     detail: "上海市浦东新区XX",
        // },
        // yun_price: "1.00",
        // pay_price: "85.00",
        // total_price: "86.00",
        params: null,
    },
    onShow: function () {
        var that = this;
        that.getOrderList()
    },
    onLoad: function (e) {
        // 接收购物车去结算按钮传递过来的food_ids
        // ids=e.ids
        var that = this;
        that.setData({
            ids:JSON.parse(e.ids)
        })
        that.getOrderInfo()

    },
    // 生成我的订单
    createOrder: function (e) {
        // wx.showLoading();
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/create'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),
                'address_id':that.data.address_id,
                'note':that.data.note
            },
            header: app.getRequestHeader(),
            success(res) {
                console.log(res.data);
                if (res.data.code != 1) {
                    //     app.alert({'content': res.data.msg});
                    //     return
                }

            }
        })
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },
    //我的订单
    getOrderList:function () {
        var that=this
        wx.request({
            url:app.buildUrl('/v1/cart/list'),
            method:'GET',
            header:app.getRequestHeader(),
            success(res){
                if (res.data.code!=1) {
                    app.alert({
                        'content': res.data.msg
                    })
                    return
                }
                that.setData({
                    list:res.data.data.list,
                    totalPrice:res.data.data.totalPrice,
                    saveHidden: true,
                    allSelect: true,
                    noSelect: false,
                })
                    that.setPageData( this.getSaveHide(), this.totalPrice(), this.allSelect(), this.noSelect(), this.data.list)
                }
        })

    },
    // 去结算页面
    getOrderInfo: function () {
        var that = this
        wx.request({
            url: app.buildUrl('/v1/order/commit'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),//购物车
                'address_id':that.data.address_id,
                // 取到备注的内容
                'note':that.data.note
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    app.alert({'content': res.data.msg})
                    return
                }
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address: res.data.data.default_address,
                    address_id: res.data.data.default_address.id,
                    yun_price: res.data.data.yun_price,
                    pay_price: res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                })
            }
        })
    }
});
