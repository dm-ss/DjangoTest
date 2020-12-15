const NotFound = () => import('./views/common/404.vue');
const Login = () => import('./views/common/Login.vue');
const Home = () => import('./views/Home.vue');
const About = () => import('./views/About.vue');
const projectList = () => import('./views/Projectlist.vue');


//高靖宇添加 龙盈智达list测试
//const ProjectReport = () => import('./views/project/ProjectReport.vue');
const lyzdEnvironmentList = () => import('./views/lyzd_environment.vue');
//lyzdInterfaceList

//高靖宇添加 龙盈智达list测试
const lyzdInterfaceList = () => import('./views/lyzd_interface.vue');
const ProjectInfo = () => import('./views/Project.vue');
const globalHost = () => import('./views/project/global/Globalhost.vue');
const API = () => import('./views/project/api/API.vue');
const ApiList = () => import('./views/project/api/ApiList.vue');
const ApiListGroup = () => import('./views/project/api/ApiListGroup.vue');
const FestTest = () => import('./views/project/api/FestTest.vue');
const addApi = () => import('./views/project/api/Addapi.vue');
const detail = () => import('./views/project/api/updateApi/ApiForm.vue');
const ApiInfo = () => import('./views/project/api/updateApi/ApiInfo.vue');
const testApi = () => import('./views/project/api/updateApi/TestApi.vue');
const UpdateApi = () => import('./views/project/api/updateApi/UpdateApi.vue');
const ApiDynamic = () => import('./views/project/api/updateApi/ApiDynamic.vue');
const AutomationTest = () => import('./views/project/automation/AutomationTest.vue');
const CaseList = () => import('./views/project/automation/CaseList.vue');
const CaseListGroup = () => import('./views/project/automation/CaseListGroup.vue');
const CaseApiList = () => import('./views/project/automation/CaseApiList.vue');
const AddCaseApi = () => import('./views/project/automation/AddCaseApi.vue');
const UpdateCaseApi = () => import('./views/project/automation/UpdateCaseApi.vue');
const TestReport = () => import('./views/project/automation/TestReport.vue');
const ProjectMember = () => import('./views/project/ProjectMember.vue');
const ProjectDynamic = () => import('./views/project/ProjectDynamic.vue');
const ProjectTitle = () => import('./views/project/projectTitle/ProjectTitle.vue');
const ProjectReport = () => import('./views/project/ProjectReport.vue');
const register = () => import('./views/register.vue')

let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true,
        projectHidden: true
    },
    {
        path: '/register',
        component: register,
        name: '',
        hidden: false,
        projectHidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true,
        projectHidden: true
    },
    {
        path: '/',
        component: Home,
        name: '',
        projectHidden: true,
        children: [
            {path: '/projectList', component: projectList, iconCls: 'el-icon-message', name: '项目列表'},
            {path: '/lyzdEnvironmentList', component: lyzdEnvironmentList, iconCls: 'el-icon-message', name: '环境列表'},
            {path: '/lyzdInterfaceList', component: lyzdInterfaceList, iconCls: 'el-icon-message', name: '接口维护'},
            // {path: '/lyzdCaseList', component: lyzdCaseList, iconCls: 'el-icon-message', name: '用例维护'},
            // {path: '/lyzdCaseList2', component: lyzdCaseList2, iconCls: 'el-icon-message', name: '接口测试执行'},
            // {path: '/lyzdCaseList3', component: lyzdCaseList3, iconCls: 'el-icon-message', name: '批量接口执行'},
            // {path: '/lyzdCaseList4', component: lyzdCaseList4, iconCls: 'el-icon-message', name: '测试执行结果查询'},
            // {path: '/lyzdCaseList5', component: lyzdCaseList5, iconCls: 'el-icon-message', name: '测试执行详情查询'},
            // {path: '/lyzdCaseList6', component: lyzdCaseList6, iconCls: 'el-icon-message', name: '系统管理'},
            //  { path: '/robot', component: robot, iconCls:'fa fa-id-card-o', name: '消息机器人', meta: { keepAlive: true }},
            {path: '/about', component: About, iconCls: 'fa fa-address-card', name: '关于我们'},
        ]
    },
    {
        path: '*',
        hidden: true,
        projectHidden: true,
        redirect: {path: '/404'}
    },
    {
        path: '/project/project=:project_id',
        component: ProjectInfo,
        name: '项目',
        hidden: true,
        children: [
            {path: '/ProjectTitle/project=:project_id', component: ProjectTitle, name: '项目概况', leaf: true},
            {path: '/GlobalHost/project=:project_id', component: globalHost, name: 'Host配置', leaf: true},
            {
                path: '/api/project=:project_id',
                component: API,
                name: 'API接口',
                leaf: true,
                child: true,
                children: [
                    {path: '/apiList/project=:project_id', component: ApiList, name: '接口列表'},
                    {path: '/apiList/project=:project_id/first=:firstGroup', component: ApiListGroup, name: '分组接口列表'},
                    {path: '/fastTest/project=:project_id', component: FestTest, name: '快速测试'},
                    {path: '/addApi/project=:project_id', component: addApi, name: '新增接口'},
                    {
                        path: '/detail/project=:project_id/api=:api_id',
                        component: detail,
                        name: '接口',
                        children: [
                            {path: '/apiInfo/project=:project_id/api=:api_id', component: ApiInfo, name: '基础信息'},
                            {path: '/testApi/project=:project_id/api=:api_id', component: testApi, name: '测试'},
                            {path: '/apiDynamic/project=:project_id/api=:api_id', component: ApiDynamic, name: '历史'},
                        ]
                    },
                    {path: '/updateApi/project=:project_id/api=:api_id', component: UpdateApi, name: '修改'},
                ]
            },
            {
                path: '/automationTest/project=:project_id',
                component: AutomationTest,
                name: '自动化测试',
                leaf: true,
                child: true,
                children: [
                    {path: '/caseList/project=:project_id', component: CaseList, name: '用例列表'},
                    {path: '/caseList/project=:project_id/first=:firstGroup', component: CaseListGroup, name: '分组用例列表'},
                    {path: '/caseApiList/project=:project_id/case=:case_id', component: CaseApiList, name: '用例接口列表'},
                    {path: '/addCaseApi/project=:project_id/case=:case_id', component: AddCaseApi, name: '添加新接口'},
                    {
                        path: '/updateCaseApi/project=:project_id/case=:case_id/api=:api_id',
                        component: UpdateCaseApi,
                        name: '修改接口'
                    },
                    {path: '/testReport/project=:project_id', component: TestReport, name: '测试报告'},
                ]
            },
            {path: '/projectMember/project=:project_id', component: ProjectMember, name: '成员管理', leaf: true},
            {path: '/projectDynamic/project=:project_id', component: ProjectDynamic, name: '项目动态', leaf: true},
            {path: '/projectReport/project=:project_id', component: ProjectReport, name: '自动化测试报告', leaf: true},
        ]
    },
    {
        path: '/project/project=:project_id',
        component: lyzdEnvironmentList,
        name: '高靖宇测试环境',
        hidden: true,
        // children: [
        //     {   path: '/ProjectTitle/project=:project_id', component: ProjectTitle, name: '项目概况', leaf: true},
        //     {   path: '/GlobalHost/project=:project_id', component: globalHost, name: 'Host配置', leaf: true},
        //     {   path: '/api/project=:project_id',
        //             component: API,
        //             name: 'API接口',
        //             leaf: true,
        //             child: true,
        //             children: [
        //                 {   path: '/apiList/project=:project_id', component: ApiList, name: '接口列表'},
        //                 {   path: '/apiList/project=:project_id/first=:firstGroup', component: ApiListGroup, name: '分组接口列表'},
        //                 {   path: '/fastTest/project=:project_id', component: FestTest, name: '快速测试'},
        //                 {   path: '/addApi/project=:project_id', component: addApi, name: '新增接口'},
        //                 {   path: '/detail/project=:project_id/api=:api_id',
        //                     component: detail,
        //                     name: '接口',
        //                     children: [
        //                         { path: '/apiInfo/project=:project_id/api=:api_id', component: ApiInfo, name: '基础信息'},
        //                         { path: '/testApi/project=:project_id/api=:api_id', component: testApi, name: '测试'},
        //                         { path: '/apiDynamic/project=:project_id/api=:api_id', component: ApiDynamic, name: '历史'},
        //                     ]
        //                 },
        //                 { path: '/updateApi/project=:project_id/api=:api_id', component: UpdateApi, name: '修改'},
        //             ]},
        //     {   path: '/automationTest/project=:project_id',
        //             component: AutomationTest,
        //             name: '自动化测试',
        //             leaf: true,
        //             child: true,
        //             children: [
        //                 {   path: '/caseList/project=:project_id', component: CaseList, name: '用例列表'},
        //                 {   path: '/caseList/project=:project_id/first=:firstGroup', component: CaseListGroup, name: '分组用例列表'},
        //                 {   path: '/caseApiList/project=:project_id/case=:case_id', component: CaseApiList, name: '用例接口列表'},
        //                 {   path: '/addCaseApi/project=:project_id/case=:case_id', component: AddCaseApi, name: '添加新接口'},
        //                 {   path: '/updateCaseApi/project=:project_id/case=:case_id/api=:api_id', component: UpdateCaseApi, name: '修改接口'},
        //                 {   path: '/testReport/project=:project_id', component: TestReport, name: '测试报告'},
        //             ]
        //     },
        //     {   path: '/projectMember/project=:project_id', component: ProjectMember, name: '成员管理', leaf: true},
        //     {   path: '/projectDynamic/project=:project_id', component: ProjectDynamic, name: '项目动态', leaf: true},
        //     {   path: '/projectReport/project=:project_id', component: ProjectReport, name: '自动化测试报告', leaf: true},
        //     ]
    },
];

export default routes;