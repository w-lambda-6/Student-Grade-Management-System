<template>
    <div>
        <Row>
            <Col span = "16" offset = "4">
                <Row>
                    <Col span = "4" style = "text-align: left;">
                        <a href = "javascript:void(0)" @click='this.router.push("/teachers")'>Teacher's Account Management</a>
                    </Col>
                    <Col span = "20" style = "text-align: right;">
                        <a href = "javascript:void(0)" @click='this.router.push("/login")'>Logout</a>
                    </Col>
                </Row>
                <Row>
                    <h1 style = "text-align: center;display:inline;">
                        Student Grade Management
                    </h1>
                </Row>
                <Row style = "margin-top:20px;">
                    <Col span = "2" offset = "10"><Button type = "primary" @click = "get_students">Get List</Button></Col>
                    <Col span = "2" offset = "1"><Button type = "success" @click = "show_add">Add</Button></Col>
                </Row>
                <Row style = "margin-top:20px;">
                    <Col span = "24">
                    <Table :columns = "columns" :data = "data">
                        <template #action = "{row, index}">
                            <Button type = "info" size = "small" @click = "show_modify(row)">Modify</Button>
                            <Button type = "error" size = "small" style = "margin-left:10px;" @click = "del_cfm(row)">Delete</Button>
                        </template>
                        </Table>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>

    <div>
        <Modal
        v-model="add.modal"
        title="New student info:"
        :loading = "add.loading"
        @on-ok="add_ok"
        @on-cancel="add_cancel">
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">Name</Col>
                <Col span = "22"><Input v-model="add.param.name" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">Chinese Score</Col>
                <Col span = "22"><Input v-model="add.param.chinese" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">Math Score</Col>
                <Col span = "22"><Input v-model="add.param.math" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">English Score</Col>
                <Col span = "22"><Input v-model="add.param.english" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
    </Modal>

    <Modal
        v-model="modify.modal"
        title="Modify student info:"
        :loading = "add.loading"
        @on-ok="edit_ok"
        @on-cancel="edit_cancel">
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">ID</Col>
                <Col span = "22"><Input v-model="modify.param.id" size = 'small' style = "width:80%" disabled /></Col>
            </Row>
        </p>
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">Name</Col>
                <Col span = "22"><Input v-model="modify.param.name" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">Chinese Score</Col>
                <Col span = "22"><Input v-model="modify.param.chinese" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">Math Score</Col>
                <Col span = "22"><Input v-model="modify.param.math" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
        <p style="padding: 5px;">
            <Row>
                <Col span = "2">English Score</Col>
                <Col span = "22"><Input v-model="modify.param.english" size = 'small' style = "width:80%"/></Col>
            </Row>
        </p>
    </Modal>
    </div>
</template>

<script>
    export default{

        data(){
            return{
                add:{
                    modal : false,
                    param : {
                        name : '',
                        chinese : '',
                        math : '',
                        english : '',
                    },
                    loading : true,
                },
                modify:{
                    modal : false,
                    param : {
                        id : '',
                        name : '',
                        chinese : '',
                        math : '',
                        english : '',
                    },
                    loading : true,
                },
                columns: [
                    {
                        title:'ID',
                        key:'id',
                        align: 'center',
                    },
                    {
                        title:'Name',
                        key:'name',
                        align: 'center',
                    },
                    {
                        title:'English',
                        key:'english',
                        align: 'center',
                    },
                    {
                        title:'Chinese',
                        key:'chinese',
                        align: 'center',
                    },
                    {
                        title:'Math',
                        key:'math',
                        align: 'center',
                    },
                    {
                        title:'Action',
                        slot:'action',
                        minWidth:120,
                    }
                ],
                data: [],
            }
        },
        // get the student page by default after refreshing
        mounted(){
            this.get_students();
        },
        methods:{
            get_students(){
                this.data = [];
                this.$axios({
                    withCredentials : true,
                    method : "GET",
                    url:"http://127.0.0.1:9000/student_list"
                }).then((res)=>{
                    if(res.status != 200){
                        this.$Message.error('API error(' + res.status + ')')
                        return
                    }
                    if (res.data.code!=0){
                        this.$Message.error('Error(' + res.data.message + ')')
                        return
                    }
                    this.$Message.success(res.data.message)
                    this.data = res.data.data
                }).catch((err)=>{
                    this.$Message.error('Network Error(' + err + ')')
                })
            },
            show_add(){
                this.add.modal = true;
            },
            add_ok(){
                if (this.add.param.name == ''){
                    this.$Message.error("Name is required");
                    // so that the box can stay there
                    this.add.loading = false;
                    this.$nextTick(()=>{
                        this.add.loading = true;
                    });
                    return
                }

                let param = {name : this.add.param.name}
                if (this.add.param.english != ''){
                    param.english = this.add.param.english
                }
                if (this.add.param.chinese != ''){
                    param.chinese = this.add.param.chinese
                }
                if (this.add.param.math != ''){
                    param.math = this.add.param.math
                }
                this.$axios({
                    withCredentials : true,
                    method : "POST",
                    url:"http://127.0.0.1:9000/student_add",
                    data : JSON.stringify(param),
                    headers:{
                        'Content-Type' : "application/json",
                    }
                }).then((res)=>{
                    if(res.status != 200){
                        this.$Message.error('API error(' + res.status + ')')
                        return
                    }
                    if (res.data.code!=0){
                        this.$Message.error('Error(' + res.data.message + ')')
                        return
                    }
                    // automatically close the block
                    this.add.modal=false;
                    this.add_reset();
                    this.$Message.success(res.data.message)

                    // stop the add box from loading after adding
                    this.add.loading = false;
                    // enable the next add box to load
                    this.$nextTick(()=>{
                        this.add.loading = true;
                    });
                    // list the newly created list with new students
                    this.get_students();
                }).catch((err)=>{
                    this.$Message.error('Network Error(' + err + ')')
                })
            },
            add_reset(){
                this.add.param.name = '';
                this.add.param.english = '';
                this.add.param.chinese = '';
                this.add.param.math = '';
            },
            add_cancel(){
                this.add_reset()
            },
            del_cfm(row){
                const self = this
                this.$Modal.confirm({
                    title:"Deletion confirmation",
                    content:'Are you sure you are going to delete (${row.name})?',
                    onOk(){
                        self.del_submit(row.id);
                    },
                    onCancel(){
                        return 
                    }
                });
            },
            del_submit(id){
                const param = {id:id}
                this.$axios({
                    withCredentials : true,
                    method : "POST",
                    url:"http://127.0.0.1:9000/student_del",
                    data : JSON.stringify(param),
                    headers:{
                        'Content-Type' : "application/json",
                    }
                }).then((res)=>{
                    if(res.status != 200){
                        this.$Message.error('API error(' + res.status + ')')
                        return
                    }
                    if (res.data.code!=0){
                        this.$Message.error('Error(' + res.data.message + ')')
                        return
                    }
                    this.$Message.success(res.data.message)
                    this.get_students();
                }).catch((err)=>{
                    this.$Message.error('Network Error(' + err + ')')
                })
            },
            modify_reset(){
                this.modify.param.id = '';
                this.modify.param.name = '';
                this.modify.param.chinese = '';
                this.modify.param.english = '';
                this.modify.param.math = '';
            },
            show_modify(row){
                // we will first clear the modify modal 
                this.modify_reset();
                // we fill the contents of the modal up before we show it
                this.modify.param.id = row.id;
                this.modify.param.name = row.name;
                this.modify.param.chinese = row.chinese;
                this.modify.param.english = row.english;
                this.modify.param.math = row.math;
                this.modify.modal = true;
            },
            modify_cancel(){
                this.modify_reset();
                this.modify.modal = false;
            },
            // we submit data to the backend via this
            modify_ok(){
                if (this.modify.param.name == ''){
                    this.$Message.error("Name is required");
                    // so that the box can stay there
                    this.modify.loading = false;
                    this.$nextTick(()=>{
                        this.modify.loading = true;
                    });
                    return
                }
                const param = {
                    id : this.modify.param.id, 
                    name : this.modify.param.name, 
                    chinese : this.modify.param.chinese, 
                    english : this.modify.param.english, 
                    math : this.modify.param.math,
                }
                this.$axios({
                    withCredentials : true,
                    method : "POST",
                    url:"http://127.0.0.1:9000/student_mod",
                    data : JSON.stringify(param),
                    headers:{
                        'Content-Type' : "application/json",
                    }
                }).then((res)=>{
                    if(res.status != 200){
                        this.$Message.error('API error(' + res.status + ')')
                        return
                    }
                    if (res.data.code!=0){
                        this.$Message.error('Error(' + res.data.message + ')')
                        return
                    }
                    this.modify.modal = false;
                    this.modify_reset();
                    this.$Message.success(res.data.message)
                    this.modify.loading = false;
                    this.$nextTick(()=>{
                        this.modify.loading = true;
                    });
                    this.get_students();
                }).catch((err)=>{
                    this.$Message.error('Network Error(' + err + ')')
                })
            },
        },
    }
</script>