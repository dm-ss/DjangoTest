<!-----页面代码开始----->
<!--
只做了页面展示，其他都没有改
1数据库取值展示到下拉列表
2加密不加密按钮对其他模块影响
3依赖接口默认不可选，点前面的checkbox才可选，
4删除操作及添加操作的js代码修改及编写
5保存及取消按钮的页面跳转功能
-->
<template>
    <section>
        <br/>
        <el-form :model="form" ref="form" :rules="FormRules">
            <div style="border: 1px solid #e6e6e6;margin-bottom: 10px;padding:15px">
                <el-row :gutter="15">
                    <el-col :span='8'><!--apiGroupLevelFirst_id-->
                        <el-form-item label="所属项目:" label-width="83px" prop="getProjectFirstID"><!--apiGroupLevelFirst_id-->
                            <el-select v-model="form.getProjectFirstID" placeholder="请选择所属项目">
                                <el-option v-for="(item,index) in project" :key="index+''" :label="item.project_name" :value="item.id"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>


                    <el-col :span="8">
                        <el-form-item label="类型分组:" label-width="83px" prop="apiGroupLevelFirst_id">
                            <el-select v-model="form.getProject" placeholder="请选择接口类型分组">
                                <el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="15">
                    <el-col :span="8">
                        <el-form-item label="请求方式:" label-width="83px" name="qingqiufangshi">
                            <el-select v-model="form.requestType"  placeholder="请求方式" @change="checkRequest">
                                <el-option v-for="(item,index) in request" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="HTTP协议:" label-width="83px" name="xieyi">
                            <el-select v-model="form.httpType" placeholder="HTTP协议">
                                <el-option v-for="(item,index) in Http" :key="index+''" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>

                </el-row>
                <el-row :gutter="15">
                    <el-col :span='8'>
                        <el-form-item label="接口名称:" label-width="83px" prop="interface_name_zh">
                            <el-input v-model.trim="form.interface_name_zh" placeholder="请输入接口名称" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="方法名称:" label-width="83px" prop="interface_name_en">
                            <el-input v-model.trim="form.interface_name_en" placeholder="请输入方法名称" auto-complete></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-row :gutter="15">
                <!--
                   <el-col :span='8'>
                           <el-form-item label="Content-Tpye:" label-width="120px" prop="apiGroupLevelFirst_id">
                                <el-select v-model="form.apiGroupLevelFirst_id" placeholder="请选择">
                                    <el-option v-for="(item,index) in group" :key="index+''" :label="item.name" :value="item.id"></el-option>
                                </el-select>

                         </el-form-item>
                    </el-col>-->
                    <el-col :span='12'>
                        <el-form-item prop="apiAddress"  label="请求地址:" label-width="83px">
                            <el-input v-model.trim="form.apiAddress" placeholder="请输入请求地址" auto-complete></el-input>
                        </el-form-item>
                    </el-col>

                </el-row>


            </div>

            <!--请求头-->
            <el-row :span="22">
                <el-collapse v-model="activeNames" @change="handleChange">
                    <el-collapse-item title="加密方式1" name="1">
                        <div style="margin: 5px">
                            <el-row :span="24">
                                <el-col :span="4"><el-radio v-model="radio" label="form-data">加密</el-radio></el-col>
                                <el-col v-if="request3" :span="4"><el-radio v-model="radio" label="raw">不加密</el-radio></el-col>

                            </el-row>
                        </div>

                           <!--form.requestList需重写词方法保证只有一个 -->
                        <el-table :data="form.MiList" highlight-current-row :class="ParameterType? 'parameter-a': 'parameter-b'">
                            <el-table-column prop="encryption" label="加密URL" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入加密URL"></el-input>
                                </template>
                            </el-table-column>
                            <el-table-column prop="decrypt" label="解密URL" min-width="40%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.JMUrl" :value="scope.row.JMUrl" placeholder="请输入解密URL"></el-input>
                                </template>
                            </el-table-column>

                        </el-table>

                    </el-collapse-item>
                    <el-collapse-item title="请求Header2" name="2">
                        <div style="margin: 5px">
                            <el-row :span="24">

                            </el-row>
                        </div>
                        <el-table :data="form.requestList" highlight-current-row :class="add">
                            <el-table-column prop="name" label="KEY" min-width="14%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入KEY"></el-input>
                                </template>
                            </el-table-column>

                            <el-table-column prop="_type" label="参数类型" min-width="14%" sortable>
                                <template slot-scope="scope">
                                    <el-select v-model="scope.row._type"  placeholder="请求方式">
                                        <el-option v-for="(item,index) in paramTyep" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column prop="description" label="存在依赖" min-width="6%" sortable>
                                <template slot-scope="scope">

                                    <el-col v-if="request3" :span="2"><el-checkbox >是</el-radio></el-col>
                                  </template>
                            </el-table-column>
                            <el-table-column prop="description" label="依赖接口" min-width="14%" sortable>
                                <template slot-scope="scope">

                                    <el-select v-model="scope.row._type" placeholder="依赖接口名称" >
                                        <el-option v-for="(item,index) in paramTyep" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select></template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="5%">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delParameter(scope.$index)"></i>
                                   </template>
                            </el-table-column>
                            <el-table-column label="" min-width="5%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(form.requestList.length-1)" size="mini" class="el-icon-plus" @click="addParameter"></el-button>
                                </template>
                            </el-table-column>
                        </el-table>

                    </el-collapse-item>

                   <el-collapse-item title="请求Body3" name="2">
                        <div style="margin: 5px">
                            <el-row :span="24">

                            </el-row>
                        </div>
                        <el-table :data="form.requestList" :cell-class-name="cellcb" highlight-current-row :class="">
                            <el-table-column prop="name" label="KEY" min-width="14%" sortable>
                                <template slot-scope="scope">
                                    <el-input v-model.trim="scope.row.name" :value="scope.row.name" placeholder="请输入KEY"></el-input>
                                </template>
                            </el-table-column>

                            <el-table-column prop="_type" label="参数类型" min-width="14%" sortable>
                                <template slot-scope="scope">
                                    <el-select v-model="scope.row._type"  placeholder="请求方式">
                                        <el-option v-for="(item,index) in paramType" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column prop="description" label="存在依赖" min-width="6%" sortable>
                                <template slot-scope="scope">

                                    <el-col v-if="request3" :span="2"><el-checkbox >是</el-radio></el-col>
                                  </template>
                            </el-table-column>
                            <el-table-column prop="description" label="依赖接口" min-width="14%" sortable>
                                <template slot-scope="scope">

                                    <el-select v-model="scope.row._type" placeholder="依赖接口名称" display="none" >
                                        <el-option v-for="(item,index) in paramType" :key="index+''" :label="item.label" :value="item.value"></el-option>
                                    </el-select></template>
                            </el-table-column>
                            <el-table-column label="操作" min-width="5%">
                                <template slot-scope="scope">
                                    <i class="el-icon-delete" style="font-size:30px;cursor:pointer;" @click="delParameter(scope.$index)"></i>
                                   </template>
                            </el-table-column>
                            <el-table-column label="" min-width="5%">
                                <template slot-scope="scope">
                                    <el-button v-if="scope.$index===(form.requestList.length-1)" size="mini" class="el-icon-plus" @click="addParameter"></el-button>
                                </template>
                            </el-table-column>
                        </el-table>

                    </el-collapse-item>




                    <el-collapse-item title="入参示例4" name="inParamShow">
                        <el-card class="box-card">

                            <el-input v-model.trim="form.data.inParamShow" type="textarea" :rows="5" placeholder="请输入入参示例"></el-input>
                        </el-card>
                    </el-collapse-item>
                     <el-collapse-item title="出参示例5" name="outParamShow">
                        <el-card class="box-card">

                            <el-input v-model.trim="form.data.outParamShow" type="textarea" :rows="5" placeholder="请输入出参示例"></el-input>
                        </el-card>
                    </el-collapse-item>
                    <el-collapse-item title="备注" name="content">
                        <el-card class="box-card">
                            <el-input v-model.trim="form.data.content" type="textarea" :rows="5" placeholder="请输入备注"></el-input>
                        </el-card>
                    </el-collapse-item>

                     <el-form-item label="描述" prop='content' label-width="83px">
                                <el-input type="textarea" :rows="7" v-model.trim="editForm.content" placeholder="请输入描述"></el-input>
                     </el-form-item>
                </el-collapse>
            </el-row>
        </el-form>

        <!--
         <router-link :to="{ name: '接口列表', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list"><i class="el-icon-d-arrow-left" style="margin-right: 5px"></i>接口列表</el-button>
        </router-link>-->
        <router-link :to="{ name: '接口列表', params: {project_id: this.$route.params.project_id}}" style='text-decoration: none;color: aliceblue;'>
            <el-button class="return-list" style="float: right">取消</el-button>
        </router-link>
        <el-button class="return-list" type="primary" style="float: right; margin-right: 15px" @click.native="addInterfaceInfo">保存</el-button>

    </section>
</template>
<!-----页面代码结束----->
<!-----脚本代码开始----->
<script>
    //import { addApiDetail, getApiGroupList } from "../../../../api/api";
import { getProjectList } from "../../../../api/api";
    export default {
        data() {
            return {
                request: [{value: 'GET', label: 'GET'},
                    {value: 'POST', label: 'POST'},
                    {value: 'PUT', label: 'PUT'},
                    {value: 'DELETE', label: 'DELETE'}],
                Http: [{value: 'HTTP', label: 'HTTP'},
                    {value: 'HTTPS', label: 'HTTPS'}],
                paramType: [{value: 'Int', label: 'Int'},
                    {value: 'String', label: 'String'},
                    {value: 'Random', label: 'Random'},
                    {value: 'Date', label: 'Date'}],
                checkHeadList: [],
        
                checkParameterList: [],
                ParameterType: true,
                group: [],
                radio: "form-data",
                secondGroup: [],
                status: [{value: true, label: '启用'},
                    {value: false, label: '禁用'}],
                header: [{value: 'Accept', label: 'Accept'},

                    {value: 'Warning', label: 'Warning'}],
                header4: "",
                addParameterFormVisible: false,
                addResponseFormVisible: false,


                radioType: "",
                result: true,
                activeNames: ['1', '2', '3', '4','5'],
                id: "",
                parameterRaw: "",
                request3: true,
                form: {
                    getProjectFirstID: '',//getProject ,apiGroupLevelFirst_id
                    interface_name_zh: '',
                    status: true,
                    requestType: 'POST',
                    httpType: 'HTTP',
                    apiAddress: '',
                    headDict: [{name: "", value: ""},
                        {name: "", value: ""}],
                    requestList: [{name: "", value: "", _type:"String", required: false, restrict: "", description: ""},
                        {name: "", value: "", _type:"String", required: false, restrict: "", description: ""}],
                    MiList: [{MiURL: "", JMiURL: ""}], //加密解密专用


                    requestParameterType: "",
                    responseList: [{name: "", value: "", _type:"String", required:false, description: ""},
                                   {name: "", value: "", _type:"String", required:false, description: ""}],
                    mockCode: '',
                    data: '',
                },
                FormRules: {
                    name : [{ required: false, message: '请输入名称', trigger: 'blur' },
                        { max: 50, message: '不能超过50个字', trigger: 'blur' }],
                    apiAddress : [{ required: false, message: '请输入地址', trigger: 'blur' }],
                    //required : [{ type: 'boolean', required: false, message: '请选择状态', trigger: 'blur' }],
                    getProjectFirstID : [{ type: 'number', required: false, message: '请选择项目', trigger: 'blur'}],
                },
                editForm: {
                    name: "",
                    value: "",
                    required: "",
                    restrict: "",
                    description: "",
                },
                // editLoading: false
            }
        },
        methods: {

             cellcb(row){
              if(row.row.checkStatus === 1&&row.columnIndex === 0){
                return "myCell"
              }
            },


            checkRequest(){
                let request = this.form.requestType;
                if (request==="GET" || request==="DELETE"){
                    this.request3=false
                } else {
                    this.request3=true
                }
            },
            isJsonString(str) {
                try {
                    if (typeof JSON.parse(str) === "object") {
                        return true;
                    }
                } catch(e) {
                }
                return false;
            },




            addInterfaceInfo:function(){//保存按钮
            alert('进入addInterfaceInfo方法，进行数据校验')
                if (this.form.data) {
                    if (!this.isJsonString(this.form.data)) {

                        this.$message({
                            message: '数据错误错误',
                            center: true,
                            type: 'error'
                        })
                    } else {
                        this.addApi()
                    }
                } else if(this.form.data){
                    this.$message({
                        message: '数据不全',
                        center: true,
                        type: 'warning'
                    })
                } else {
                    this.addInterface()
                }
            },
            addInterface: function () {
            alert('进入保存的正式方法')
            console.log(this.form.data)//请求的header2 过来了读取到了值
                this.$refs.form.validate((valid) => {
                alert(1)

                    if (valid) {
                    alert(2)
                        let self = this;
                        console.log(this.form.requestList);
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.form.parameterType = self.radio;
                            let _type = self.form.parameterType;
                            let _parameter = {};
                            _parameter = self.form.requestList;

                            console.log(_parameter)
                            let params = {//构建参数
                                project_id: Number(self.$route.params.project_id),
                                getProjectFirstId: Number(self.form.getProjectFirstId),
                                //apiGroupLevelFirst_id: Number(self.form.apiGroupLevelFirst_id),
                                name: self.form.name,
                                httpType: self.form.httpType,
                                requestType: self.form.requestType,
                                apiAddress: self.form.apiAddress,
                                status: self.form.status,
                                headDict: self.form.headDict,
                                requestParameterType: _type,
                                requestList: _parameter,
                                responseList: self.form.responseList,
                                // mockCode: self.form.mockCode,
                                data: self.form.data,
                                content: "content",
                            };
                            console.log(1234)
                            console.log(params)
                            let headers = {
                                "Content-Type": "application/json",
                                Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))

                            };
                            if (self.parameterRaw&&_type==="raw"){
                                if (!self.isJsonString(self.parameterRaw)) {
                                    self.$message({
                                        message: '源数据格式错误',
                                        center: true,
                                        type: 'error'
                                    })
                                } else {
                                    addApiDetail(headers, params).then(_data => {
                                        let {msg, code, data} = _data;
                                        if (code === '999999') {
                                            self.$router.push({name: '分组接口列表',
                                                params: {
                                                    // project_id: self.$route.params.project_id,
                                                    firstGroup: self.form.getProject
                                                }
                                            });
                                            self.$message({
                                                message: '保存成功',
                                                center: true,
                                                type: 'success'
                                            })
                                        }
                                        else {
                                            self.$message.error({
                                                message: msg,
                                                center: true,
                                            })
                                        }
                                    })
                                }
                            } else {
                                addApiDetail(headers, params).then(_data => {
                                    let {msg, code, data} = _data;
                                    if (code === '999999') {
                                        self.$router.push({name: '分组接口列表',
                                            params: {
                                                project_id: self.$route.params.project_id,
                                                firstGroup: self.form.getProject
                                            }
                                        });
                                        self.$message({
                                            message: '保存成功',
                                            center: true,
                                            type: 'success'
                                        })
                                    }
                                    else {
                                        self.$message.error({
                                            message: msg,
                                            center: true,
                                        })
                                    }
                                })
                            }
                        })
                    }
                })
            },
            editParameterSubmit: function () {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.form.requestList[this.id] = this.editForm;
                        this.addParameterFormVisible = false
                    }
                })
            },
            handleParameterEdit: function (index, row) {
                this.addParameterFormVisible = true;
                this.id = index;
                this.editForm = Object.assign({}, row);
            },
            editResponseSubmit: function () {
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.form.responseList[this.id] = this.editForm;
                        this.addResponseFormVisible = false
                    }
                })
            },
            handleResponseEdit: function (index, row) {
                this.addResponseFormVisible = true;
                this.id = index;
                this.editForm = Object.assign({}, row);
            },



            /// demo  例子
            getProjects() {
                let self = this;
                let params = {
                     project_id: this.$route.params.project_id
                };
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };

                getProjectList(headers, params).then(_data => {
                    let {msg, code, data} = _data;

                    if (code === '999999') {
                    self.group = data;

                        //self.group = data;
                        //self.form.apiGroupLevelFirst_id = self.group[0].id

                        self.project = data;
                        self.form.getProjectFirstID = self.get[0].id
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
                })
            },



            addHead() {
                let headers = {name: "", value: ""};
                this.form.headDict.push(headers)
            },
            delHead(index) {
                this.form.headDict.splice(index, 1);
                if (this.form.headDict.length === 0) {
                    this.form.headDict.push({name: "", value: ""})
                }
            },
            addParameter() {
                let headers = {name: "", value: "", _type:"String", required:true, restrict: "", description: ""};
                this.form.requestList.push(headers)
            },
            delParameter(index) {
                this.form.requestList.splice(index, 1);
                if (this.form.requestList.length === 0) {
                    this.form.requestList.push({name: "", value: "", _type:"String", required:true, restrict: "", description: ""})
                }
            },
            addResponse() {
                let headers = {name: "", value: "", _type:"String", required:true, description: ""};
                this.form.responseList.push(headers)
            },
            cellcb(index) {   // txt.style.display = "none";
                //this.form.responseList.splice(index, 1);

                if(index.row.checkStatus === 1&&index.row.columnIndex === 0){
                alert(index.row.columnIndex)
                    return "myCell"}


            },


            changeParameterType() {//不要删除这个加密URL用的到
                if (this.radio === 'form-data') {
                    this.ParameterType = true
                } else {
                    this.ParameterType = false
                }
            },
            showData() {
                this.result = true
            },
            showHead(){
                this.result = false
            },
            handleChange(val) {
            },
            onSubmit() {
                console.log('submit!');
            },
            fastAdd() {
                let form = this.$route.params.formData;
                let _type = this.$route.params._type;
                let _typeData = this.$route.params._typeData;
                if (form) {
                    this.form.requestList = [];
                    this.form.requestType = form.request4.toUpperCase();
                    this.form.httpType = form.Http4;
                    this.form.apiAddress = form.addr;
                    this.form.headDict = form.head;
                    this.form.parameterRaw = form.parameterRaw;
                    form.parameter.forEach((item) => {
                        item['_type'] = 'String';
                        item['required'] = true;
                        item['restrict'] = '';
                        item['description'] = '';
                        this.form.requestList.push(item)
                    });
                    // this.form.parameter = form.parameter;
                    this.form.mockCode = form.statusCode;
                    this.form.data = JSON.stringify(form.resultData)
                }
                if (_type) {
                    this.radio = _type
                }
                if (_typeData) {
                    this.radioType = _typeData
                }
            }
        },
        watch: {
            radio() {
                this.changeParameterType()
            },
        },
        mounted() {
            this.getProjects();
            this.fastAdd();
        }
    }
</script>

<style lang="scss" scoped>
    .return-list {
        margin-top: 0px;
        margin-bottom: 10px;
        border-radius: 25px;
    }
    .head-class {
        font-size: 17px
    }
    .parameter-a {
        display: block;
    }
    .parameter-b {
        display: none;
    }
    .selectInput {
        position: absolute;
        /*margin-left: 7px;*/
        padding-left: 9px;
        width: 180px;
        /*border-radius:0px;*/
        /*height: 38px;*/
        left: 1px;
        border-right: 0px;
    }
</style>
<style lang="scss">
    .selectInput{
        input{
            border-right: 0px;
            border-radius: 4px 0px 0px 4px;
        }
    }
</style>

<style>
 .myCell .el-checkbox__input {
  display: none
}

</style>