<template>
    <div class="form-container">
        <div class="screen">
            <div class="screen__content">
        <h1>Login </h1>
        <div v-if="success" class="alert alert-success" role="alert">
            <p>Logged IN</p>
        </div>
        <div v-if="errors.length" class="alert alert-danger" role="alert">
            <ul class="error">
                <li  v-for="error in errors" :key="errors.indexOf(error)">{{ error }}</li>
            </ul>
        </div>
        <form @submit.prevent="loginUser" method="post" enctype="multipart/form-data"
            id="LoginForm" 
            ref="LoginForm">
            
            <div class="form-field">
                <label for="username">Username</label>
                <input 
                    type="text" 
                    name="username" 
                    id="username" 
                    v-model="username"
                    required
                />
            </div>
            <div class="form-field">
                <label for="password">Password</label>
                <input 
                    type="password" 
                    name="password" 
                    id="password" 
                    v-model="password"
                    required
                />
            </div>
            <button type="submit" class="submit-btn">Login</button>
        </form>
    </div>
</div>
</div>
</template>

<script>
export default{
    name: 'LoginForm',
    data(){
        return{
            csrf_token: '',
            errors: [],
            success:false
        }
    },
    created(){
        this.getCsrfToken();
    },
    methods:{
        saveUser(){
            let LoginForm = document.getElementById('LoginForm');
            let form_data = new FormData(LoginForm);
            let self = this
            fetch("/api/v1/login", {
                method: 'POST',
                body: form_data,
                headers:{
                    'X-CSRFToken': this.csrf_token
                }
            })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                // display a success message
                console.log(data);
                if('errors' in data){
                    self.errors=[...data.errors]
                    self.success = false
                } else {
                    self.errors=[]
                    self.errors= true
                }
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        getCsrfToken() {
            fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            csrf_token.value = data.csrf_token;
        })
        }
    }
}

</script>
<style scoped>
* {
	box-sizing: border-box;
	margin: 0;
	padding: 0;	
	font-family: Raleway, sans-serif;
}
.screen {		
	background: linear-gradient(90deg, #675eac, #7C78B8);		
	position: relative;	
	height: 300px;
	width: 360px;	
	box-shadow: 0px 0px 24px #5C5696;
}
.screen__content {
	z-index: 1;
	position: relative;	
	height: 100%;
}

.form-container{
    display: grid;
	align-items: center;
	justify-content: center;
	min-height: 100vh
}
.form-field{
    border: none;
	border-bottom: 2px solid #D1D1D4;
	background: none;
	padding: 10px;
	padding-left: 24px;
	font-weight: 700;
	width: 75%;
	transition: .2s;
}
.form-field input, .form-field textarea{
    display: block;
    border: 1px solid #cccccc;
    border-radius: 6px;
}

button{
    font-size: 24px;
	margin-left: auto;
	color: #7875B5;
    background: #fff;
	font-size: 14px;
	margin-top: 30px;
	padding: 16px 20px;
	border-radius: 26px;
	border: 1px solid #D4D3E8;
	text-transform: uppercase;
	font-weight: 700;
	display: flex;
	align-items: center;
	width: 100%;
	color: #4C489D;
	box-shadow: 0px 2px 2px #5C5696;
	cursor: pointer;
	transition: .2s;
}

.submit-btn:active,
.submit-btn:focus,
.submit-btn:hover {
	border-color: #6A679E;
	outline: none;
}
ul, li{
    margin: 0;
}
.alert{
    margin-top: 1rem;
}
</style>