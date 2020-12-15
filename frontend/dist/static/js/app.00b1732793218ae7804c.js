webpackJsonp([31],[function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0}),n.default={name:"app",components:{}}},,function(e,n){e.exports=Vue},function(e,n,t){"use strict";function o(e){return e&&e.__esModule?e:{default:e}}var i=t(4),r=o(i),c=t(8),u=o(c),a=t(12),p=o(a);Vue.config.productionTip=!1,Vue.use(ELEMENT),Vue.use(VueRouter),Vue.use(Vuex);var l=new VueRouter({routes:p.default});l.beforeEach(function(e,n,t){"/login"===e.path&&sessionStorage.removeItem("token");var o=sessionStorage.getItem("token");"undefined"===o&&(o=""),o||"/register"!==e.path?o||"/login"===e.path?t():(console.log(e.path),t({path:"/login",query:{url:e.path}})):t(),"/"===e.path&&t({path:"/projectList"})});var d={};d.install=function(e,n){e.directive("highlightA",{inserted:function(e){for(var n=e.querySelectorAll("pre code"),t=0;t<n.length;t++){console.log(n),console.log(n[t]);var o=n[t];console.log(o),hljs.highlightBlock(o)}}}),e.directive("highlightB",{componentUpdated:function(e){for(var n=e.querySelectorAll("pre code"),t=0;t<n.length;t++){var o=n[t];hljs.highlightBlock(o)}}})},Vue.use(d),new Vue({router:l,store:u.default,render:function(e){return e(r.default)}}).$mount("#app")},function(e,n,t){"use strict";function o(e){t(5)}Object.defineProperty(n,"__esModule",{value:!0});var i=t(0),r=t.n(i);for(var c in i)"default"!==c&&function(e){t.d(n,e,function(){return i[e]})}(c);var u=t(7),a=t(1),p=o,l=a(r.a,u.a,!1,p,null,null);n.default=l.exports},function(e,n){},,function(e,n,t){"use strict";var o=function(){var e=this,n=e.$createElement,t=e._self._c||n;return t("div",{attrs:{id:"app"}},[t("transition",{attrs:{name:"fade",mode:"out-in"}},[t("router-view")],1)],1)},i=[],r={render:o,staticRenderFns:i};n.a=r},function(e,n,t){"use strict";function o(e){if(e&&e.__esModule)return e;var n={};if(null!=e)for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&(n[t]=e[t]);return n.default=e,n}function i(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(n,"__esModule",{value:!0});var r=t(2),c=i(r),u=t(9),a=i(u),p=t(10),l=o(p),d=t(11),s=o(d);c.default.use(a.default);var f={count:10},h={INCREMENT:function(e){e.count++},DECREMENT:function(e){e.count--}};n.default=new a.default.Store({actions:l,getters:s,state:f,mutations:h})},function(e,n){e.exports=Vuex},function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0});n.increment=function(e){(0,e.commit)("INCREMENT")},n.decrement=function(e){(0,e.commit)("DECREMENT")}},function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0});n.getCount=function(e){return e.count}},function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var o=function(){return t.e(29).then(t.bind(null,15))},i=function(){return t.e(12).then(t.bind(null,16))},r=function(){return t.e(28).then(t.bind(null,17))},c=function(){return t.e(30).then(t.bind(null,18))},u=function(){return t.e(9).then(t.bind(null,19))},a=function(){return t.e(11).then(t.bind(null,20))},p=function(){return t.e(8).then(t.bind(null,21))},l=function(){return t.e(27).then(t.bind(null,22))},d=function(){return t.e(10).then(t.bind(null,23))},s=function(){return t.e(24).then(t.bind(null,24))},f=function(){return t.e(18).then(t.bind(null,25))},h=function(){return t.e(17).then(t.bind(null,26))},m=function(){return t.e(4).then(t.bind(null,27))},j=function(){return t.e(6).then(t.bind(null,28))},_=function(){return t.e(15).then(t.bind(null,29))},b=function(){return t.e(20).then(t.bind(null,30))},v=function(){return t.e(7).then(t.bind(null,31))},g=function(){return t.e(5).then(t.bind(null,32))},E=function(){return t.e(23).then(t.bind(null,33))},y=function(){return t.e(16).then(t.bind(null,34))},M=function(){return t.e(2).then(t.bind(null,35))},C=function(){return t.e(1).then(t.bind(null,36))},V=function(){return t.e(3).then(t.bind(null,37))},A=function(){return t.e(14).then(t.bind(null,38))},L=function(){return t.e(13).then(t.bind(null,39))},P=function(){return t.e(22).then(t.bind(null,40))},R=function(){return t.e(25).then(t.bind(null,41))},T=function(){return t.e(26).then(t.bind(null,42))},O=function(){return t.e(21).then(t.bind(null,43))},H=function(){return t.e(0).then(t.bind(null,44))},I=function(){return t.e(19).then(t.bind(null,45))},N=[{path:"/login",component:i,name:"",hidden:!0,projectHidden:!0},{path:"/register",component:I,name:"",hidden:!1,projectHidden:!0},{path:"/404",component:o,name:"",hidden:!0,projectHidden:!0},{path:"/",component:r,name:"",projectHidden:!0,children:[{path:"/projectList",component:u,iconCls:"el-icon-message",name:"项目列表"},{path:"/lyzdEnvironmentList",component:a,iconCls:"el-icon-message",name:"环境列表"},{path:"/lyzdInterfaceList",component:p,iconCls:"el-icon-message",name:"接口维护"},{path:"/about",component:c,iconCls:"fa fa-address-card",name:"关于我们"}]},{path:"*",hidden:!0,projectHidden:!0,redirect:{path:"/404"}},{path:"/project/project=:project_id",component:l,name:"项目",hidden:!0,children:[{path:"/ProjectTitle/project=:project_id",component:O,name:"项目概况",leaf:!0},{path:"/GlobalHost/project=:project_id",component:d,name:"Host配置",leaf:!0},{path:"/api/project=:project_id",component:s,name:"API接口",leaf:!0,child:!0,children:[{path:"/apiList/project=:project_id",component:f,name:"接口列表"},{path:"/apiList/project=:project_id/first=:firstGroup",component:h,name:"分组接口列表"},{path:"/fastTest/project=:project_id",component:m,name:"快速测试"},{path:"/addApi/project=:project_id",component:j,name:"新增接口"},{path:"/detail/project=:project_id/api=:api_id",component:_,name:"接口",children:[{path:"/apiInfo/project=:project_id/api=:api_id",component:b,name:"基础信息"},{path:"/testApi/project=:project_id/api=:api_id",component:v,name:"测试"},{path:"/apiDynamic/project=:project_id/api=:api_id",component:E,name:"历史"}]},{path:"/updateApi/project=:project_id/api=:api_id",component:g,name:"修改"}]},{path:"/automationTest/project=:project_id",component:y,name:"自动化测试",leaf:!0,child:!0,children:[{path:"/caseList/project=:project_id",component:M,name:"用例列表"},{path:"/caseList/project=:project_id/first=:firstGroup",component:C,name:"分组用例列表"},{path:"/caseApiList/project=:project_id/case=:case_id",component:V,name:"用例接口列表"},{path:"/addCaseApi/project=:project_id/case=:case_id",component:A,name:"添加新接口"},{path:"/updateCaseApi/project=:project_id/case=:case_id/api=:api_id",component:L,name:"修改接口"},{path:"/testReport/project=:project_id",component:P,name:"测试报告"}]},{path:"/projectMember/project=:project_id",component:R,name:"成员管理",leaf:!0},{path:"/projectDynamic/project=:project_id",component:T,name:"项目动态",leaf:!0},{path:"/projectReport/project=:project_id",component:H,name:"自动化测试报告",leaf:!0}]},{path:"/project/project=:project_id",component:a,name:"高靖宇测试环境",hidden:!0}];n.default=N}],[3]);