<template>
    
    <div class="form-container">
        <div class="screen"> 
        <h1>Register Form</h1>
        
        <div v-if="success" class="alert alert-success" role="alert">
            <p>User Successfully added</p>
        </div>
        <div v-if="errors.length" class="alert alert-danger" role="alert">
            <ul class="error">
                <li  v-for="error in errors" :key="errors.indexOf(error)">{{ error }}</li>
            </ul>
        </div>
        <form 
            @submit.prevent="registerUser" 
            method="post" 
            enctype="multipart/form-data"
            id="RegisterForm" 
            ref="RegisterForm">
    

            
                <div class="form-field col">
                    <label for="username">Username</label>
                    <input 
                        type="text" 
                        name="username" 
                        id="username" 
                        v-model="username"
                        required
                    />
                </div>
                <div class="form-field col">
                    <label for="password">Password</label>
                    <input 
                        type="password" 
                        name="password" 
                        id="password"
                        pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                        title="Must contain at least one  number and one uppercase and lowercase letter, and at least 8 or more characters" 
                        v-model="password"
                        required
                    >
                </div>
            
            
                <div class="form-field col">
                    <label for="firstname">First Name</label>
                    <input 
                        type="text" 
                        name="firstname" 
                        id="firstname" 
                        v-model="firstname"
                        required
                    />
                </div>
                
                <div class="form-field col">
                    <label for="lastname">Last Name</label>
                    <input 
                        type="text" 
                        name="lastname" 
                        id="lastname" 
                        v-model="lastname"
                        required
                    />
                </div>
                <div class="form-field col">
                    <label for="email">Email</label>
                    <input 
                        type="email" 
                        name="email" 
                        id="email" 
                        v-model="email"
                        required
                    />
                </div>
            
            
                <div class="form-field col">
                    <label for="location">Location</label>
                    <input 
                        type="text" 
                        name="location" 
                        id="location" 
                        v-model="location"
                        required
                    />
                </div>
                <div class="col"></div>
            
            <div class="form-field">
                <label for="biography">Biography</label>
                <textarea 
                    name="biography" 
                    id="biography" 
                    v-model="biography" 
                    cols="30" 
                    rows="0"
                    required
                ></textarea>
            </div>
            <div class="form-field">
                <label for="photo">Upload photo</label>
                <input 
                    type="file" 
                    name="photo" 
                    id="photo"
                    ref="photo" 
                    accept="image/png, image/jpg, image/jpeg"
                    required
                    @change="handleFileUpload"
                />
            </div>
            

            <button type="submit" class="submit-btn"> <span class="button_text">Register</span>
                <i class="button__icon fas fa-chevron-right"></i>
            </button>
        </form>
    </div>
</div>
</template>

<script>
export default{
    name: 'RegisterForm',
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
            let RegisterForm = document.getElementById('RegisterForm');
            let form_data = new FormData(RegisterForm);
            let self = this
            fetch("/api/v1/register", {
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

.screen {		
	background: linear-gradient(90deg, #675eac, #7C78B8);		
	position: relative;	
	height: 900px;
	width: 360px;	
	box-shadow: 0px 0px 24px #5C5696;
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
#biography{
    width: 100%;
    padding: 16px 20px;
    
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
.button__icon {
	font-size: 24px;
	margin-left: auto;
	color: #1c11e7;
}
.submit-btn:active,
.submit-btn:focus,
.submit-btn:hover {
	border-color: #6A679E;
	outline: none;
}
</style>