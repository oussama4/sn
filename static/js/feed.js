var postInput = new Vue({
  el: '#post',
  data: {
    post_text: '',
    selectedImage: null
  },
  methods: {
    onFileChanged (event) {
      this.selectedImage = event.target.files[0]
    },
    onUpload () {
      var csrftoken = Cookies.get('csrftoken')
      var formData = new FormData()
      formData.append('post_text', this.post_text)
      formData.append('post_image', this.selectedImage)
      console.log('iamge:', this.selectedImage)

      axios.post('/feed/post', formData, {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
          'content-type': 'multipart/form-data'
        }
      }).then(res => console.log(res)).catch(err => console.log(err))
    }
  }
})

var feed = new Vue({
  delimiters: ["[[", "]]"],
  el: '#feed',
  data: {
    offset: 0,
    limit: 10,
    actions: []
  },
  created () {
    var query = `
    query getActions{
      actions(limit:10, offset:0, isProfile:false){
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
    axios.post('graphql/', JSON.stringify({query: query}), {
      withCredentials: true,
      headers: {
        'X-CSRFToken': csrftoken,
        'content-type': 'application/json'
      }
    }).then(res => {
      console.log('created: ', res.data)
      this.actions = res.data.data.actions
    }).catch(err => console.log('feed created err: ', err))
  },
  methods: {
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
      axios.post('graphql/', JSON.stringify({
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
    fetchActions () {
      this.limit += 10
      this.offset += 10
      var query = `
      query getActions{
        actions(limit:${this.limit}, offset:${this.offset}, isProfile:false){
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
      axios.post('graphql/', JSON.stringify({query: query}), {
        withCredentials: true,
        headers: {
          'X-CSRFToken': csrftoken,
          'content-type': 'application/json'
        }
      }).then(res => {
        console.log('fetchActions: ', res.data)
        if (res.data.data.actions.length === 0) {
          console.log('empty response')
        }
        this.actions = this.actions.concat(res.data.data.actions)
        // block_request = false
        console.log('fetched')
      }).catch(err => console.log('fetchActions err: ', err))
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
      axios.post('graphql/', JSON.stringify({
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
    var monitor = scrollMonitor.create(document.getElementById('feed_buttom'), -300)
    monitor.enterViewport(function () {
      console.log('entered viewport')
      vueInstance.fetchActions()
    })
  }
})
