var profile = new Vue({
    delimiters: ["[[", "]]"],
    el: '#profile',
    data: {
      user_id: 0,
      offset: 0,
      limit: 10,
      actions: [],
      followers: [],
      following: []
    },
    created () {
      this.user_id = window.location.pathname.substring(9, window.location.pathname.length-1)
      var query = `
      query getActions{
        actions(limit:10, offset:0, isProfile:true, userId:${this.user_id}){
          id
          verb
          created
          actor{
            id
            email
            firstName
            lastName
            avatar
            followers{
              id
              firstName
              lastName
              avatar
            }
            isFollowing{
              id
              firstName
              lastName
              avatar
            }
          }
          target{
            id
            text
            image
          }
          targetActor{
            id
            firstName
            lastName
          }
          comments{
            id
            user{
              id
              avatar
              firstName
              lastName
            }
            body
            created
          }
        }
      }
      `
      var csrftoken = Cookies.get('csrftoken')
      axios.post(window.location.origin + '/graphql/', JSON.stringify({query: query}), {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
          'content-type': 'application/json'
        }
      }).then(res => {
        console.log('created: ', res.data)
        this.followers = res.data.data.actions[0].actor.followers
        this.following = res.data.data.actions[0].actor.isFollowing
        this.actions = res.data.data.actions
      }).catch(err => console.log('created err: ', err))
    },
    methods: {
      onFollow: function () {
        var csrftoken = Cookies.get('csrftoken')
        var btn = document.querySelector('#followBtn')
        payload = {
          id: btn.getAttribute('data-id'),
          action: btn.getAttribute('data-action')
        }
        console.log('payload: ', payload)
        axios.post(window.location.origin + '/follow_user',
          JSON.stringify({
            id: btn.getAttribute('data-id'),
            action: btn.getAttribute('data-action')
          }),
          {
            withCredentials: true,
            headers: {
              'X-CSRFToken': csrftoken,
              'content-type': 'application/json'
            }
          }).then(res => {
            if (res.data['status'] === 'ok') {
              var previous_action = btn.getAttribute('data-action')
              
              // toggle data-action
              btn.setAttribute('action', previous_action === 'follow' ? 'unfollow' : 'follow')
              
              // toggle link text
              btn.innerHTML = previous_action === 'follow' ? 'Unfollow' : 'Follow'
            }
            console.log('response: ' + res.data)
          }).catch(err => console.log('follow err: ', err))
      },
      fetchActions: function () {
        this.offset += 10
        this.limit += 10
        var query = `
        query getActions{
          actions(limit:${this.limit}, offset:${this.offset}, isProfile:true, userId:${this.user_id}){
            id
            verb
            created
            actor{
              id
              email
              firstName
              lastName
              avatar
            }
            target{
              id
              text
              image
            }
            targetActor{
              id
              firstName
              lastName
            }
            comments{
              id
              user{
                id
                avatar
                firstName
                lastName
              }
              body
              created
            }
          }
        }
        `
        var csrftoken = Cookies.get('csrftoken')
        console.log('host: ' + window.location.host)
        axios.post(window.location.origin + '/graphql/', JSON.stringify({query: query}), {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
            'content-type': 'application/json'
          }
        }).then(res => {
          console.log('fetchActions: ', res.data)
          this.actions = this.actions.concat(res.data.data.actions)
        }).catch(err => console.log('fetchActions err: ', err))
      },
      onLike (action) {
        this.createAction(action, 'like')
      },
      onShare (action) {
        this.createAction(action, 'share')
      },
      onComment (action, event) {
        var query = `
        mutation cmtCreate($comment:CommentInput!){
          createComment(comment:$comment){
            id
          }
        }
        `
        var csrftoken = Cookies.get('csrftoken')
        
        axios.post(window.location.origin + '/graphql/', JSON.stringify({
          query: query,
          variables: {
            comment: {
              action: action.id,
              body: event.target.value,
            }
          }
        }), {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
            'content-type': 'application/json'
          }
        }).then(res => {
          console.log(res.data)
        }).catch(err => console.log(err))
      },
      createAction (action, verb) {
        var query = `
        mutation actCreate($input:ActionInput){
          createAction(action:$input){
            id
            verb
          }
        }
        `
        var csrftoken = Cookies.get('csrftoken')
        axios.post(window.location.origin + '/graphql/', JSON.stringify({
          query: query,
          variables: {
            input: {
              verb: verb,
              post: action.target.id,
              targetActor: action.actor.id
            }
          }
        }), {
          withCredentials: true,
          headers: {
            'X-CSRFToken': csrftoken,
            'content-type': 'application/json'
          }
        }).then(res => {
          console.log(res.data)
        }).catch(err => console.log(err))
      }
    },
    filters: {
      ago: function (value) {
        var timeagoInstance = timeago()
        return timeagoInstance.format(value)
      }
    },
    mounted () {
      var vueInstance = this
      var monitor = scrollMonitor.create(document.getElementById('profile_buttom'), -300)
      monitor.enterViewport(function () {
        console.log('entered viewport')
        vueInstance.fetchActions()
      })
    }
  })
  