<template>
    <div style = "margin-top:30px;">
        <Row style="text-align:center;display:inline;">
            <h1>Grade Management System</h1>
        </Row>
    </div>

    <div style = "margin-top:20px;">
        <Row>
            <Col span = "8" offset = "8">
                <Row>
                    <Col span = "4"><h3>Account:</h3></Col>
                    <Col span = "20"><Input v-model = "name"/></Col>
                </Row>
                <Row style = "margin-top:20px;">
                    <Col span = "4"><h3>Password:</h3></Col>
                    <Col span = "20"><Input type = "password" v-model = "password"/></Col>
                </Row>
                <Row style = "margin-top:20px;">
                    <Col offset = "4" span = "20">
                        <Button type="success" long @click='login'>Login</Button>
                    </Col>
                </Row>
            </Col>
        </Row>
    </div>
</template>

<script>
    export default{

        data(){
            return{
                name: '',
                password: '',
            }
        },
        methods:{
            login() {
                if (this.name == ''){
                    this.$Message.info('Please type in user name')
                    return
                }
                if (this.password == ''){
                    this.$Message.info('Please type in password')
                    return
                }
                const param = {name : this.name, password : this.password}

                this.$axios({
                    withCredentials : true,
                    method : "POST",
                    url: 'http://127.0.0.1:9000/login',
                    data : JSON.stringify(param),
                    headers:{
                        'Content-Type' : "application/json",
                    },
                }).then((res)=>{
                    if(res.status != 200){
                        this.$Message.error('API error(' + res.status + ')')
                        return
                    }
                    if(res.data.code != 0){
                        this.$Message.error('LOGIN FAILURE(' + res.data.message + ')')
                        return
                    }
                    this.$Message.success('LOGIN SUCCESS')
                    this.$router.push("/students")
                }).catch((err)=>{
                    this.$Message.error('Network Error(' + err + ')')
                })
            }
        },
    }
</script>

