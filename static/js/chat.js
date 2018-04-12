/* var path = window.location.pathname.split('/')
var socket = new WebSocket(
        'ws://localhost' + window.location.host + 
        'chat/rooms/' + path[path.length -2]) */

var chat = new Vue({
    delimiters: ["[[", "]]"],
    el: '#app',
    data: {
        ws: null,
        msg: '',
        messages: [],
        room: '',
        user: '',
        limit: 10,
        offset: 0
    },
    filters: {
        ago: function (value) {
          var timeagoInstance = timeago()
          return timeagoInstance.format(value)
        }
      },
    methods: {
        onSend () {
            this.ws.send(JSON.stringify({
                room: this.room,
                user: this.user,
                message: this.msg
            }))
            this.msg = ''
        }
    },
    created: function () {
        var path = window.location.pathname.split('/')
        this.room = path[path.length -2]
        this.user = document.querySelector('#user_data').getAttribute('data-userid')
        console.log(this.user)
        var query = `query getMsgs {
            messages(room: ${this.room}, limit: ${this.limit}, offset: ${this.offset}) {
              author {
                id
                avatar
                firstName
                lastName
              }
              room {
                id
              }
              body
              created
            }
          }`

          var csrftoken = Cookies.get('csrftoken')
            axios.post(window.location.origin + '/graphql/', JSON.stringify({query: query}), {
            withCredentials: true,
            headers: {
                'X-CSRFToken': csrftoken,
                'content-type': 'application/json'
            }
            }).then(res => {
            console.log('created: ', res.data)
            this.messages = res.data.data.messages
            }).catch(err => console.log('chat created err: ', err))
    },
    mounted: function () {
        var vueInstance = this
        this.ws = new WebSocket(
            'ws://' + window.location.host + 
            '/chat/rooms/' + this.room + '/')
        
        this.ws.onopen = function (e) {
            console.log('connection opened')
        }

        this.ws.onclose = function (e) {
            console.log('connection closed')
        }

        this.ws.onmessage = function (e) {
            console.log('received data: ' + e.data)
            var data = JSON.parse(e.data)
            var user
            var query = `query getUser{
                user(userId:${data['user']}){
                  id
                  firstName
                  lastName
                  avatar
                }
              }`
            var csrftoken = Cookies.get('csrftoken')
            axios.post(window.location.origin + '/graphql/', JSON.stringify({query: query}), {
            withCredentials: true,
            headers: {
                'X-CSRFToken': csrftoken,
                'content-type': 'application/json'
            }
            }).then(res => {
                console.log('created: ', res.data)
                user = res.data.data.user
                vueInstance.messages.push({
                    author: {
                        id: user.id,
                        firstName: user.firstName,
                        lastName: user.lastName,
                        avatar: user.avatar
                    },
                    room: {
                        id: data['room']
                    },
                    body: data['message'],
                    created: data['created']
                })
            }).catch(err => console.log('chat created err: ', err))
        }
    }
})