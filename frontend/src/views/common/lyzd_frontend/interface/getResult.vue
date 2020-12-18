<!--接口维护 add by gaojingyu-->
<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>

                <el-form-item>

                    <el-button type="primary" @click="getResult">查询</el-button>
                </el-form-item>
            </el-form>
        </el-col>

    </section>
</template>

<script>

   import { getResult,


       // updateProject, addProject
       } from '../../../../api/api';
     // import { getProject, delProject, disableProject, enableProject,
      //  updateProject, addProject} from '../api/api';
    // import ElRow from "element-ui/packages/row/src/row";
    export default {
        // components: {ElRow},
        data() {
            return {
                filters: {
                    name: ''
                },
                project: [],
                total: 0,
                page: 1,
                listLoading: false,
                sels: [],//列表选中列

                editFormVisible: false,//编辑界面是否显示
                editLoading: false,
                //options: [{ label: "Web", value: "Web"}, { label: "App", value: "App"}],




                addFormVisible: false,//新增界面是否显示
                addLoading: false,
                addFormRules: {
                    env_desc: [
                        { required: true, message: '请输入环境名称', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],

                    address: [
                        { required: true, message: '请输入地址', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],
                    content: [
                        { required: true, message: '请输入描述', trigger: 'blur' },
                        { max: 255, message: '不能超过125个字符', trigger: 'blur' }
                    ]
                },
                //新增界面数据
                addForm: {
                    name: '',
                    version: '',
                    type: '',
                    description: ''
                }

            }
        },
        methods: {
            // 获取项目列表 getLyzdEnvironments getLyzdEnvironments getResult

            getResult() {
                this.listLoading = true;
                let self = this;
                let params = { page: self.page, interface_name_zh: self.filters.interface_name_zh};
                //alert(params)



                let headers = {Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))};
                getResult(headers).then((res) => {

                })
            },
            //删除
            handleDel: function (index, row) {
                this.$confirm('确认删除该记录吗?', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: [row.id, ]};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                    };
                    delEnvironment(header, params).then(_data => {
                        let { msg, code, data } = _data;
                        if (code === '999999') {
                            self.$message({
                                message: '删除成功',
                                center: true,
                                type: 'success'
                            })
                        } else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                        self.getResult()
                    });
                })
            },
            // 改变项目状态
            handleChangeStatus: function(index, row) {
                let self = this;
                this.listLoading = true;
                let params = { project_id: row.id};
                let headers = {
                    "Content-Type": "application/json",
                    Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                };
                if (row.status) {
                    disableProject(headers, params).then(_data => {
                        let { msg, code, data } = _data;
                        self.listLoading = false;
                        if (code === '999999') {
                            self.$message({
                                message: '禁用成功',
                                center: true,
                                type: 'success'
                            });
                            row.status = !row.status;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                } else {
                    enableProject(headers, params).then(_data => {
                        let { msg, code, data } = _data;
                        self.listLoading = false;
                        if (code === '999999') {
                            self.$message({
                                message: '启用成功',
                                center: true,
                                type: 'success'
                            });
                            row.status = !row.status;
                        }
                        else {
                            self.$message.error({
                                message: msg,
                                center: true,
                            })
                        }
                    });
                }
            },
            handleCurrentChange(val) {
                this.page = val;
                this.getResult()
            },
            //显示编辑界面
            handleEdit: function (index, row) {
                this.editFormVisible = true;
                this.editForm = Object.assign({}, row);
            },
            //显示新增界面
            handleAdd: function () {
                this.addFormVisible = true;
            },
            //编辑
            editSubmit: function () {
                let self = this;
                this.$refs.editForm.validate((valid) => {
                    if (valid) {
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.editLoading = true;
                            //NProgress.start();
                            let params = {
                                id: self.editForm.id,
                                env_desc: self.editForm.env_desc,
                                address: self.editForm.address,
                                content: self.editForm.content,
                            };
                            //alert(params)
                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            updateEnvironment(header, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.editLoading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '修改成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['editForm'].resetFields();
                                    self.editFormVisible = false;
                                    self.getLyzdEnterfaceList()
                                } else if (code === '999997'){
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                }
                            });
                        });
                    }
                });
            },
            //新增
            addSubmit: function () {
                this.$refs.addForm.validate((valid) => {
                    if (valid) {
                        let self = this;
                        this.$confirm('确认提交吗？', '提示', {}).then(() => {
                            self.addLoading = true;
                            //NProgress.start();
                            let params = JSON.stringify({
                                env_desc: self.addForm.env_desc,
                                address: self.addForm.address,
                                content: self.addForm.content,

                            });


                            let header = {
                                "Content-Type": "application/json",
                                Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))
                            };
                            addEnvironment(header, params).then(_data => {
                                let {msg, code, data} = _data;
                                self.addLoading = false;
                                if (code === '999999') {
                                    self.$message({
                                        message: '添加成功',
                                        center: true,
                                        type: 'success'
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.getLyzdEnterfaceList()
                                } else if (code === '999997') {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    })
                                } else {
                                    self.$message.error({
                                        message: msg,
                                        center: true,
                                    });
                                    self.$refs['addForm'].resetFields();
                                    self.addFormVisible = false;
                                    self.getResult()
                                }
                            })
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },

        },
        mounted() {
            this.getResult();
        }
    }

</script>

<style>

</style>
