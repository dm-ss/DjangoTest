<!--接口维护 add by gaojingyu-->
<template>
    <section>
        <!--工具条-->
        <el-col :span="24" class="toolbar" style="padding-bottom: 0px;">
            <el-form :inline="true" :model="filters" @submit.native.prevent>
                <el-form-item>
                    <el-input v-model="filters.interface_name_en" placeholder="接口名称" @keyup.enter.native="getLyzdInterfaceList"></el-input>
                </el-form-item>
                <el-form-item>

                    <el-button type="primary" @click="getLyzdInterfaceList">查询</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="handleAdd">新增1</el-button>
                </el-form-item>
                <el-form-item>

					<router-link :to="{ path: 'addInterface'}" style='text-decoration: none;color: aliceblue;'>
						<el-button type="primary">新增</el-button>
					</router-link>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" :disabled="update" @click="changeGroup">修改模块</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click.native="DownloadApi">下载接口文档</el-button>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click.native="loadSwaggerApi = true">导入接口</el-button>
					<el-dialog title="导入swagger接口" :visible.sync="loadSwaggerApi" :close-on-click-modal="false">
						<el-input v-model.trim="swaggerUrl" placeholder="请输入swagger接口地址" style="width:90%"></el-input>
						<el-button type="primary" @click="addSubmit" :loading="addLoading">导入</el-button>
						<P v-if="!swaggerUrl" style="color: red; margin: 0px">不能为空</P>
					</el-dialog>
				</el-form-item>

            </el-form>
        </el-col>

        <!--列表-->
        <el-table :data="project" highlight-current-row v-loading="listLoading" @selection-change="selsChange" style="width: 100%;">
            <el-table-column type="selection" min-width="5%">
           <!-- </el-table-column>
            <el-table-column prop="Project_id" label="所属项目" min-width="16%" sortable>
            </el-table-column>-->
            <el-table-column prop="interface_name_zh" label="接口中文名称" min-width="12%" sortable>
            </el-table-column>
            <el-table-column prop="interface_name_en" label="方法名称" min-width="12%" sortable>
            </el-table-column>


            <el-table-column prop="delete_flag" label="状态" min-width="5%" sortable>
                <template slot-scope="scope">
                    <img v-show="!scope.row.delete_flag" src="../assets/icon-yes.svg"/>
                    <img v-show="scope.row.delete_flag" src="../assets/icon-no.svg"/>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="25%">
                <template slot-scope="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                     <el-button size="small" @click="handleEdit(scope.$index, scope.row)">详情</el-button>
                    <el-button type="danger" size="small" @click="handleDel(scope.$index, scope.row)">删除</el-button>
                   <el-button type="info" size="small" @click="handleChangeStatus(scope.$index, scope.row)">{{scope.row.status===false?'启用':'禁用'}}</el-button>

                </template>
            </el-table-column>

        </el-table>
           <!--工具条-->
        <el-col :span="24" class="toolbar">
            <el-button type="danger" @click="batchRemove" :disabled="this.sels.length===0">批量删除</el-button>
            <el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="20" :page-count="total" style="float:right;">
            </el-pagination>
        </el-col>


        <!--编辑界面-->
        <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false" style="width: 75%; left: 12.5%">
            <el-form :model="editForm" label-width="80px"  :rules="editFormRules" ref="editForm">
                <el-form-item label="环境名称" prop="env_desc">
                    <el-input v-model="editForm.env_desc" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="地址" prop='address'>
                     <el-input v-model="editForm.address" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="描述" prop='content'>
                    <el-input type="textarea" :rows="6" v-model="editForm.content"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="editFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="editSubmit" :loading="editLoading">提交</el-button>
            </div>
        </el-dialog>

        <!--新增界面-->
        <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false" style="width: 90%; left: 2%">
            <el-form :model="addForm" label-width="80px" :rules="addFormRules" ref="addForm">
                <el-form-item label="模块" prop="env_desc">
                    <el-input v-model.trim="addForm.env_desc" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="接口名称" prop="address">
                    <el-input v-model.trim="addForm.address" auto-complete="off"></el-input>

                </el-form-item>
                  <el-form-item label="启用状态" prop="address">
                    <el-input v-model.trim="addForm.address" auto-complete="off"></el-input>

                </el-form-item>
                <el-form-item label="描述" prop='content'>
                    <el-input type="textarea" :rows="6" v-model="addForm.content"></el-input>
                </el-form-item>



            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click.native="addFormVisible = false">取消</el-button>
                <el-button type="primary" @click.native="addSubmit" :loading="addLoading">提交</el-button>
            </div>
        </el-dialog>


    </section>
</template>

<script>
    //import NProgress from 'nprogress'
   import { getLyzdInterface,
    //addEnvironment,delEnvironment,updateEnvironment
   //, delProject, disableProject, enableProject,
       // updateProject, addProject
       } from '../api/api';
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

                editFormRules: {
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
                //编辑界面数据
                editForm: {
                    name: '',
                    version: '',
                    type: '',
                    description: ''
                },

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
            // 获取项目列表 getLyzdEnvironments getLyzdEnvironments getLyzdInterfaceList
            getLyzdInterfaceList() {
                this.listLoading = true;
                let self = this;
                let params = { page: self.page, interface_name_zh: self.filters.interface_name_zh};
                //alert(params)



                let headers = {Authorization: 'Token '+JSON.parse(sessionStorage.getItem('token'))};
                getLyzdInterface(headers, params).then((res) => {
                    self.listLoading = false;
                    let { msg, code, data } = res;
                    if (code === '999999') {
                        self.total = data.total;
                        self.project = data.data
                    }
                    else {
                        self.$message.error({
                            message: msg,
                            center: true,
                        })
                    }
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
                        self.getLyzdInterfaceList()
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
                this.getLyzdInterfaceList()
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
                                    self.getLyzdInterfaceList()
                                }
                            })
                        });
                    }
                });
            },
            selsChange: function (sels) {
                this.sels = sels;
            },
            //批量删除
            batchRemove: function () {
                let ids = this.sels.map(item => item.id);
                let self = this;
                this.$confirm('确认删除选中记录吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.listLoading = true;
                    //NProgress.start();
                    let self = this;
                    let params = {ids: ids};
                    let header = {
                        "Content-Type": "application/json",
                        Authorization: 'Token ' + JSON.parse(sessionStorage.getItem('token'))
                    };
                    delEnvironment(header, params).then(_data => {
                        let {msg, code, data} = _data;
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
                        self.getLyzdInterfaceList()
                    });
                })
            }
        },
        mounted() {
            this.getLyzdInterfaceList();
        }
    }

</script>

<style>

</style>
