/* Add your Application JavaScript */
Vue.component('app-header', {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <a class="navbar-brand" href="#">Photogram</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <router-link class="nav-link" v-bind:to="'/users/'+ userid">My Profile <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item active">
            <router-link class="nav-link" to="/explore">Explore <span class="sr-only">(current)</span></router-link>
          </li>
        </ul>
        
        <ul class="navbar-nav" v-if="user">
            <li class="nav-item active">
              <router-link class="nav-link" to="/logout/">Logout <span class="sr-only">(current)</span></router-link>
            </li>  
        </ul>
        <ul class="navbar-nav" v-else>
            <li class="nav-item active">
            <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
          </li>
        </ul>
      </div>
    </nav>
    `,
    watch: {
        '$route' (to, fom){
            this.reload()
        }
      },
    created: function() {
        let self = this;
        self.user=localStorage.getItem('token');
        self.userid=localStorage.getItem('userid')
    },
    data: function() {
        return {
            user: [],
        }
    },
    methods:{
        reload(){
            let self = this;
            self.user=localStorage.getItem('token');
            self.userid=localStorage.getItem('userid')
        }
    }
});

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container-fluid">
            <p class="card-text">Copyright &copy; Flask Inc.</p>
        </div>
    </footer>
    `
});

const Home = Vue.component('home', {
   template: `
    <div class="row container-fluid">
        <div class="col-md-6 landing-container-child">
            <img src="/static/images/water-display.jpg" id="landing-img"/>
        </div>
        <div class="col-md-6 landing-container-child float-clear">
          <div class="card" style="width: 45rem; height: 40rem; box-shadow: 2px 2px 10px grey;">
            <img class="card-img-top" src="static/images/photogramLogo.png" alt="Card image cap" style="width: 60%; margin: 0 auto; padding-top: 20px;">
            <div class="card-body" style="padding-top: 0px;">
              <hr>
              <p class="card-text">Share photos of your favourite moments with friends, family and the world.</p>
              <div style="padding-left: 120px; margin-top: 20%;">
                  <router-link class="btn btn-login col-md-5" to="/register">Register</router-link>
                  <router-link class="btn btn-primary col-md-5" to="/login">Login</router-link>
              </div>
            </div>
          </div>  
        </div>
    </div>
   `,
    data: function() {
       return {}
    }
});



const register= Vue.component('register-form', {
    template: `
        <div class="fix-register">
        <h2>Register</h2>
        <div class="layout border-style">
        <ul class="list">
            <li v-for="resp in error"class="list alert alert-danger">
                {{resp.errors[0]}} <br>
                {{resp.errors[1]}} <br>
                {{resp.errors[2]}} <br>
                {{resp.errors[3]}} <br>
                {{resp.errors[4]}} <br>
                {{resp.errors[5]}} <br>
                {{resp.errors[6]}} <br>
                {{resp.errors[7]}} <br>
            </li>
        </ul>
            <form id="registerForm"  @submit.prevent="registeruser" method="POST" enctype="multipart/form-data">
            <div class="form-space">
                <div class="row">
                    <div class="col-md-11">
                        <div class="form-group">
                            <label class="label_bold" for="msg"> First Name </label>
                        </div>
                        <div class="form-group">
                            <input type="text" id="form_firstName" class="form-control" name="firstName"/>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-11">
                        <div class="form-group">
                            <label class="label_bold" for="msg"> Last Name </label>
                        </div>
                        <div class="form-group">
                            <input type="text" id="form_lastName" class="form-control" name="lastName"/>
                        </div>
                    </div>
                </div>
                  <div class="row">
                      <div class="col-md-11">
                          <div class="form-group">
                              <label class="label_bold" for="msg"> Username </label>
                              <input type="text" id="form_userName" class="form-control" name="userName"/>
                          </div>
                      </div>
                </div>
                <div class="row">
                    <div class="col-md-11">
                        <div class="form-group">
                            <label class="label_bold" for="msg"> Password </label>
                            <input type="password" id="form_password" class="form-control" name="password"/>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-11">
                        <div class="form-group">
                            <label class="label_bold" for="msg"> Email </label>
                            <input type="text" id="form_email" class="form-control" placeholder="eg. exampl@example.com" name="email"/>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-11">
                        <div class="form-group">
                            <label class="label_bold" for="msg"> Location </label>
                            <input type="text" id="form_location" class="form-control" placeholder="eg. Kingston, Jamaica" name="location"/>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-11">
                        <div class="form-group">
                            <label class="label_bold" for="msg"> Biography </label>
                            <textarea id="msg" name="biography" class="form-control"/></textarea>
                        </div>
                    </div>
                </div>
                <p class="label_bold">Profile Picture</p>
                    <div class="row photo">
                        <div class="upload-btn-wrapper">
                            <button id="btn">Browse</button>
                            <input type="file" name="proPhoto"/>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-11">
                        <button class="btn btn-login" type="submit">Register</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
    `,
    data: function() {
       return {
           response: [],
           error: []
       };
    },
    methods: {
        registeruser: function () {
            let self = this;
            let registerForm = document.getElementById('registerForm');
            let form_data = new FormData(registerForm);
            fetch("/api/users/register", { 
                method: 'POST', 
                body: form_data,
                headers: {
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                return response.json();
                })
                .then(function (jsonResponse) {
                // display a success message
                console.log(jsonResponse);
                if(jsonResponse.result){
                    alert("User Added")
                    self.$router.push('/');
                }else if(jsonResponse.errors){
                    self.error = jsonResponse.errors;
                }
                })
                .catch(function (error) {
                console.log(error);
            });
        }
    }
});

const loginform= Vue.component('login-form', {
    template: `
    <div class="fix-login">
      <h2>Login</h2>
      <li v-for="resp in error"class="list alert alert-danger">
                {{resp.errors[0]}} <br>
                {{resp.errors[1]}} <br>
            </li>
      <div class="layout border-style">
        <form id="loginforms" @submit.prevent="loginuser" method="POST" >
            <div class="row">
                <div class="col-md-11">
                    <div class="form-group">
                        <label class="label_bold" for="msg"> Username </label>
                        <input type='text' id='usrname' name='userName' class="form-control"/>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-11">
                    <div class="form-group">
                        <label class="label_bold" for="msg"> Password </label>
                        <input type='password' id='passwd' name='password' class="form-control"/>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-11">
                    <button id="submit" class="btn btn-login">Login</button>
                </div>
            </div>
        </form>
      </div>
    </div>
    `,
    data: function() {
       return {
           response: [],
           error: []
       };
    },
    methods: {
        loginuser: function () {
            let self = this;
            let loginforms = document.getElementById('loginforms');
            let form_data = new FormData(loginforms);
            fetch("/api/auth/login", { 
                method: 'POST', 
                body: form_data,
                headers: {
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                return response.json();
                })
                .then(function (jsonResponse) {
                // display a success message
                console.log(jsonResponse);
                if(jsonResponse.errors){
                    self.error = jsonResponse.errors;
                } else{
                    let jwt_token = jsonResponse.data.token;
                    let userid = jsonResponse.data.userid;
                    localStorage.setItem('token', jwt_token);
                    localStorage.setItem('userid', userid);
                    alert("User login successfully");
                    self.$router.push('/explore');
                }
                })
                .catch(function (error) {
                console.log(error);
            });
        }
    }
});

const profilepage= Vue.component('profile-form', {
    template: `
    <div>
        <div v-if="info" class="container-fluid">
            <li v-for="user in info" class="list">
                <div class="row border-style center profile profiles-container">
                    <a href="#"><img v-bind:src= "'/static/uploads/'+user.photo" class="post_pic"></a>
                        <div class="col">
                            <h2><strong>{{user.firstname}} {{user.lastname}}</strong></h2>
                            <h5><span id="pro_info">{{ user.location}}</span></h5>
                            <span id="pro_info"> Member since: {{ user.joined_on}}</span>
                            <span id="pro_info">{{ user.biography}}</span>
                        </div>
                    <div class="view-profile center col-3 bio">
                        </br>
                        <section class="like like_8oo9w">
                            <p class="follow_count"><span class="post_len">{{output.length}}</span><span class="follow_len">{{numberoffollower.length}}</span></p>
                        </section>
                        <section class="like like_8oo9w">
                            <p class="follow_count"><span class="follow_title">Posts</span><span class="follow_title">Followers</span></p>
                        </section>
                        <div v-if="isuser">
                        </div>
                        <div v-else class="pro-btn">
                            <div v-if="following">
                                <a class="view-btn btn-login pro-style" >Following</a>
                            </div>
                            <div v-else>
                                <a class="view-btn btn-primary pro-style" @click="follow">Follow</a>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
        </div>
        <div v-else>
            <li v-for="resp in info"class="list">
                <h5>No Posts</h5>
            </li>
        </div>
        <div style="flex-direction: column; padding-bottom: 200px; padding-top: 0px;">
            <div class="imageView">
                <li v-for="pic in output" class="list li_grid">
                    <img  v-bind:src= "'/static/uploads/'+pic.photo" class="profile_post">
                </li>
            </div>
        </div>
    </div>
    `,
    watch: {
        '$route' (to, fom){
            this.reload()
        },
        'following' (newvalue, oldvalue){
            this.reload()
        }
      },
    created: function() {
        let self = this;
        let userid = this.$route.params.userid;
        fetch("/api/users/"+userid+"/posts", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            if(jsonResponse.data){
                self.output = jsonResponse.data;
            }
            })
            .catch(function (error) {
            console.log(error);
        });
        fetch("/api/users/"+userid+"/", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            if(jsonResponse.profile){
                self.info = jsonResponse.profile;
            }
            if(jsonResponse.isuser){
                self.isuser = jsonResponse.isuser;
            }else{
                self.isuser = false;
            }
            })
            .catch(function (error) {
            console.log(error);
        });
        fetch("/api/users/"+userid+"/followersnumber", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            if(jsonResponse.follower){
                self.numberoffollower = jsonResponse.follower;
            }
            })
            .catch(function (error) {
            console.log(error);
        });
        fetch("/api/users/"+userid+"/following", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            let follow = jsonResponse.following
            if(follow==false){
                console.log(follow);
                self.following = false;
            }else{
                self.following = true;
            }
            })
            .catch(function (error) {
            console.log(error);
            });
    },
    data: function() {
       return {
           output:[],
           info:[],
           error: [],
           numberoffollower:[],
           following: null,
       };
    },
     methods:{
        reload(){
            let self = this;
            let userid = this.$route.params.userid;
            fetch("/api/users/"+userid+"/posts", { 
                method: 'GET',
                'headers': {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                return response.json();
                })
                .then(function (jsonResponse) {
                // display a success message
                console.log(jsonResponse);
                if(jsonResponse.data){
                    self.output = jsonResponse.data;
                }
                })
                .catch(function (error) {
                console.log(error);
            });
            fetch("/api/users/"+userid+"/", { 
                method: 'GET',
                'headers': {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                return response.json();
                })
                .then(function (jsonResponse) {
                // display a success message
                console.log(jsonResponse);
                if(jsonResponse.profile){
                    self.info = jsonResponse.profile;
                }
                if(jsonResponse.isuser){
                    self.isuser = jsonResponse.isuser;
                }else{
                    self.isuser = false;
                }
                })
                .catch(function (error) {
                console.log(error);
            });
            fetch("/api/users/"+userid+"/followersnumber", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            if(jsonResponse.follower){
                self.numberoffollower = jsonResponse.follower;
            }
            })
            .catch(function (error) {
            console.log(error);
        });
        fetch("/api/users/"+userid+"/following", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            let follow = jsonResponse.following
            if(follow==false){
                console.log(follow);
                self.following = false;
            }else{
                self.following = true;
            }
            })
            .catch(function (error) {
            console.log(error);
            });
        },
        follow(){
            let self = this;
            let userid = this.$route.params.userid;
            fetch("/api/users/"+userid+"/follow", { 
            method: 'POST',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            if(jsonResponse.message){
                let message = jsonResponse.message
                alert(message);
                self.following = true;
            }
            })
            .catch(function (error) {
            console.log(error);
            });
        }
    }
});

const newpost= Vue.component('post-form', {
    template: `
    <div class="fix-register ">
    <div class="layout border-style">
        <ul id = "message">
            <li v-for="resp in response" class="list alert alert-success">
                      {{ resp.message }}
            </li>
            <li v-for="resp in error"class="list alert alert-danger">
                {{resp.errors[0]}} <br>
                {{resp.errors[1]}} <br>
            </li>
        </ul>
          <form id="postforms" @submit.prevent="make_post" method="POST" >
              <p class="label_bold">Photo</p>
                    <div class="row photo">
                        <div class="upload-btn-wrapper">
                            <button id="btn">Browse</button>
                            <input type="file" name="photo"/>
                        </div>
                    </div>
              <div class="row">
                    <div class="col-md-11">
                        <div class="form-group">
                              <label class="label_bold" for="msg">Caption </label>
                              <textarea type='text' id='usrname' name='caption' placeholder="Write a caption..."class="form-control"/></textarea>
                        </div>
                    </div>
              </div>
              <div class="row">
                  <div class="col-md-11">
                      <button id="submit" class="btn btn-login">Submit</button>
                  </div>
              </div>
          </form>
      </div>
      </div>`,
    data: function() {
       return {
           response: [],
           error: []
       };
    },
    methods: {
        make_post: function () {
            let self = this;
            let loginforms = document.getElementById('postforms');
            let form_data = new FormData(postforms);
            let userid = localStorage.getItem('userid');
            fetch("/api/users/"+userid+"/posts", { 
                method: 'POST', 
                body: form_data,
                'headers': {
                    'Authorization': 'Bearer ' + localStorage.getItem('token'),
                    'X-CSRFToken': token
                },
                credentials: 'same-origin'
            })
                .then(function (response) {
                return response.json();
                })
                .then(function (jsonResponse) {
                // display a success message
                console.log(jsonResponse);
                if(jsonResponse.message){
                    let message = jsonResponse.message;
                    alert(message);
                    self.$router.push('/explore');
                } else{
                    self.error = jsonResponse.errors;
                }
                })
                .catch(function (error) {
                console.log(error);
            });
        }
    }
});



const explorepage= Vue.component('explore-form', {
    template: `
    <div>
        <div v-if="messageFlag" class="sidenav">
            <router-link class="btn btn-primary" to="/post/new">New Post</router-link>
        </div>
        <div class="fix-register" v-else>
            <router-link class="btn btn-primary post_div" to="/post/new">New Post</router-link>
            <P class="alert alert-danger"><center> PLEASE LOGIN TO SEE EXPLORE VIEW!!!!!.</br> IF YOU DO NOT HAVE AN ACCOUNT CLICK REGISTER AND SIGN UP :-D </br> P.S: FROM YOUR CREATOR K.NELSON and O.CHRISTIE</center></P>
        </div>
        <div class=" container-fluid fix-explore" v-if="output">
            <li v-for="resp in output"class="list">
                <div id="wrapper">
					<section class="main items">
    					<div class="post-box">
                            <p><img v-bind:src= "'/static/uploads/'+resp.pro_photo"style="width: 2rem; height: 2rem; padding: 3px; border-radius:100px;"/><router-link v-bind:to="'/users/' +resp.userid">{{resp.username}}</router-link></p>
    						<article class="item">
    							<header>
    								<img v-bind:src= "'/static/uploads/'+resp.photo" style="width: 32.9rem; height: 20rem;"/>
    							</header>
    							<p class="caption"><strong style="color:black;">{{resp.username}}</strong> {{resp.caption}}</p>
    						</article>
    						<section class="like like_8oo9w">
                                <a class="like_eszkz like_l9yih nohover" href="#" role="button"><span class="span_8scx2 coreSpriteHeartOpen">Likes</span></a>
                                <a class="like_eszkz like_et4ho nohover" href="#"><span class="span_8scx2 coreSpriteHeartOpen2">28 Apr 2018</span></a>
                            </section>
    					</div>
					</section>
			     </div>
            </li>
        </div>
        <div v-else>
            <li v-for="resp in output"class="list">
                <h5>No Posts</h5>
            </li>
        </div>
    </div>
    `,
    created: function() {
        let self = this;
        fetch("/api/posts/", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
                'X-CSRFToken': token
            },
            credentials: 'same-origin'
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            if(jsonResponse.data){
                self.output = jsonResponse.data
                self.messageFlag = true;
            }
            })
            .catch(function (error) {
            console.log(error);
        });
    },
    data: function() {
       return {
           output: [],
           error: [],
           messageFlag: false
       };
    }
});


const logout= Vue.component('logout-form', {
    template: `<div></div>`,
    created: function() {
        let self = this;
        fetch("/api/auth/logout", { 
            method: 'GET',
            'headers': {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
        })
            .then(function (response) {
            return response.json();
            })
            .then(function (jsonResponse) {
            // display a success message
            console.log(jsonResponse);
            let message = jsonResponse.message;
            if(jsonResponse.message){
                localStorage.removeItem('token');
                localStorage.removeItem('userid');
                alert (message);
                self.$router.push('/');
                
            }
            })
            .catch(function (error) {
            console.log(error);
        });
    },
    methods: {
    }
});

Vue.use(VueRouter);

// Define Routes
const router = new VueRouter({
    routes: [
        { path: "/", component: Home },
        { path: "/register/", component: register },
        { path: "/login/", component: loginform },
        { path: "/users/:userid", component: profilepage },
        { path: "/logout/", component: logout },
        { path: "/post/new", component: newpost },
        { path: "/explore", component: explorepage }
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});