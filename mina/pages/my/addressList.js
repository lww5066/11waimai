//获取应用实例
var app = getApp();
Page({
    data: {
        addressList: []
    },
    selectTap: function (e) {
        //从商品详情下单选择地址之后返回
        wx.navigateBack({});
    },
    addessSet: function (e) {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        })
    },
    onShow: function () {
        var that = this;
        that.getAddressList()
        // that.setData({
            // addressList: [
            //     {
            //         id:1,
            //         name: "test1",
            //         mobile: "12345678901",
            //         detail: "上海市浦东新区XX",
            //         isDefault: 1
            //     },
            //     {
            //         id: 2,
            //         name: "test2",
            //         mobile: "12345678901",
            //         detail: "上海市浦东新区XX"
            //     }
            // ]
        // });
    },
    //展示收货地址
    getAddressList: function () {
        var that = this
        wx.request({
            url: app.buildUrl('/v1/address/list'),
            method: 'GET',
            header: app.getRequestHeader(),
            success: function (res) {
                var data = res.data
                if (data.code != 1) {
                    app.alert({'content': data.msg})
                    return;
                }
                that.setData({
                    addressList: data.data.addressList
                })
            }
        })
    }
});

